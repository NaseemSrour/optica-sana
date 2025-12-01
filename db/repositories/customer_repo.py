from typing import List

from db.models import Customer
from db.utils import dict_from_row, row_to_dataclass


class CustomerRepo:

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # CREATE
    # -----------------------------
    def add_customer(self, ssn, fname, lname, phone=None, town=None, notes=None) -> Customer:
        cursor = self.conn.execute("""
            INSERT INTO customers (ssn, fname, lname, phone, town, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ssn, fname, lname, phone, town, notes))
        self.conn.commit()

        return Customer(
            id=cursor.lastrowid,
            ssn=ssn,
            fname=fname,
            lname=lname,
            phone=phone,
            town=town,
            notes=notes
        )

    # -----------------------------
    # READ (single)
    # -----------------------------
    def get_customer(self, customer_id) -> Customer:
        row = self.conn.execute("""
            SELECT * FROM customers WHERE id = ?
        """, (customer_id,)).fetchone()

        if row:
            return Customer(**dict_from_row(row))
        return None

    def get_customer_by_ssn(self, customer_ssn) -> Customer:
        row = self.conn.execute("""
            SELECT * FROM customers WHERE ssn = ?
        """, (customer_ssn,)).fetchone()

        if row:
            return Customer(**dict_from_row(row))
        return None

    # -----------------------------
    # READ (all)
    # -----------------------------
    def list_customers(self) -> list[Customer]:
        rows = self.conn.execute("""
            SELECT * FROM customers ORDER BY id
        """).fetchall()

        return [Customer(**dict_from_row(r)) for r in rows]

    def search_by_name(self, query: str) -> List[Customer]:
        """Search by full name, partial name, or anything in-between"""
        cur = self.conn.cursor()

        words = query.strip().split()

        if not words:
            return []

        conditions = []
        params = []

        for w in words:
            like = f"%{w}%"
            conditions.append("(fname LIKE ? OR lname LIKE ?)")
            params.extend([like, like])

        sql = f"""
            SELECT * FROM customers
            WHERE {" AND ".join(conditions)}
        """

        rows = cur.execute(sql, params).fetchall()
        return [row_to_dataclass(row, Customer) for row in rows]

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_customer(self, customer: Customer) -> bool:
        self.conn.execute("""
            UPDATE customers
            SET ssn = ?, fname = ?, lname = ?, phone = ?, town = ?, notes = ?
            WHERE id = ?
        """, (customer.ssn, customer.fname, customer.lname, customer.phone, customer.town, customer.notes, customer.id))

        self.conn.commit()
        return True

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_customer(self, customer_id) -> bool:
        self.conn.execute("""
            DELETE FROM customers WHERE id = ?
        """, (customer_id,))
        self.conn.commit()
        return True