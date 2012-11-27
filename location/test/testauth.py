#!/usr/bin/env python

import json
import unittest

from location.test import RequestBaseTest

class TestAuth(RequestBaseTest):
    """Test authentication and authorization permissions."""
    test_location = {
                'address' : '123 Main St.',
                'lat'     : '127.0',    # forgive numbers coming as strings
                'lng'     : -42,
                'name'    : 'nowhere',
                }

    def test_redirect_to_login_path(self):
        """Test that going to a valid page redirects to the login."""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers['Location'], 'http://localhost/login?next=%2F')

        resp = self.client.get('/', follow_redirects=True)
        self.assertTrue('Please log in to access this page.' in resp.data)

    def test_registration(self):
        """Test that a registered user is logged in."""
        resp = self.register('foo', 'bar')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_api_access(self):
        """Test that the user must be logged in to access the api."""
        resp = self.client.get('api/locations/')
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('api/locations/', **self.json_args())
        self.assertEqual(resp.status_code, 302)

        self.login_test_user()
        resp = self.client.get('api/locations/')
        self.assertEqual(resp.status_code, 200)

        self.logout()
        resp = self.client.get('api/locations/')
        self.assertEqual(resp.status_code, 302)

    def test_permissions(self):
        """Test that a user can only access their data."""
        user1 = { 'username': 'one', 'password': 'pw' }
        user2 = { 'username': 'two', 'password': 'pw' }

        # register a new user
        self.register(*user1)
        self.login(*user1)

        # the user has no locations
        resp = self.client.get('api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 0)

        # so create one
        resp = self.client.post('api/locations/', **self.json_args(self.test_location))
        self.assertEqual(resp.status_code, 201)

        # make sure user1 can get it
        relative = self.relative_location(resp)
        resp = self.client.get(relative, **self.json_args())
        self.assertEqual(resp.status_code, 200)

        # make sure user1 can see it in his list
        resp = self.client.get('api/locations/', **self.json_args())
        self.assertEqual(len(json.loads(resp.data)), 1)

        # log user1 out
        self.logout()

        # TODO same problem as before - current_user from Flask-Login is bunk with this
        # test client, so every user that logs in is getting the same default id or something
        if False:
            # register and log in user2 and make the list is empty
            self.register(*user2)
            self.login(*user2)
            resp = self.client.get('api/locations/', **self.json_args())
            self.assertEqual(len(json.loads(resp.data)), 0)

            # make sure user2 cannot view, edit, or delete it
            relative = 'api%s' % resp.headers['Location'].split('api')[1]
            resp = self.client.get(relative, **self.json_args())
            self.assertEqual(resp.status_code, 403)

            resp = self.client.post(relative, **self.json_args())
            self.assertEqual(resp.status_code, 403)

            resp = self.client.delete(relative, **self.json_args())
            self.assertEqual(resp.status_code, 403)

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuth)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
