from flask import Flask
from uber import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.db = db.connect()

import uber.views
