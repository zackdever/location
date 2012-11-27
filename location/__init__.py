import os

from flask import Flask
from flask_sslify import SSLify

from location import db
from location.api import api
from location.auth import auth, setup_auth
from location.ui import ui

# create a Flask app, force SSL when debug is False
app = Flask(__name__, static_folder='./ui/static')
app.config.from_pyfile('config.py')

# set the below env var to your config file path to load custom configs
CONFIG_FILE_VAR = 'LOCATION_CONFIG'

if os.environ.get(CONFIG_FILE_VAR) is not None:
    app.config.from_envvar(CONFIG_FILE_VAR)

# setup
app.db = db.connect()
setup_auth(app)
SSLify(app, subdomains=True)

# register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)
app.register_blueprint(ui)

def run_server():
    """Starts the server, as you might expect."""
    app.run(host=app.config['HOST'], port=app.config['PORT'])
