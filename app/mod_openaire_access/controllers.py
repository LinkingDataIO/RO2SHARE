from flask import Blueprint, request, json, jsonify
from flask_cors import CORS
from docs import conf, sparql_templates as sparqlt
from app.mod_auth.models import User
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib2
import urllib
import time
import math
from hashlib import sha1
from bs4 import BeautifulSoup
import uuid

mod_openaire = Blueprint('openaire', __name__, url_prefix='/openaire')
CORS(mod_openaire)


@mod_openaire.route('/search/', methods=['GET'])
def get_openaire_data():
    orcid = request.args.get('orcid')
    user = User.query.filter_by(orcid=orcid).first()
    username = urllib.quote_plus(user.name)
    openaaire_objects = []
    req = urllib2.Request(conf.OPENAIRE_PUBLICATION_API_URL.format(author=username))
    print conf.OPENAIRE_PUBLICATION_API_URL.format(author=username)
    response = urllib2.urlopen(req)
    objects_xml = BeautifulSoup(response.read(), 'lxml-xml')
    openaaire_objects += parse_objects(objects_xml, 'creative work', orcid)

    req = urllib2.Request(conf.OPENAIRE_DATASET_API_URL.format(author=username))
    response = urllib2.urlopen(req)
    openaaire_objects_xml = BeautifulSoup(response.read(), 'lxml-xml')
    openaaire_objects += parse_objects(openaaire_objects_xml, 'dataset', orcid)
    return jsonify(openaaire_objects)


def parse_objects(openaaire_objects_xml, objects_type, orcid):
    openaire_objects_xml = openaaire_objects_xml.select('results > result')
    openaire_objects = []

    for object_xml in openaire_objects_xml:
        openaire_object = dict()
        openaire_object['type'] = objects_type
        openaire_object['id'] = object_xml.find('dri:objIdentifier').string
        openaire_object['url'] = object_xml.find('webresource').find('url').string
        openaire_object['claimed'] = openaire_result_exists(openaire_object['url'], orcid=orcid)
        openaire_object['title'] = object_xml.find('title').string
        description = object_xml.find('description').string
        openaire_object['description'] = description if description else openaire_object['title']

        openaire_object['tags'] = []
        tags_xml = object_xml.find_all('subject')
        tags_xml = [] if not tags_xml else tags_xml
        for tag_xml in tags_xml:
            if tag_xml.string and tag_xml.string not in openaire_object['tags']:
                openaire_object['tags'].append(tag_xml.string)

        openaire_object['identifiers'] = []
        pids_xml = object_xml.find_all('pid')
        pids_xml = [] if not pids_xml else pids_xml

        for pid_xml in pids_xml:
            if pid_xml.string:
                openaire_object['identifiers'].append(pid_xml.string)

        openaire_object['lists'] = dict(publishers=[], contributors=[])
        publishers_xml = object_xml.find_all('publisher')
        publishers_xml = [] if not publishers_xml else publishers_xml
        for publisher_xml in publishers_xml:
            if publisher_xml.string:
                publisher = dict(type='organization', id=uuid.uuid4().hex, name=publisher_xml.string)
                openaire_object['lists']['publishers'].append(publisher)

        contributors_xml = object_xml.find_all('to', {'class': 'hasAuthor'})
        contributors_xml = [] if not contributors_xml else contributors_xml

        for contributor_xml in contributors_xml:
            contributor_name = contributor_xml.parent.find('fullname').string
            if contributor_name and contributor_name != '':
                contributor_name = parse_name(contributor_name)
                contributor = dict(affiliations=[], id=uuid.uuid4().hex, name=contributor_name)
                openaire_object['lists']['contributors'].append(contributor)
        openaire_objects.append(openaire_object)
    return openaire_objects


def parse_name(name):
    if ',' in name:
        name = name.split(',')
        name = name[1] + ' ' + name[0]
    return name


def openaire_result_exists(url, orcid):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    orcid = 'http://orcid.org/' + orcid
    query = sparqlt.RO_EXIST.format(orcid=orcid, share_url=url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return bool(sparql.query().convert()['boolean'])
