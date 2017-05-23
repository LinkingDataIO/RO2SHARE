from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
import urllib2
from SPARQLWrapper import SPARQLWrapper, JSON, POST
import urllib
from docs import conf
from app.mod_auth.models import User
from docs import rdf_templates as rdft
from docs import sparql_templates as sparqlt
import tempfile
from app.utils.sparql_access import load_turtle

from app import db

mod_research_objects = Blueprint('ro', __name__, url_prefix='/ro')
CORS(mod_research_objects)


@mod_research_objects.route('/claim', methods=['POST'])
def claim_ro():
    research_object = request.get_json()
    orcid = research_object['orcid']
    research_object = research_object['_source']
    if not person_exist(orcid):
        req = urllib2.Request('http://orcid.org/' + orcid)
        req.add_header('Accept', 'text/turtle')
        response = urllib2.urlopen(req)
        load_turtle('/tmp/' + orcid + '.ttl', response.read())
    load_turtle('/tmp/' + research_object['id'] + '.ttl', create_creative_work(research_object, orcid))
    return jsonify({'result': 'ok'})


@mod_research_objects.route('/mine', methods=['GET'])
def get_mine():
    orcid = request.args.get('orcid')
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    orcid = 'http://orcid.org/' + orcid
    query = sparqlt.USER_ROS.format(orcid=orcid)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ros = []
    for result in results['results']['bindings']:
        ro = dict(uri=result['uri']['value'], title=result['title']['value'])
        ros.append(ro)
    return jsonify(ros)


def create_creative_work(research_object, orcid):
    user = User.query.filter_by(orcid=orcid).first()
    user_name = user.name
    cw_turtle = rdft.PREFIXES
    work_uri = conf.BASE_URI + '/work/' + research_object['id']

    share_url = 'https://share.osf.io/creativework/' + research_object['id']
    cw_turtle += rdft.CREATIVE_WORK_SAME_AS.format(work_uri=work_uri, web_site=share_url)

    work_type = research_object['type'].replace(' ', '_')
    work_type = rdft.FABIO_TYPES[work_type] if work_type in rdft.FABIO_TYPES else rdft.FABIO_TYPES['default']
    creative_work_type = rdft.CREATIVE_WORK_TYPE.format(work_uri=work_uri, type=work_type)
    cw_turtle += creative_work_type

    work_title = research_object['title'].encode('utf8')
    work_title = rdft.CREATIVE_WORK_TITLE.format(work_uri=work_uri, title=work_title)
    cw_turtle += work_title

    for identifier in research_object['identifiers']:
        cw_turtle += rdft.CREATIVE_WORK_IDENTIFIER.format(work_uri=work_uri, identifier=identifier)
        if 'doi' in identifier:
            cw_turtle += rdft.CREATIVE_WORK_DOI.format(work_uri=work_uri, doi=identifier)
        else:
            cw_turtle += rdft.CREATIVE_WORK_SEE_ALSO.format(work_uri=work_uri, web_site=identifier)

    for publisher in research_object['lists']['publishers']:
        publisher_uri = conf.BASE_URI + 'publishers/' + publisher['id']
        publisher_type = publisher['type']
        publisher_type = rdft.FOAF_TYPES[publisher_type]
        publisher_name = publisher['name']
        cw_turtle += rdft.PUBLISHER.format(publisher_uri=publisher_uri, type=publisher_type, name=publisher_name)
        cw_turtle += rdft.CREATIVE_WORK_PUBLISHER.format(work_uri=work_uri, publisher_uri=publisher_uri)

    for contributor in research_object['lists']['contributors']:
        contributor_uri = 'http://orcid.org/' + orcid
        if user_name.lower() not in contributor['name'].lower():
            contributor_uri = conf.BASE_URI + 'contributors/' + contributor['id']
            contributor_name = contributor['name'].encode('utf8')
            cw_turtle += rdft.PERSON.format(contributor_uri=contributor_uri, name=contributor_name)
        cw_turtle += rdft.CREATIVE_WORK_CREATOR.format(work_uri=work_uri, creator_uri=contributor_uri)
        for affiliation in contributor['affiliations']:
            affiliation_uri = conf.BASE_URI + 'affiliations/' + affiliation['id']
            cw_turtle += rdft.AFFILIATION.format(affiliation_uri=affiliation_uri,
                                                 name=affiliation['name'].encode('utf8'))

            person_uri_role = contributor_uri + '/roles/' + affiliation['id']
            cw_turtle += rdft.PERSON_WORK_AFFILIATION.format(person_uri=contributor_uri,
                                                             person_uri_role=person_uri_role,
                                                             work_uri=work_uri,
                                                             affiliation_uri=affiliation_uri)
    for tag in research_object['tags']:
        tag_rdf = rdft.CREATIVE_WORK_TAG.format(work_uri=work_uri, tag=tag)
        cw_turtle += tag_rdf
    return cw_turtle


def person_exist(orcid):
    user = User.query.filter_by(orcid=orcid).first()
    user_name = user.name
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    query = sparqlt.USER_EXIST_QUERY.format(orcid=orcid, name=user_name)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = bool(sparql.query().convert()['boolean'])
    return result
