from functools import wraps

from bson.objectid import ObjectId
from flask import request, abort

from uber.api.errors import bad_request

def ensure_json_content_type(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ctype = request.headers['Content-Type']
        if ctype != 'application/json':
            return bad_request("Expected 'application/json', got '%s'" % ctype)
        return f(*args, **kwargs)
    return decorated

def get_or_404(objects, id):
    if not ObjectId.is_valid(id):
        abort(404)

    oid = ObjectId(id)
    obj = objects.find_one(oid)

    if not obj:
        abort(404)

    return obj
