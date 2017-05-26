from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON
from docs import conf
from app.utils.sparql_access import load_turtle, get_turtle_uri
from docs import rdf_templates as rdft
from docs import sparql_templates as sparqlt
import uuid


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
    file_path = os.path.join(current_app.root_path, conf.TMP_DIR) + disco_uri.replace('/', '_') + '.ttl'
    load_turtle(file_path, disco_rdf)
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
        if 'uri' in result:
            ro = dict(uri=result['uri']['value'], title=result['title']['value'], objects=result['objects']['value'])
            ros.append(ro)
    return jsonify(ros)


@mod_discos.route('/download', methods=['GET'])
def download_disco():
    disco_uri = request.args.get('uri')
    turtle_str = get_turtle_uri(disco_uri, True)
    filepath = os.path.join(current_app.root_path, conf.TMP_DIR)
    file_name = disco_uri.replace('/', '_') + 'DOWNLOAD.ttl'
    with open(filepath + file_name, 'w') as rdf_file:
        rdf_file.write(turtle_str)
    return send_from_directory(directory=filepath, filename=file_name)
