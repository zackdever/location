from functools import wraps

from bson.objectid import ObjectId
from flask import Blueprint, current_app, request, jsonify, url_for, Response
from flask.ext.login import login_required
from pymongo.errors import OperationFailure

from uber.api.location import Location
from uber.api.errors import bad_request, not_found, server_error

api = Blueprint('api', __name__)

def check_content_type(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST' or request.method == 'PUT':
            ctype = request.headers['Content-Type']
            if ctype != 'application/json':
                return bad_request("Expected 'application/json', got '%s'" % ctype)
        return f(*args, **kwargs)
    return decorated

@api.route('/locations/', methods = ['GET', 'POST'])
@login_required
@check_content_type
def locations():
    if request.method == 'POST':
        location = Location.parse_json(request.json, has_id=False)
        if not location: return bad_request()

        try:
            current_app.db.locations.insert(location, safe=True)
            location = Location.flatten(location)

            resp = jsonify(location)
            resp.status_code = 201
            resp.headers['Location'] = url_for('.locations') + location['id']
            return resp
        except OperationFailure as e:
            return server_error(str(e))

    # GET - show all
    return jsonify({
        'locations': [Location.flatten(loc) for loc in current_app.db.locations.find()]
    })

@api.route('/locations/<id>', methods = ['GET', 'PUT', 'DELETE'])
@login_required
@check_content_type
def location(id):
    if not ObjectId.is_valid(id):
        return bad_request("'id' is either missing or is of the wrong type")

    # ok, the id's format is valid, but does it exist?
    oid = ObjectId(id)
    location = current_app.db.locations.find_one(oid)
    if not location: return not_found()

    if request.method == 'PUT':
        updated = Location.parse_json(request.json, has_id=True)
        if not updated or updated['_id'] != oid: return bad_request()

        try:
            current_app.db.locations.save(updated, safe=True)
            return jsonify(Location.flatten(updated))
        except OperationFailure as e:
            return server_error(str(e))
    elif request.method == 'DELETE':
        try:
            current_app.db.locations.remove({ '_id' : oid }, safe=True)
            return Response(status=204, content_type='application/json')
        except OperationFailure as e:
            return server_error(str(e))

    # GET - show location with id
    return jsonify(Location.flatten(location))

