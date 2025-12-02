from typing import Optional

from db.models import RefractionTest
from db.utils import *


class RefractionRepo:

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # CREATE
    # -----------------------------
    def add_test(self, test: RefractionTest) -> RefractionTest:
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
            test.od_sphere, test.od_cylinder, test.od_axis, test.od_add, test.od_va,
            test.os_sphere, test.os_cylinder, test.os_axis, test.os_add, test.os_va,
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
        rows = self.conn.execute("""
            SELECT * FROM refraction_tests
            WHERE customer_id = ?
            ORDER BY exam_date DESC
        """, (customer_id,)).fetchall()

        results = []
        for r in rows:
            data = dict_from_row(r)
            data["exam_date"] = text_to_datetime(data["exam_date"])
            results.append(RefractionTest(**data))

        return results

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_test(self, test: RefractionTest) -> bool:
        self.conn.execute("""
            UPDATE refraction_tests
            SET customer_id=?, exam_date=?, examiner=?,
                od_sphere=?, od_cylinder=?, od_axis=?, od_add=?, od_va=?,
                os_sphere=?, os_cylinder=?, os_axis=?, os_add=?, os_va=?,
                pupil_distance=?, diagnosis=?, notes=?
            WHERE id=?
        """, (
            test.customer_id,
            datetime_to_text(test.exam_date),
            test.examiner,
            test.od_sphere, test.od_cylinder, test.od_axis, test.od_add, test.od_va,
            test.os_sphere, test.os_cylinder, test.os_axis, test.os_add, test.os_va,
            test.pupil_distance, test.diagnosis, test.notes,
            test.id
        ))

        self.conn.commit()
        return True

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_test(self, test_id: int) -> bool:
        self.conn.execute("""
            DELETE FROM refraction_tests WHERE id = ?
        """, (test_id,))
        self.conn.commit()
        return True
