from functools import wraps

from bson.objectid import ObjectId
from flask import request, abort

from uber.api.errors import bad_request

def ensure_json_content_type(f):
    """Ensure the 'Content-Type' header is 'application/json'.

    Wraps views. If the check fails, returns a 400 bad request.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        ctype = request.headers['Content-Type']
        if ctype != 'application/json':
            return bad_request("Expected 'application/json', got '%s'" % ctype)
        return f(*args, **kwargs)
    return decorated

def get_or_404(objects, id):
    """Get the object with id from objects, or abort with a 404."""
    if not ObjectId.is_valid(id):
        abort(404)

    oid = ObjectId(id)
    obj = objects.find_one(oid)

    if not obj:
        abort(404)

    return obj
