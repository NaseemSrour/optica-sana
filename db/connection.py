import sqlite3
from db.db_config import DATABASE_PATH  # Import path is relative to where we're running the main.py file from (root),
# even though here it's inside the connection.py file.
# So instead of "from db_config" use "from db.db_config" because it's relative
# to the main.py file and not this file (although it's inside this file connection.py).

_conn = None


def get_connection():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DATABASE_PATH)
        _conn.row_factory = sqlite3.Row  # dict-like rows for convenience
    return _conn
