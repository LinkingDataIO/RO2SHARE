# Import flask dependencies
from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
import urllib2
import urllib
from docs import conf
# Import the database object from the main app module
from app import db


# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(mod_auth)


# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'OPTIONS'])
def signin():
    auth_code = request.args.get('orcid_auth_code')
    params = {'client_id': conf.ORCID_CLIENT_ID,
              'client_secret': conf.ORCID_SECRET,
              'grant_type': 'authorization_code',
              'code': auth_code,
              'redirect_uri': 'http://localhost:4200/login'
              }
    data = urllib.urlencode(params)
    req = urllib2.Request(conf.ORCID_API_URL, data)
    response = urllib2.urlopen(req)
    user_data = json.loads(response.read())
    if not user_exists(user_data['orcid']):
        create_user(user_data['orcid'], user_data['name'], None, user_data['access_token'])
    return jsonify(user_data)


def user_exists(orcid):
    user = User.query.filter_by(orcid=orcid).first()
    return True if user else False


def create_user(orcid, name, aka, token):
    user = User(orcid=orcid, name=name, aka=aka, token=token)
    db.session.add(user)
    db.session.commit()
