from pymongo import Connection
import config

def connect():
    """Connect to the database and ensure indexes."""

    conn = Connection(config.DB_HOST, config.DB_PORT)
    db = conn[config.DATABASE]
    db.users.ensure_index('username', unique=True)
    return db
