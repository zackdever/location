from flask import render_template
from flask.ext.login import current_user

from uber import app

@app.route('/')
def index():
    if current_user.is_authenticated():
        pass
    return render_template('index.html')
