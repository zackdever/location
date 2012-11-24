from flask import current_app, render_template
from flask.ext.login import login_required

from uber.ui import ui

@ui.route('/')
@login_required
def index():
    return render_template('index.html',
                maps_api_key=current_app.config['MAPS_API_KEY'])
