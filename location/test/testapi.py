#!/usr/bin/env python

import json
import unittest

from location.test import RequestBaseTest

class TestAPI(RequestBaseTest):
    """Test CRUD operations on Location API."""

    def test_get_collection(self):
        """Test that a JSON list of Locations is returned."""
        self.login_test_user()

        # should have an empty list
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json.loads(resp.data)), 0)

        # create a location
        resp = self.client.post('/api/locations/', **self.json_args(data=self.test_location))
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 1)

        # create another location
        resp = self.client.post('/api/locations/', **self.json_args(data=self.test_location))
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 2)

    def test_post(self):
        """Test the creation of a new Location."""
        self.login_test_user()

        location = {
                'address' : '42 Loop',
                'lat'     :  100.91,
                'lng'     :  23.3,
                'name'    : 'somewhere',
                }

        # create a new location
        resp = self.client.post('/api/locations/', **self.json_args(data=location))
        self.assertEqual(resp.status_code, 201)
        relative = self.relative_location(resp)
        resp = self.client.get(relative, **self.json_args())

        # check that the data is correct
        actual = json.loads(resp.data)
        self.assertEqual(actual['address'], location['address'])
        self.assertEqual(actual['lat'], location['lat'])
        self.assertEqual(actual['lng'], location['lng'])
        self.assertEqual(actual['name'], location['name'])
        self.assertIsNotNone(actual['id'])

    def test_get_single(self):
        """Test that we can get a single Location."""
        self.login_test_user()

        # create a new location
        resp = self.client.post('/api/locations/', **self.json_args(data=self.test_location))

        # make sure we can get it back
        relative = self.relative_location(resp)
        resp = self.client.get(relative, **self.json_args())
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        """Test updates on Location properties."""
        self.login_test_user()

        # create the normal test location
        resp = self.client.post('/api/locations/', **self.json_args(data=self.test_location))
        relative = self.relative_location(resp)

        # change the name
        updated = json.loads(resp.data).copy()
        updated['name'] = 'some place special'

        # put the changes on the server
        resp = self.client.put(relative, **self.json_args(data=updated))
        actual = json.loads(resp.data).copy()

        # verify that they saved
        self.assertEqual(actual['address'], updated['address'])
        self.assertEqual(actual['lat'], updated['lat'])
        self.assertEqual(actual['lng'], updated['lng'])
        self.assertEqual(actual['name'], updated['name'])
        self.assertIsNotNone(actual['id'])

        self.assertNotEqual(actual['name'], self.test_location['name'])


    def test_delete(self):
        """Test tha deletes do in fact remove the Location."""
        self.login_test_user()

        # start at 0
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 0)

        # add one
        resp = self.client.post('/api/locations/', **self.json_args(data=self.test_location))
        one = self.relative_location(resp)
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 1)
        resp = self.client.get(one, **self.json_args())
        self.assertEqual(resp.status_code, 200)

        # add another
        resp = self.client.post('/api/locations/', **self.json_args(data=self.test_location))
        two = self.relative_location(resp)
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 2)
        resp = self.client.get(two, **self.json_args())
        self.assertEqual(resp.status_code, 200)

        # delete the first location
        resp = self.client.delete(one, **self.json_args())
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 1)
        resp = self.client.get(one, **self.json_args())
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get(two, **self.json_args())
        self.assertEqual(resp.status_code, 200)

        # delete the second location
        resp = self.client.delete(two, **self.json_args())
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get('/api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 0)
        resp = self.client.get(two, **self.json_args())
        self.assertEqual(resp.status_code, 404)

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
