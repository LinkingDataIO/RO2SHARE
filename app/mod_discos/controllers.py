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

from app import db

mod_discos = Blueprint('discos', __name__, url_prefix='/disco')
CORS(mod_discos)


@mod_discos.route('/create', methods=['GET'])
def create_disco():
    research_objects = request.get_json()
    orcid = research_objects['orcid']
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