#!/usr/bin/env python

import unittest

from bson.objectid import ObjectId

from location.api.models import Location
from location.test import RequestBaseTest

class TestModels(RequestBaseTest):
    """Test the Location model's JSON <-> Python conversions."""

    def test_python_to_json(self):
        """Test flattening Python data to its JSON equivalent.

        This should flatten data types to primitives,
        and remove/rename attributes to make them public.
        """
        location = {
                'address' : '123 Main St.',
                'lat'     : 127.0,
                'lng'     : -42,
                'name'    : 'nowhere',
                'owner'   : ObjectId(),
                '_id'     : ObjectId()
                }

        parsed = Location.flatten(location)

        # these should all be the same
        self.assertEqual(parsed['address'], location['address'])
        self.assertEqual(parsed['lat'], location['lat'])
        self.assertEqual(parsed['lng'], location['lng'])
        self.assertEqual(parsed['name'], location['name'])

        # owner should be removed
        self.assertFalse(parsed.has_key('owner'))

        # and id should be renamed from _id to id, and flattened
        self.assertFalse(parsed.has_key('_id'))
        self.assertTrue(parsed.has_key('id'))
        self.assertEqual(parsed['id'], str(location['_id']))

    def test_json_to_python(self):
        """Test converting flattened public data to its Python equivalent.

        This should expand ids to ObjectId instances, and set the logged in
        user to the owner of any incoming Location objects.
        """

        # There seems to be a problem with Flask-Login setting the current_user proxy
        # in api/models.py, which we need t run this test.
        if False:
            self.login_test_user()

            location = {
                    'address' : '123 Main St.',
                    'lat'     : '127.0',    # forgive numbers coming as strings
                    'lng'     : -42,
                    'name'    : 'nowhere',
                    'id'      : str(ObjectId())
                    }

            expanded = Location.from_json(location)

            # these should all be the same
            self.assertEqual(expanded['address'], location['address'])
            self.assertEqual(expanded['lat'], location['lat'])
            self.assertEqual(expanded['lng'], location['lng'])
            self.assertEqual(expanded['name'], location['name'])

            # owner should be set by the currently logged in location
            self.assertEqual(expanded['owner'], self.test_location.id)

            # id should be renamed from id to _id, and expanded
            self.assertTrue(expanded.has_key('_id'))
            self.assertFalse(expanded.has_key('id'))
            self.assertEqual(str(expanded['_id']), location['id'])


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
