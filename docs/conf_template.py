# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

ORCID_CLIENT_ID = ""
ORCID_SECRET = ""
ORCID_API_URL = "https://orcid.org/oauth/token"

GITHUB_CLIENT_ID = ""
GITHUB_SECRET = ""
GITHUB_API_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API_URL = "https://api.github.com/user"

SHARE_API_URL = "https://share.osf.io/api/v2/search/creativeworks/_search"

SLIDESHARE_API_URL = "https://www.slideshare.net/api/2/get_slideshows_by_user"
SLIDESHARE_PARAMS = "?api_key={api_key}&ts={ts}&hash={hash}&username_for={username}"
SLIDESHARE_API_KEY = ""
SLIDESHARE_SECRET = ""

OPENAIRE_PUBLICATION_API_URL = "http://api.openaire.eu/search/publications?author={author}"
OPENAIRE_DATASET_API_URL = "http://api.openaire.eu/search/datasets?author={author}"

SPARQL_QUERY_ENDPOINT = "http://localhost:3030/ro2share/sparql"
SPARQL_UPLOAD_ENDPOINT = "http://localhost:3030/ro2share/update"


BASE_URI = 'http://ro2share.org/'

TMP_DIR = 'tmp/'