import pytest
import sqlite3
from datetime import datetime

from db.models import ContactLensesTest
from db.repositories.contact_lenses_repo import ContactLensesTestRepo


# -------------------------------------------------------------------
# SCHEMA FIXTURE
# -------------------------------------------------------------------
@pytest.fixture
def conn():
    """Provides an in-memory SQLite connection with full schema."""
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    connection.executescript("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );

        INSERT INTO customers (name) VALUES ('John Doe');

        CREATE TABLE contact_lenses_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            exam_date TEXT NOT NULL,
            examiner TEXT,

            r_rH REAL, r_rV REAL, r_aver REAL, r_k_cyl REAL, r_axH INTEGER,
            r_rT REAL, r_rN REAL, r_rI REAL, r_rS REAL,

            l_rH REAL, l_rV REAL, l_aver REAL, l_k_cyl REAL, l_axH INTEGER,
            l_rT REAL, l_rN REAL, l_rI REAL, l_rS REAL,

            r_lens_type TEXT, r_manufacturer TEXT, r_brand TEXT,
            r_diameter REAL, r_base_curve_numerator REAL, r_base_curve_denominator REAL,
            r_lens_sph REAL, r_lens_cyl REAL, r_lens_axis INTEGER,
            r_material TEXT, r_tint TEXT,
            r_lens_va_numerator INTEGER, r_lens_va_denominator INTEGER,

            l_lens_type TEXT, l_manufacturer TEXT, l_brand TEXT,
            l_diameter REAL, l_base_curve_numerator REAL, l_base_curve_denominator REAL,
            l_lens_sph REAL, l_lens_cyl REAL, l_lens_axis INTEGER,
            l_material TEXT, l_tint TEXT,
            l_lens_va_numerator INTEGER, l_lens_va_denominator INTEGER,

            notes TEXT,

            CHECK(
                (r_lens_cyl IS NULL AND r_lens_axis IS NULL) OR
                (r_lens_cyl = 0 AND r_lens_axis IS NULL) OR
                (r_lens_cyl <> 0 AND r_lens_axis BETWEEN 0 AND 180)
            ),
            CHECK(
                (l_lens_cyl IS NULL AND l_lens_axis IS NULL) OR
                (l_lens_cyl = 0 AND l_lens_axis IS NULL) OR
                (l_lens_cyl <> 0 AND l_lens_axis BETWEEN 0 AND 180)
            ),

            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
        );
    """)

    yield connection
    connection.close()


# -------------------------------------------------------------------
# REPOSITORY FIXTURE
# -------------------------------------------------------------------
@pytest.fixture
def repo(conn):
    """Provides a repository with a fresh database."""
    return ContactLensesTestRepo(conn)


# -------------------------------------------------------------------
# EXAMPLE OBJECT FACTORY
# -------------------------------------------------------------------
@pytest.fixture
def make_test():
    """Returns a factory function for creating ContactLensesTest objects."""

    def _factory(**overrides):
        base = dict(
            id=None,
            customer_id=1,
            exam_date=datetime(2025, 2, 15),
            examiner="Dr. Smith",

            r_rH=7.80, r_rV=7.65, r_aver=7.72, r_k_cyl=0.15, r_axH=90,
            r_rT=7.90, r_rN=7.85, r_rI=7.88, r_rS=7.87,

            l_rH=7.75, l_rV=7.60, l_aver=7.67, l_k_cyl=0.15, l_axH=80,
            l_rT=7.82, l_rN=7.78, l_rI=7.80, l_rS=7.79,

            r_lens_type="SF", r_manufacturer="CooperVision", r_brand="Biofinity",
            r_diameter=14.0, r_base_curve_numerator=8.6, r_base_curve_denominator=None,
            r_lens_sph=-2.50, r_lens_cyl=None, r_lens_axis=None,
            r_material="Comfilcon A", r_tint="Blue",
            r_lens_va_numerator=6, r_lens_va_denominator=6,

            l_lens_type="Toric", l_manufacturer="Alcon", l_brand="Air Optix",
            l_diameter=14.5, l_base_curve_numerator=8.7, l_base_curve_denominator=None,
            l_lens_sph=-1.75, l_lens_cyl=-0.75, l_lens_axis=120,
            l_material="Lotrafilcon B", l_tint="Blue",
            l_lens_va_numerator=6, l_lens_va_denominator=9,

            notes="Example notes"
        )

        base.update(overrides)
        return ContactLensesTest(**base)

    return _factory
