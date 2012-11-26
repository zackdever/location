from flask import request, jsonify
from pymongo.errors import OperationFailure

from uber.api import api

@api.errorhandler(400)
def bad_request(message=None):
    """400 Bad Request JSON response."""
    return _make_json_error(400, 'Bad Request', message)

@api.errorhandler(401)
def unauthorized(message=None):
    """401 Unauthorized JSON response."""
    return _make_json_error(401, 'Unathorized: %s' % request.url, message)

@api.errorhandler(403)
def forbidden(message=None):
    """403 Forbidden JSON response."""
    return _make_json_error(403, 'Forbidden: %s' % request.url, message)

@api.errorhandler(404)
def not_found(message=None):
    """404 Not Found JSON response."""
    return _make_json_error(404, 'Not Found: %s' % request.url, message)

# it's not possible to register a 500 error handler
# on a Blueprint as of writing
def server_error(message=None):
    """500 Internal Server Error JSON response."""
    return _make_json_error(500, 'Internal Server Error', message)

def _make_json_error(code, default_message, message=None):
    """Make a application/json response with provided code and messages.

    code: HTTP response code
    default_message: used if no message is supplied.
    message: returned as part of the response body.
    """

    message = default_message if message is None else message
    resp = jsonify({
        'error': {
            'code': code,
            'message':  str(message),
        }
    })

    resp.status_code = code
    return resp

