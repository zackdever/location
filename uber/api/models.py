from bson.errors import InvalidId
from bson.objectid import ObjectId
#from flask import current_app
from pymongo.errors import OperationFailure

class Location:
    #objects = current_app.db.locations

    @staticmethod
    def flatten(data):
        data['id'] = str(data['_id'])
        del data['_id']
        del data['owner']
        return data
        pass

    @staticmethod
    def from_json(data, required_id=None):
        if data is None: return None

        # ensure all data is there, though we don't care who they say the owner is
        try:
            parsed = {
                'address' : data.pop('address'),
                'lat'     : float(data.pop('lat')),
                'lng'     : float(data.pop('lng')),
                'name'    : data.pop('name'),
            }

            if required_id is not None:
                if not ObjectId.is_valid(id): return None
                parsed['_id'] = ObjectId(data.pop('id'))
                if parsed['_id'] != required_id: return None

        except (KeyError, ValueError, TypeError, InvalidId):
            return None

        # check that there is no extra data, and that address and name aren't empty
        if (len(data) != 0 or
            len(parsed['address']) == 0 or
            len(parsed['name']) == 0):
            return None

        return parsed
