from bson.objectid import ObjectId
from functools import wraps
from flask import request, jsonify, url_for, Response
from uber import app
from uber.models import Location

def check_content_type(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST' or request.method == 'PUT':
            ctype = request.headers['Content-Type']
            if ctype != 'application/json':
                return bad_request("Expected 'application/json', got '%s'" % ctype)
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return 'you see a map.\n'

@app.route('/locations/', methods = ['GET', 'POST'])
@check_content_type
def locations():
    if request.method == 'POST':
        location = Location.parse_json(request.json, has_id=False)
        if not location: return bad_request()

        app.db.locations.insert(location)
        location = Location.flatten(location)

        resp = jsonify(location)
        resp.status_code = 201
        resp.headers['Location'] = url_for('locations') + location['id']
        return resp

    # GET /locations/ - show all
    return jsonify({
        'locations' : [Location.flatten(loc) for loc in app.db.locations.find()]
    })

@app.errorhandler(404)
@app.route('/locations/<id>', methods = ['GET', 'PUT', 'DELETE'])
@check_content_type
def location(id):
    if not ObjectId.is_valid(id):
        return bad_request("'id' is either missing or is of the wrong type")

    # ok, the id's format is valid, but does it exist?
    oid = ObjectId(id)
    location = app.db.locations.find_one({ '_id' : oid })
    if not location: return not_found()

    if request.method == 'PUT':
        updated = Location.parse_json(request.json, has_id=True)
        if not updated or updated['_id'] != oid: return bad_request()

        app.db.locations.save(updated)
        return jsonify(Location.flatten(updated))
    elif request.method == 'DELETE':
        app.db.locations.remove({ '_id' : oid })
        return Response(status=204, content_type='application/json')

    # GET /location/<id> - show location with id
    return jsonify(Location.flatten(location))

### Error handlers
@app.errorhandler(400)
def bad_request(message=None):
    message = message if message != None else request.url
    resp = jsonify({
        'error': {
            'code': 400,
            'message': 'Bad Request: ' + message,
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
            'message': 'Not Found: ' + message,
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
