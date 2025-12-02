from typing import Optional

from db.models import RefractionTest
from db.utils import *


class RefractionRepo:

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # CREATE
    # -----------------------------
    def add_test(self, test: RefractionTest):
        """Receives an object, not a dict, to ensure complete objects & correct field naming."""
        # convenience wrapper that internally creates a cursor, runs the query, and returns that cursor.
        cursor = self.conn.execute(""" 
            INSERT INTO refraction_tests (
                customer_id, exam_date, examiner,
                r_sphere, r_cylinder, r_axis, r_add, r_va,
                l_sphere, l_cylinder, l_axis, l_add, l_va,
                pupil_distance, diagnosis, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test.customer_id,
            datetime_to_text(test.exam_date),
            test.examiner,
            test.r_sphere, test.r_cylinder, test.r_axis, test.r_add, test.r_va,
            test.l_sphere, test.l_cylinder, test.l_axis, test.l_add, test.l_va,
            test.pupil_distance, test.diagnosis, test.notes
        ))

        self.conn.commit()
        test.id = cursor.lastrowid
        return test

    # -----------------------------
    # READ (single)
    # -----------------------------
    def get_test(self, test_id: int) -> Optional[RefractionTest]:
        row = self.conn.execute("""
            SELECT * FROM refraction_tests WHERE id = ?
        """, (test_id,)).fetchone()

        if row:
            return row_to_dataclass(row, RefractionTest)
        return None

    # -----------------------------
    # READ (all by customer)
    # -----------------------------
    def list_tests_for_customer(self, customer_id: int):
        # Repo handles database-level risks (invalid types, corrupted rows)
        # While the Service handles user input and business rules before calling repo
        if customer_id is None:
            raise ValueError("customer_id must not be None")

        if not isinstance(customer_id, int):
            raise TypeError("customer_id must be an integer")

        if customer_id <= 0:
            raise ValueError("customer_id must be a positive integer")

        rows = self.conn.execute("""
            SELECT * FROM refraction_tests
            WHERE customer_id = ?
            ORDER BY exam_date DESC
        """, (customer_id,)).fetchall()

        results = []
        for r in rows:
            data = dict_from_row(r)
            if not (data["exam_date"] is None):
                try:
                    data["exam_date"] = text_to_datetime(data["exam_date"])
                except Exception:
                    pass  # do nothing
            results.append(RefractionTest(**data))

        return results

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_test(self, test: RefractionTest) -> bool:
        """Receives an object, not a dict, to ensure complete objects & correct field naming."""
        # convenience wrapper that internally creates a cursor, runs the query, and returns that cursor.

        self.conn.execute("""
            UPDATE refraction_tests
            SET customer_id=?, exam_date=?, examiner=?,
                r_sphere=?, r_cylinder=?, r_axis=?, r_add=?, r_va=?,
                l_sphere=?, l_cylinder=?, l_axis=?, l_add=?, l_va=?,
                pupil_distance=?, diagnosis=?, notes=?
            WHERE id=?
        """, (
            test.customer_id,
            test.exam_date,
            test.examiner,
            test.r_sphere, test.r_cylinder, test.r_axis, test.r_add, test.r_va,
            test.l_sphere, test.l_cylinder, test.l_axis, test.l_add, test.l_va,
            test.pupil_distance, test.diagnosis, test.notes,
            test.id
        ))

        self.conn.commit()
        return True

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_test(self, test_id: int) -> bool:
        # convenience wrapper that internally creates a cursor, runs the query, and returns that cursor.
        self.conn.execute("""
            DELETE FROM refraction_tests WHERE id = ?
        """, (test_id,))
        self.conn.commit()
        return True
