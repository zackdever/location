from bson.errors import InvalidId
from bson.objectid import ObjectId

class Location:
    @staticmethod
    def parse_json(data, has_id):
        # ensure all the data is there
        try:
            parsed = {
                'address' : data.pop('address'),
                'lat'     : float(data.pop('lat')),
                'lng'     : float(data.pop('lng')),
                'name'    : data.pop('name')
            }
        except (KeyError, ValueError):
            return None

        if has_id:
            try:
                parsed['id'] = ObjectId(data.pop('id'))
            except (TypeError, InvalidId):
                return None

        # check that there is no extra data, and that address and name aren't empty
        if len(data) != 0 or len(parsed['address']) == 0 or len(parsed['name']) == 0:
            return None

        return parsed

    @staticmethod
    def flatten(data):
        data['id'] = str(data['id'])
        return data