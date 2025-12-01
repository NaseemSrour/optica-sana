# SQL for initial creation
import connection as db


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssn INTEGER NOT NULL,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            phone TEXT,
            town TEXT,
            notes TEXT
        )
    """)
    conn.commit()


con = db.get_connection()
create_tables(con)
print("Created customers table successfully!")
