from flask import Blueprint

api = Blueprint('api', __name__)

import location.api.views
