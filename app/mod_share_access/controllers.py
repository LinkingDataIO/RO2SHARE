from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
import urllib2
import urllib
from docs import conf
from app.mod_auth.models import User


from app import db

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
    return jsonify(share_results)
