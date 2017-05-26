from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
import urllib2
from docs import conf, sparql_templates as sparqlt
from app.mod_auth.models import User
from SPARQLWrapper import SPARQLWrapper, JSON

mod_share_access = Blueprint('share', __name__, url_prefix='/share')
CORS(mod_share_access)


@mod_share_access.route('/search/', methods=['GET', 'OPTIONS'])
def share_search():
    orcid = request.args.get('orcid')
    user = User.query.filter_by(orcid=orcid).first()
    query = 'contributors:"' + user.name + '"'
    params = {
        'query': {
            'query_string': {
                'query': query
            }
        }
    }
    req = urllib2.Request(conf.SHARE_API_URL)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(params))
    share_results = json.loads(response.read())
    share_results = share_results['hits']['hits']
    for result in share_results:
        result['claimed'] = share_result_exists(result['_id'], orcid)
    return jsonify(share_results)


def share_result_exists(share_id, orcid):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    orcid = 'http://orcid.org/' + orcid
    share_url = 'https://share.osf.io/creativework/' + share_id
    query = sparqlt.RO_EXIST.format(orcid=orcid, share_url=share_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return bool(sparql.query().convert()['boolean'])
