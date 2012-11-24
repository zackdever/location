import json

from flask import abort, jsonify, request, Response, url_for
from flask import current_app as app
from flask.views import MethodView
from flask.ext.login import current_user, login_required
from pymongo.errors import OperationFailure

from uber.api import api
from uber.api.errors import server_error
from uber.api.utils import ensure_json_content_type, get_or_404
from uber.api.models import Location

class LocationAPI(MethodView):
    def _authorize_location_by_id(self, id):
        location = get_or_404(app.db.locations, id)
        if location['owner'] != current_user.id:
            abort(403)
        return location

    def _location_from_json_or_400(self, data, required_id=None):
        location = Location.from_json(data, required_id=required_id)

        if not location:
            abort(400)

        return location

    @login_required
    def get(self, id=None):
        if id is not None:
            location = self._authorize_location_by_id(id)
            return jsonify(Location.flatten(location))

        # can't use jsonify http://flask.pocoo.org/docs/security/#json-security
        locations = [Location.flatten(loc) for loc in
                app.db.locations.find({ 'owner': current_user.id })]
        resp = Response(content_type='application/json')
        resp.data = json.dumps(locations)
        return resp

    @login_required
    @ensure_json_content_type
    def post(self):
        location = self._location_from_json_or_400(request.json)
        try:
            app.db.locations.insert(location, safe=True)
            location = Location.flatten(location)

            resp = jsonify(location)
            resp.status_code = 201
            resp.headers['Location'] = url_for('.location_view',
                    _method='GET', id=location['id'])
            return resp
        except OperationFailure as e:
            return server_error(str(e))

    @login_required
    def delete(self, id):
        location = self._authorize_location_by_id(id)
        try:
            app.db.locations.remove(location['_id'], safe=True)
            return Response(status=204, content_type='application/json')
        except OperationFailure as e:
            return server_error(str(e))

    @login_required
    @ensure_json_content_type
    def put(self, id):
        self._authorize_location_by_id(id)
        updated = self._location_from_json_or_400(request.json, required_id=id)
        try:
            app.db.locations.save(updated, safe=True)
            return jsonify(Location.flatten(updated))
        except OperationFailure as e:
            return server_error(str(e))

location_view = LocationAPI.as_view('location_view')
api.add_url_rule('/locations/', view_func=location_view,
                    methods=['GET', 'POST'])
api.add_url_rule('/locations/<id>', view_func=location_view,
                    methods=['GET', 'PUT', 'DELETE'])
