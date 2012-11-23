from bson.errors import InvalidId
from bson.objectid import ObjectId

class Location:
    @staticmethod
    def parse_json(data, has_id):
        # ensure all data is there, though we don't care who they say the owner is
        try:
            parsed = {
                'address' : data.pop('address'),
                'lat'     : float(data.pop('lat')),
                'lng'     : float(data.pop('lng')),
                'name'    : data.pop('name'),
            }

            if has_id:
                parsed['_id'] = ObjectId(data.pop('id'))

        except (KeyError, ValueError, TypeError, InvalidId):
            return None

        # check that there is no extra data, and that address and name aren't empty
        if (len(data) != 0 or
            len(parsed['address']) == 0 or
            len(parsed['name']) == 0):
            return None

        return parsed

    @staticmethod
    def flatten(data):
        data['id'] = str(data['_id'])
        del data['_id']
        del data['owner']
        return data
