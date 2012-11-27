from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask.ext.login import current_user

class Location:
    """Static methods to convert location JSON <-> Python.

    A location is used to save a named address with corresponding lat/lng.

    Location:
        id (_id in Python)
        address
        lat
        lng
        name
        owner (Python only)

    Python includes an owner id, and id's are bson ObjectId objects.
    JSON does not have an owner id, and the id's are strings.
    """


    @staticmethod
    def flatten(data):
        """Convert from Python to JSON."""
        flat = data.copy()
        flat['id'] = str(data['_id'])
        del flat['_id']

        # don't make owner public
        del flat['owner']
        return flat

    @staticmethod
    def from_json(data, required_id=None):
        """Convert from JSON to Python.

        If the data is a new object to be created, there is no required_id.
        If it is supplied, ensure that it matches the id in data.
        Also does some basic type checking.

        required_id: the id that data should include.
        returns: converted data as a dict, or None if there was a problem.
        """

        # assume current user is owner
        if data is None: return None

        try:
            parsed = {
                'address' : data.pop('address'),
                'lat'     : float(data.pop('lat')),
                'lng'     : float(data.pop('lng')),
                'name'    : data.pop('name'),
                'owner'   : current_user.id
            }

            # check that id is there and that it matches
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
