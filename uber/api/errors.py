from flask import request, jsonify
from pymongo.errors import OperationFailure

from uber.api import api

@api.errorhandler(400)
def bad_request(message=None):
    return _make_json_error(400, 'Bad Request', message)

@api.errorhandler(401)
def unauthorized(message=None):
    return _make_json_error(401, 'Unathorized: %s' % request.url, message)

@api.errorhandler(403)
def forbidden(message=None):
    return _make_json_error(403, 'Forbidden: %s' % request.url, message)

@api.errorhandler(404)
def not_found(message=None):
    return _make_json_error(404, 'Not Found: %s' % request.url, message)

# it's not possible to register a 500 error handler on a Blueprint as of writing
def server_error(message=None):
    return _make_json_error(500, 'Internal Server Error', message)

def _make_json_error(code, default_message, message=None):
    message = default_message if message is None else message
    resp = jsonify({
        'error': {
            'code': code,
            'message':  str(message),
        }
    })

    resp.status_code = code
    return resp

