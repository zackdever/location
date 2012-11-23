from pymongo import Connection
import config

def connect():
    conn = Connection(config.DB_HOST, config.DB_PORT)
    db = conn[config.DATABASE]
    db.users.ensure_index('username', unique=True)
    return db
