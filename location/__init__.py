import os

from flask import Flask
from flask_sslify import SSLify

from location import db
from location.api import api
from location.auth import auth, setup_auth
from location.ui import ui

def init_app(db_name=None):
    """Initialize the app.

    Because the database name has to be set before the app inits,
    we allow it to be passed in outside of configs, because we can't
    set it on app.config['DATABASE'] before we actually have an app.

    This is mainly for testing, because it could be set via env vars,
    but we don't want the test to override any env vars that are already set.
    """

    # create a Flask app, force SSL when debug is False
    app = Flask(__name__, static_folder='./ui/static')
    app.config.from_pyfile('config.py')

    # load custom config file
    custom_config = app.config['CUSTOM_CONFIG_PATH']
    if os.environ.get(custom_config) is not None:
        app.config.from_envvar(custom_config)

    # setup
    app.db = db.connect(db_name)
    setup_auth(app)
    SSLify(app, subdomains=True)

    # register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth)
    app.register_blueprint(ui)

    return app

def run_server():
    """Starts the server, as you might expect."""
    app = init_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'])
