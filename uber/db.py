from pymongo import Connection
import config

def connect():
    conn = Connection(config.DB_HOST, config.DB_PORT)
    return conn[config.DATABASE]
