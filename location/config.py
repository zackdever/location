"""
All configs should go here.

Check __init__.py on how to easily load a custom local config file.

For git-only deploy systems, this file checks for individual env vars as well.
"""

from os import environ

debug = environ.get('LOCATION_DEBUG')
DEBUG = True if debug is None else debug

# not name-spaced, b/c heroku requires 'PORT', and that's good enough for now
PORT = int(environ.get('PORT') or 5000)
HOST = environ.get('LOCATION_HOST') or '127.0.0.1'

# database
DB_HOST = environ.get('LOCATION_DB_HOST') or 'localhost'
DB_PORT = int(environ.get('LOCATION_DB_PORT') or 27017)
DB_USER = environ.get('LOCATION_DB_USER') or None
DB_PW = environ.get('LOCATION_DB_PW') or None
DATABASE = environ.get('LOCATION_DB') or 'location'

# Google Maps API
# https://developers.google.com/maps/documentation/javascript/tutorial#api_key
MAPS_API_KEY = environ.get('LOCATION_MAPS_API_KEY') or ''

# you should change this, you could generate a new one with:
#      import os
#      os.urandom(24)
SECRET_KEY = environ.get('LOCATION_SECRET_KEY') or """LK\xce6\xac"\x05R\xe1\xaa\x85\x8ctK\xc2\n\xef\x0f\x84\xf7`&\x1d7"""

# The file path to a custom config file
CUSTOM_CONFIG_PATH = 'LOCATION_CONFIG'
