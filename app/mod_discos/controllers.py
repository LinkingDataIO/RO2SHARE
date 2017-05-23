from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
import urllib2
from SPARQLWrapper import SPARQLWrapper, JSON, POST
import urllib
from docs import conf
from app.utils.sparql_access import load_turtle
from app.mod_auth.models import User
from docs import rdf_templates as rdft
from docs import sparql_templates as sparqlt
import tempfile
import uuid

from app import db

mod_discos = Blueprint('discos', __name__, url_prefix='/disco')
CORS(mod_discos)


@mod_discos.route('/create', methods=['POST'])
def create_disco():
    disco = request.get_json()
    orcid = 'http://orcid.org/' + disco['orcid']
    disco_uri = conf.BASE_URI + 'discos/' + uuid.uuid4().hex
    disco_rdf = rdft.PREFIXES
    disco_rdf += rdft.DISCO.format(disco_uri=disco_uri, disco_description=disco['description'], person_uri=orcid)
    for ro in disco['ros']:
        disco_rdf += rdft.DISCO_RESOURCE.format(disco_uri=disco_uri, ro_uri=ro)
    load_turtle('/tmp/' + disco_uri.replace('/', '_') + '.ttl', disco_rdf)
    return jsonify(disco)


@mod_discos.route('/mine', methods=['GET'])
def get_mine():
    orcid = request.args.get('orcid')
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    orcid = 'http://orcid.org/' + orcid
    query = sparqlt.USER_DISCOS.format(orcid=orcid)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ros = []
    for result in results['results']['bindings']:
        ro = dict(uri=result['uri']['value'], title=result['title']['value'], objects=result['objects']['value'])
        ros.append(ro)
    return jsonify(ros)
