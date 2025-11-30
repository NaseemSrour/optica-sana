import sqlite3
from db_config import DATABASE_PATH

_conn = None


def get_connection():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DATABASE_PATH)
        _conn.row_factory = sqlite3.Row  # dict-like rows for convenience
    return _conn
