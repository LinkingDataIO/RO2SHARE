from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
import urllib2
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib
from docs import conf
from app.mod_auth.models import User
from docs import rdf_templates as rdft
from docs import sparql_templates as sparqlt
import tempfile

from app import db

mod_research_objects = Blueprint('ro', __name__, url_prefix='/ro')
CORS(mod_research_objects)


@mod_research_objects.route('/claim', methods=['POST'])
def claim_ro():
    research_object = request.get_json()
    orcid = research_object['orcid']
    research_object = research_object['_source']
    req = urllib2.Request('http://orcid.org/' + orcid)
    req.add_header('Accept', 'text/turtle')
    response = urllib2.urlopen(req)

    load_turtle('/tmp/' + orcid + '.ttl', response.read())
    load_turtle('/tmp/' + research_object['id'] + '.ttl', create_creative_work(research_object, orcid))
    return jsonify({'result': 'ok'})


def load_turtle(file_path, turtle_str):
    with open(file_path, 'a') as rdf_file:
        rdf_file.write(turtle_str)
        query = 'LOAD <file://' + file_path + '>'
        sparql = SPARQLWrapper(conf.SPARQL_UPLOAD_ENDPOINT)
        sparql.setQuery(query)
        sparql.query()


def create_creative_work(research_object, orcid):
    cw_turtle = rdft.PREFIXES
    work_uri = conf.BASE_URI + '/work/' + research_object['id']

    work_type = research_object['type'].replace(' ', '_')
    work_type = rdft.FABIO_TYPES[work_type]
    creative_work_type = rdft.CREATIVE_WORK_TYPE.format(work_uri=work_uri, type=work_type)
    cw_turtle += creative_work_type

    work_title = research_object['title']
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
        if not person_exist(orcid, contributor['name']):
            contributor_uri = conf.BASE_URI + 'contributors/' + contributor['id']
            cw_turtle += rdft.PERSON.format(contributor_uri=contributor_uri, name=contributor['name'])
        cw_turtle += rdft.CREATIVE_WORK_CREATOR.format(work_uri=work_uri, creator_uri=contributor_uri)
        for affiliation in contributor['affiliations']:
            affiliation_uri = conf.BASE_URI + 'affiliations/' + affiliation['id']
            cw_turtle += rdft.AFFILIATION.format(affiliation_uri=affiliation_uri, name=affiliation['name'])

            person_uri_role = contributor_uri + '/roles/' + affiliation['id']
            cw_turtle += rdft.PERSON_WORK_AFFILIATION(person_uri=contributor_uri, person_uri_role=person_uri_role,
                                                      work_uri=work_uri, affiliation_uri=affiliation_uri)
    return cw_turtle


def person_exist(orcid, name):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    query = sparqlt.USER_EXIST_QUERY.format(orcid=orcid, name=name)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = bool(sparql.query().convert()['boolean'])
    return result
