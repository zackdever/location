from bson.objectid import ObjectId
from flask import Blueprint, current_app
from flask.ext.login import LoginManager

from uber.auth.models import User

auth = Blueprint('auth', __name__)

# Using Flask-Login to handle login/logout/sessions.
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # must be absolute, not relative

def setup_auth(app):
    """Required by Flask-Login. Sets up app with the login manager."""
    login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    """Required by Flask-Login. Creates a Flask-Login compliant User."""
    user = current_app.db.users.find_one(ObjectId(userid))
    return User(user['username'], user['_id']) if user else None

import uber.auth.views
