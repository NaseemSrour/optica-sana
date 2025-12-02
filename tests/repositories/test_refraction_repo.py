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
        CREATE TABLE refraction_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            exam_date TEXT,
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

            pupil_distance INTEGER,
            diagnosis TEXT,
            notes TEXT
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
        customer_id=customer_id,
        exam_date=datetime(2025, 1, 1),
        examiner="Dr. Smith",

        r_sphere=-1.25,
        r_cylinder=-0.75,
        r_axis=180,
        r_add=1.25,
        r_va="20/20",

        l_sphere=-1.00,
        l_cylinder=-0.50,
        l_axis=170,
        l_add=1.00,
        l_va="20/25",

        pupil_distance=64,
        diagnosis="Myopia",
        notes="Patient reported headaches."
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
