from flask import render_template
from flask.ext.login import login_required

from uber.ui import ui

@ui.route('/')
@login_required
def index():
    return render_template('index.html')
