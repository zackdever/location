from flask import render_template, Blueprint
from flask.ext.login import current_user

ui = Blueprint('ui', __name__, template_folder='templates')

@ui.route('/')
def index():
    if current_user.is_authenticated():
        pass
    return render_template('index.html')
