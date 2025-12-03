import sqlite3
import pytest
from datetime import datetime

from db.models import RefractionTest
from db.utils import datetime_to_text, text_to_datetime

from db.repositories.refraction_repo import RefractionRepo


# ------------------------------------------------------
# Helper: create a fresh in-memory DB with schema
# ------------------------------------------------------
def setup_in_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    conn.execute("""
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
    )
    """)

    conn.commit()
    return conn


# ------------------------------------------------------
# Helper: sample refraction test object
# ------------------------------------------------------
def sample_test(customer_id=1):
    return RefractionTest(
        id=None,
        customer_id=5,

        # --- Exam metadata ---
        exam_date=datetime(2025, 5, 9, 14, 30),
        examiner="Sanaa",

        # --- Right Eye (OD) ---
        r_fv_numerator=6,
        r_fv_denominator=9,
        r_sphere=-2.25,
        r_cylinder=-1.00,
        r_axis=170,
        r_prism=0.5,
        r_base="IN",
        r_va="6/6",
        r_add_read=1.25,
        r_add_int=0.75,
        r_add_bif=1.50,
        r_add_mul=1.25,
        r_high=None,  # Unused or unknown field

        # --- Left Eye (OS) ---
        l_fv_numerator=6,
        l_fv_denominator=12,
        l_sphere=-1.75,
        l_cylinder=-0.50,
        l_axis=10,
        l_prism=0.25,
        l_base="OUT",
        l_va="6/7.5",
        l_add_read=1.25,
        l_add_int=0.75,
        l_add_bif=1.50,
        l_add_mul=1.25,
        l_high=None,

        # --- Symptoms / Notes ---
        pupil_distance=63.5,  # PD (usually 54–74mm)
        dominant_eye="R",
        iop="R: 15, L: 16 mmHg",  # Intraocular pressure
        glasses_role="Distance",
        lenses_material="Polycarbonate",
        lenses_diameter=70.0,  # mm
        segment_diameter=28.0,  # mm
        lenses_manufacturer="Essilor",
        lenses_color="Clear",
        catalog_num="ESL-12345",

        frame_manufacturer="Ray-Ban",
        frame_supplier="Optica Jerusalem",
        frame_model="RB3025 Aviator",
        frame_size="58-14",
        frame_bar_length="135",
        frame_color="Gold",

        diagnosis="Myopia with Astigmatism",
        notes="Patient reports mild eye strain after long computer use."
    )


# ------------------------------------------------------
# TEST: add_test()
# ------------------------------------------------------
def test_add_test():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    test = sample_test()
    saved = repo.add_test(test)

    assert saved.id == 1
    assert saved.customer_id == 1

    # Verify row in DB
    row = conn.execute("SELECT * FROM refraction_tests WHERE id=1").fetchone()
    assert row is not None
    assert row["customer_id"] == 1
    assert row["examiner"] == "Dr. Smith"
    assert row["r_sphere"] == -1.25


# ------------------------------------------------------
# TEST: get_test()
# ------------------------------------------------------
def test_get_test():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    inserted = repo.add_test(sample_test())
    retrieved = repo.get_test(inserted.id)

    assert retrieved is not None
    assert retrieved.id == inserted.id
    assert retrieved.exam_date == inserted.exam_date.isoformat()


# ------------------------------------------------------
# TEST: get_test() returns None for missing record
# ------------------------------------------------------
def test_get_test_not_found():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    assert repo.get_test(999) is None


# ------------------------------------------------------
# TEST: list_tests_for_customer() orders by exam_date DESC
# ------------------------------------------------------
def test_list_tests_for_customer_ordering():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    # Insert tests with different dates
    t1 = sample_test()
    t1.exam_date = datetime(2024, 1, 1)

    t2 = sample_test()
    t2.exam_date = datetime(2025, 1, 1)

    repo.add_test(t1)
    repo.add_test(t2)

    results = repo.list_tests_for_customer(1)

    assert len(results) == 2
    # Most recent (2025-01-01) first
    assert results[0].exam_date == datetime(2025, 1, 1)
    assert results[1].exam_date == datetime(2024, 1, 1)


# ------------------------------------------------------
# TEST: list_tests_for_customer validation errors
# ------------------------------------------------------
def test_list_tests_for_customer_invalid_none():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    with pytest.raises(ValueError):
        repo.list_tests_for_customer(None)


def test_list_tests_for_customer_invalid_type():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    with pytest.raises(TypeError):
        repo.list_tests_for_customer("abc")


def test_list_tests_for_customer_invalid_negative():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    with pytest.raises(ValueError):
        repo.list_tests_for_customer(-5)


# ------------------------------------------------------
# TEST: list_tests_for_customer gracefully handles corrupted date TEXT
# ------------------------------------------------------
def test_list_tests_customer_corrupted_date():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    # Insert row with invalid date
    conn.execute("""
        INSERT INTO refraction_tests (
            customer_id, exam_date
        ) VALUES (?, ?)
    """, (1, "BAD_DATE_FORMAT"))
    conn.commit()

    results = repo.list_tests_for_customer(1)

    assert len(results) == 1
    # exam_date should stay as raw text (no parsing)
    assert results[0].exam_date == "BAD_DATE_FORMAT"


# ------------------------------------------------------
# TEST: update_test()
# ------------------------------------------------------
def test_update_test():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    test = repo.add_test(sample_test())

    # modify fields
    test.examiner = "Dr. Updated"
    test.r_sphere = -2.00

    repo.update_test(test)

    row = conn.execute("SELECT * FROM refraction_tests WHERE id=?", (test.id,)).fetchone()

    assert row["examiner"] == "Dr. Updated"
    assert row["r_sphere"] == -2.00


# ------------------------------------------------------
# TEST: delete_test()
# ------------------------------------------------------
def test_delete_test():
    conn = setup_in_memory_db()
    repo = RefractionRepo(conn)

    inserted = repo.add_test(sample_test())
    repo.delete_test(inserted.id)

    row = conn.execute("SELECT * FROM refraction_tests WHERE id=?", (inserted.id,)).fetchone()
    assert row is None
