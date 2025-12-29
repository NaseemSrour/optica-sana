from typing import Optional

from db.models import GlassesTest
from db.sql_queries import *
from db.utils import *


class GlassesRepo:

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # CREATE
    # -----------------------------
    def add_test(self, test: GlassesTest):
        """Receives an object, not a dict, to ensure complete objects & correct field naming."""
        # convenience wrapper that internally creates a cursor, runs the query, and returns that cursor.
        cursor = self.conn.execute(ADD_GLASSES_TEST_QUERY, (
            test.customer_id,
            datetime_to_text(test.exam_date),
            test.examiner,
            test.r_fv, test.r_sphere, test.r_cylinder, test.r_axis, test.r_prism, test.r_base, test.r_va, test.both_va, test.r_add_read, test.r_add_int, test.r_add_bif, test.r_add_mul, test.r_high, test.r_pd, test.sum_pd, test.near_pd,
            test.l_fv, test.l_sphere, test.l_cylinder, test.l_axis, test.l_prism, test.l_base, test.l_va, test.l_add_read, test.l_add_int, test.l_add_bif, test.l_add_mul, test.l_high, test.l_pd,
            test.dominant_eye, test.r_iop, test.l_iop, test.glasses_role, test.lenses_material, test.lenses_diameter_1, test.lenses_diameter_2, test.lenses_diameter_decentration_horizontal, test.lenses_diameter_decentration_vertical, test.segment_diameter, test.lenses_manufacturer, test.lenses_color, test.lenses_coated, test.catalog_num, test.frame_manufacturer, test.frame_supplier, test.frame_model, test.frame_size, test.frame_bar_length, test.frame_color,
            test.diagnosis, test.notes
        ))

        self.conn.commit()
        test.id = cursor.lastrowid
        return test

    # -----------------------------
    # READ (single)
    # -----------------------------
    def get_test(self, test_id: int) -> Optional[GlassesTest]:
        row = self.conn.execute("""
            SELECT * FROM glasses_tests WHERE id = ?
        """, (test_id,)).fetchone()

        if row:
            return row_to_dataclass(row, GlassesTest)
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
            SELECT * FROM glasses_tests
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
            results.append(GlassesTest(**data))

        return results

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_test(self, test: GlassesTest) -> bool:
        """Receives an object, not a dict, to ensure complete objects & correct field naming."""
        # convenience wrapper that internally creates a cursor, runs the query, and returns that cursor.

        self.conn.execute(UPDATE_GLASSES_TEST_QUERY, (
            test.customer_id,
            datetime_to_text(test.exam_date),
            test.examiner,
            test.r_fv, test.r_sphere, test.r_cylinder, test.r_axis, test.r_prism,
            test.r_base, test.r_va, test.both_va, test.r_add_read, test.r_add_int, test.r_add_bif, test.r_add_mul, test.r_high, test.r_pd, test.sum_pd, test.near_pd,
            test.l_fv, test.l_sphere, test.l_cylinder, test.l_axis, test.l_prism,
            test.l_base, test.l_va, test.l_add_read, test.l_add_int, test.l_add_bif, test.l_add_mul, test.l_high, test.l_pd,
            test.dominant_eye, test.r_iop, test.l_iop, test.glasses_role, test.lenses_material, test.lenses_diameter_1, test.lenses_diameter_2, test.lenses_diameter_decentration_horizontal, test.lenses_diameter_decentration_vertical, test.segment_diameter, test.lenses_manufacturer, test.lenses_color, test.lenses_coated, test.catalog_num, test.frame_manufacturer, test.frame_supplier, test.frame_model, test.frame_size, test.frame_bar_length, test.frame_color,
            test.diagnosis, test.notes,
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
            DELETE FROM glasses_tests WHERE id = ?
        """, (test_id,))
        self.conn.commit()
        return True
