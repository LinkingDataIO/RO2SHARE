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

mod_slideshare = Blueprint('slideshare', __name__, url_prefix='/slideshare')
CORS(mod_slideshare)


@mod_slideshare.route('/search', methods=['GET'])
def get_presentations():
    username = request.args.get('username')
    password = request.args.get('password')
    orcid = request.args.get('orcid')
    ts = str(math.ceil(time.time()))
    hash_slideshare = conf.SLIDESHARE_SECRET + ts
    sha_1 = sha1()
    sha_1.update(hash_slideshare)
    hash_slideshare = sha_1.hexdigest()
    slideshare_params = conf.SLIDESHARE_PARAMS.format(api_key=conf.SLIDESHARE_API_KEY,
                                                      ts=ts, hash=hash_slideshare,
                                                      username=username,
                                                      password=password)
    print conf.SLIDESHARE_API_URL + slideshare_params
    req = urllib2.Request(conf.SLIDESHARE_API_URL + slideshare_params)
    response = urllib2.urlopen(req)
    presentations_soup = BeautifulSoup(response.read(), 'lxml-xml')
    presentations_xml = presentations_soup.find_all('Slideshow')
    presentations = []
    for presentation_xml in presentations_xml:
        presentation = dict()

        presentation['id'] = presentation_xml.find('ID').string
        presentation['url'] = presentation_xml.find('URL').string
        presentation['title'] = presentation_xml.find('Title').string.replace('\n', ' ')
        description = presentation_xml.find('Description').string
        if description:
            description = description.replace('\n', ' ')
        presentation['description'] = description
        presentation['language'] = presentation_xml.find('Language').string
        presentation['format'] = presentation_xml.find('Format').string
        presentation['claimed'] = presentation_exists(presentation['url'], orcid)

        presentations.append(presentation)
    return jsonify(presentations)


def presentation_exists(presentation_url, orcid):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    orcid = 'http://orcid.org/' + orcid
    query = sparqlt.RO_EXIST.format(orcid=orcid, share_url=presentation_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return bool(sparql.query().convert()['boolean'])
