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

    REFRACTION_TEST_SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS refraction_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        exam_date TEXT NOT NULL,
        examiner TEXT,

        r_sphere REAL,
        r_cylinder REAL,
        r_axis INTEGER,
        r_add REAL,
        r_va TEXT,

        l_sphere REAL,
        l_cylinder REAL,
        l_axis INTEGER,
        l_add REAL,
        l_va TEXT,

        pupil_distance REAL,
        diagnosis TEXT,
        notes TEXT,

        FOREIGN KEY (customer_id)
            REFERENCES customers(id)
            ON DELETE CASCADE
    );
    """
    conn.execute(REFRACTION_TEST_SCHEMA_SQL)
    conn.commit()


con = db.get_connection()
create_tables(con)
print("Created customers table successfully!")
