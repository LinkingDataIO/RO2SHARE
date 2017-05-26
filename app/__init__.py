# Import flask and template operators
from flask import Flask, render_template
import os
from docs import conf
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('docs.conf')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_share_access.controllers import mod_share_access as share_access_module
from app.mod_research_objects.controllers import mod_research_objects
from app.mod_discos.controllers import mod_discos
from app.mod_github_access.controllers import mod_github

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(share_access_module)
app.register_blueprint(mod_research_objects)
app.register_blueprint(mod_discos)
app.register_blueprint(mod_github)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

file_path = os.path.join(app.root_path, conf.TMP_DIR)
if not os.path.exists(file_path):
    os.makedirs(file_path)
