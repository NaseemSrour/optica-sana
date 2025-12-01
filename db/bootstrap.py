import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def ensure_data_folder():
    data_dir = os.path.join(BASE_DIR)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"[BOOTSTRAP] Created folder: {data_dir}")

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return f.read()

def initialize_database():
    ensure_data_folder()

    should_create = not os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema_sql = load_schema()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

    if should_create:
        print(f"[BOOTSTRAP] Created new SQLite database at: {DB_PATH}")
    else:
        print(f"[BOOTSTRAP] Verified schema on existing database at: {DB_PATH}")

if __name__ == "__main__":
    initialize_database()
