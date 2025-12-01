import sqlite3
import pytest

from db.repositories.customer_repo import CustomerRepo


# -----------------------------------
# Helpers
# -----------------------------------
def create_test_connection():
    """Creates a fresh in-memory SQLite DB with schema for each test."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssn TEXT NOT NULL,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            phone TEXT,
            town TEXT,
            notes TEXT
        );
    """)

    return conn


@pytest.fixture
def repo():
    conn = create_test_connection()
    return CustomerRepo(conn)


# -----------------------------------
# TESTS
# -----------------------------------

def test_add_customer(repo):
    c = repo.add_customer(
        ssn="123",
        fname="John",
        lname="Doe",
        phone="050123",
        town="Haifa",
        notes="Test note"
    )

    assert c.id == 1
    assert c.fname == "John"
    assert c.lname == "Doe"

    # Verify DB actually has it
    db_customer = repo.get_customer(1)
    assert db_customer.fname == "John"


def test_get_customer_not_found(repo):
    assert repo.get_customer(999) is None


def test_get_customer_by_ssn(repo):
    repo.add_customer("111", "Alice", "Smith")
    repo.add_customer("222", "Bob", "Blue")

    c = repo.get_customer_by_ssn("222")

    assert c is not None
    assert c.fname == "Bob"
    assert c.lname == "Blue"


def test_list_customers(repo):
    repo.add_customer("111", "Alice", "Smith")
    repo.add_customer("222", "Bob", "Blue")

    all_customers = repo.list_customers()

    assert len(all_customers) == 2
    assert all_customers[0].fname == "Alice"
    assert all_customers[1].fname == "Bob"


def test_search_by_name(repo):
    repo.add_customer("111", "David", "Ben Abo")
    repo.add_customer("222", "Davi", "Stone")
    repo.add_customer("333", "Naseem", "Srour")

    results = repo.search_by_name("Dav")

    assert len(results) == 2
    assert {c.ssn for c in results} == {"111", "222"}


def test_search_by_full_name(repo):
    repo.add_customer("111", "David Ben", "Zeid")
    repo.add_customer("222", "David", "Ben Zeid")

    results = repo.search_by_name("Ben Zeid")

    assert len(results) == 2


def test_update_customer(repo):
    c = repo.add_customer("111", "Old", "Name")
    c.fname = "New"
    c.lname = "Name"

    ok = repo.update_customer(c)
    assert ok is True

    updated = repo.get_customer(c.id)
    assert updated.fname == "New"


def test_delete_customer(repo):
    c = repo.add_customer("111", "John", "Doe")

    ok = repo.delete_customer(c.id)
    assert ok is True

    assert repo.get_customer(c.id) is None
    assert repo.list_customers() == []
