from flask import request, jsonify

from uber.auth import auth

@auth.errorhandler(400)
def bad_request(message=None):
    message = message if message != None else 'Bad Request: %s' % request.url
    resp = jsonify({
        'error': {
            'code': 400,
            'message': message
        }
    })

    resp.status_code = 400
    return resp

@auth.errorhandler(404)
def not_found(message=None):
    message = message if message != None else 'Not Found: %s' % request.url
    resp = jsonify({
        'error': {
            'code': 404,
            'message': message,
        }
    })

    resp.status_code = 404
    return resp

# AssertionError: It is currently not possible to register a 500
# internal server error on a per-blueprint level.
#@auth.errorhandler(500)
def server_error(message=None):
    message = message if message != None else "It's me, not you."
    resp = jsonify({
        'error': {
            'code': 500,
            'message':  message,
        }
    })

    resp.status_code = 500
    return resp
