from flask import render_template
from flask.ext.login import current_user

from uber.ui import ui

@ui.route('/')
def index():
    if current_user.is_authenticated():
        pass
    return render_template('index.html')
