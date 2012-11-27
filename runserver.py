#!/usr/bin/env python

"""
Starts the server, as you might expect.
"""

from location import app

app.run(host=app.config['HOST'], port=app.config['PORT'])
