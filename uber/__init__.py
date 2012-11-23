from flask import Flask

from uber import db
from uber.api import api
from uber.auth import auth, setup_auth
from uber.ui import ui

app = Flask(__name__, static_folder='./ui/static')
app.config.from_pyfile('config.py')

app.db = db.connect()
setup_auth(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)
app.register_blueprint(ui)
