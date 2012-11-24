from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask.ext.login import current_user

class Location:
    #objects = current_app.db.locations

    @staticmethod
    def flatten(data):
        data['id'] = str(data['_id'])
        del data['_id']

        # don't make owner public
        del data['owner']
        return data

    @staticmethod
    def from_json(data, required_id=None):
        "assume current user is owner"
        if data is None: return None

        try:
            parsed = {
                'address' : data.pop('address'),
                'lat'     : float(data.pop('lat')),
                'lng'     : float(data.pop('lng')),
                'name'    : data.pop('name'),
                'owner'   : current_user.id
            }

            if required_id is not None:
                id = data.pop('id')
                if not ObjectId.is_valid(id):
                    return None

                parsed['_id'] = ObjectId(id)
                if id != required_id:
                    return None

        except (KeyError, ValueError, TypeError, InvalidId):
            return None

        # check that there is no extra data, and that address isn't empty
        if (len(data) != 0 or len(parsed['address']) == 0):
            return None

        return parsed
