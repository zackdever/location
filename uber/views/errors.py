from flask import request, jsonify

from uber import app

# TODO only return json error if on api route, which should be set in settings
@app.errorhandler(400)
def bad_request(message=None):
    message = message if message != None else request.url
    resp = jsonify({
        'error': {
            'code': 400,
            'message': 'Bad Request: %s' % message,
        }
    })

    resp.status_code = 400
    return resp

@app.errorhandler(404)
def not_found(message=None):
    message = message if message != None else request.url
    resp = jsonify({
        'error': {
            'code': 404,
            'message': 'Not Found: %s' % message,
        }
    })

    resp.status_code = 404
    return resp

@app.errorhandler(500)
def server_error(message=None):
    message = message if message != None else "It's me, not you."
    resp = jsonify({
        'error': {
            'code': 500,
            'message':  message,
        }
    })

    resp.status_code = 404
    return resp
