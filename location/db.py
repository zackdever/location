from pymongo import Connection

# While it may be more 'correct' to import app.config,
# I prefer this b/c it really doesn't have anything to do with Flask.
# This way it's that much easier to use in other Python projects.
import config

def connect():
    """Connect to the database and ensure indexes."""

    conn = Connection(config.DB_HOST, config.DB_PORT)
    db = conn[config.DATABASE]

    if config.DB_USER and config.DB_PW:
        db.authenticate(config.DB_USER, config.DB_PW)

    db.users.ensure_index('username', unique=True)
    return db
