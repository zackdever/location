import json
import unittest

import location

class RequestBaseTest(unittest.TestCase):
    """Base test case for any test involving request."""

    test_location = {
                'address' : '123 Main St.',
                'lat'     : '127.0',    # forgive numbers coming as strings
                'lng'     : -42,
                'name'    : 'nowhere',
                }

    def setUp(self):
        """Create a new app, test client, and database for each test."""
        self.app = location.init_app(db_name='location_test')
        self.app.config['TESTING'] = True

        self.test_user = { 'username': 'foo', 'password': 'jklshwensldkjhsaidfhosjd' }

        self.client = self.app.test_client()

    def tearDown(self):
        """Remove the test database."""
        self.app.db.connection.drop_database(self.app.db.name)

    def register(self, username, password):
        """Register a user with the given username and password."""
        return self.client.post('/register', data=locals(), follow_redirects=True)

    def login(self, username, password):
        """Login a user with the given username and password."""
        return self.client.post('/login', data=locals(), follow_redirects=True)

    def logout(self):
        """Logout the user, if any."""
        return self.client.get('/logout', follow_redirects=True)

    def login_test_user(self):
        """Create a dummy test user and log it in."""
        self.register(self.test_user['username'], self.test_user['password'])

    def json_args(self, data=None):
        """Make a application/json request."""
        return { 'content_type': 'application/json', 'data': json.dumps(data) }

    def relative_location(self, resp):
        """Given a Response with a Location header, parse the relative uri."""
        return 'api%s' % resp.headers['Location'].split('api')[1]

