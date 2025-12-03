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
    r_fv_numerator INTEGER,
    r_fv_denominator INTEGER,
    r_sphere REAL,
    r_cylinder REAL,
    r_axis INTEGER,
    r_prism REAL,
    r_base TEXT,
    r_va TEXT,
    r_add_read REAL,
    r_add_int REAL,
    r_add_bif REAL,
    r_add_mul REAL,
    r_high REAL,
    l_fv_numerator INTEGER,
    l_fv_denominator INTEGER,
    l_sphere REAL,
    l_cylinder REAL,
    l_axis INTEGER,
    l_prism REAL,
    l_base TEXT,
    l_va TEXT,
    l_add_read REAL,
    l_add_int REAL,
    l_add_bif REAL,
    l_add_mul REAL,
    l_high REAL,
    pupil_distance REAL,
    dominant_eye TEXT,
    iop TEXT,
    glasses_role TEXT,
    lenses_material TEXT,
    lenses_diameter REAL,
    segment_diameter REAL,
    lenses_manufacturer TEXT,
    lenses_color TEXT,
    catalog_num TEXT,
    frame_manufacturer TEXT,
    frame_supplier TEXT,
    frame_model TEXT,
    frame_size TEXT,
    frame_bar_length TEXT,
    frame_color TEXT,
    diagnosis TEXT,
    notes TEXT,

    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
    );
    """
    conn.execute(REFRACTION_TEST_SCHEMA_SQL)
    conn.commit()


con = db.get_connection()
create_tables(con)
print("Created customers table successfully!")
