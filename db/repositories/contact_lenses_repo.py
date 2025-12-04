from dataclasses import asdict
from typing import Optional, List
from db.models import ContactLensesTest
from db.utils import datetime_to_text


class ContactLensesTestRepo:
    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # CREATE
    # -----------------------------
    def add_test(self, test: ContactLensesTest) -> int:
        """Insert a new test and return the row ID."""
        data = asdict(test)
        data.pop("id")  # Auto-increment
        data["exam_date"] = datetime_to_text(data["exam_date"])
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO contact_lenses_tests ({columns}) VALUES ({placeholders})"

        cur = self.conn.cursor()
        cur.execute(sql, tuple(data.values()))
        self.conn.commit()

        return cur.lastrowid

    # -----------------------------
    # READ (single)
    # -----------------------------
    def get_test(self, contact_lenses_test_id: int) -> Optional[ContactLensesTest]:
        sql = "SELECT * FROM contact_lenses_tests WHERE id = ?"
        cur = self.conn.cursor()
        row = cur.execute(sql, (contact_lenses_test_id,)).fetchone()
        return ContactLensesTest.from_row(row)

    # -----------------------------
    # READ (multiple)
    # -----------------------------
    def list_tests_for_customer(self, customer_id: int) -> List[ContactLensesTest]:
        if customer_id is None:
            raise ValueError("customer_id must not be None")

        if not isinstance(customer_id, int):
            raise TypeError("customer_id must be an integer")

        if customer_id <= 0:
            raise ValueError("customer_id must be a positive integer")

        sql = """
            SELECT * FROM contact_lenses_tests
            WHERE customer_id = ?
            ORDER BY exam_date DESC
        """
        cur = self.conn.cursor()
        rows = cur.execute(sql, (customer_id,)).fetchall()
        return [ContactLensesTest.from_row(r) for r in rows]

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_test(self, test: ContactLensesTest) -> bool:
        """Update a test. Returns True if a row was updated."""
        if test.id is None:
            raise ValueError("Cannot update a test without an ID")

        data = asdict(test)
        test_id = data.pop("id")

        assignments = ", ".join(f"{k}=?" for k in data.keys())
        sql = f"UPDATE contact_lenses_tests SET {assignments} WHERE id = ?"

        cur = self.conn.cursor()
        result = cur.execute(sql, tuple(data.values()) + (test_id,))
        self.conn.commit()

        return result.rowcount > 0

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_test(self, test_id: int) -> bool:
        sql = "DELETE FROM contact_lenses_tests WHERE id = ?"
        cur = self.conn.cursor()
        result = cur.execute(sql, (test_id,))
        self.conn.commit()
        return result.rowcount > 0
