from flask import Flask
from flask.ext.login import LoginManager

from uber import db

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.db = db.connect()
app.db.users.ensure_index('username', unique=True)

app.login_manager = LoginManager()
app.login_manager.setup_app(app)

import uber.views
