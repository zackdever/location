import os

from flask import Flask

from location import db
from location.api import api
from location.auth import auth, setup_auth
from location.ui import ui

# create a Flask app
app = Flask(__name__, static_folder='./ui/static')
app.config.from_pyfile('config.py')

# set the below env var to your config file path to load custom configs
CONFIG_FILE_VAR = 'LOCATION_CONFIG'

if os.environ.get(CONFIG_FILE_VAR) is not None:
    app.config.from_envvar(CONFIG_FILE_VAR)

# setup
app.db = db.connect()
setup_auth(app)

# register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)
app.register_blueprint(ui)
