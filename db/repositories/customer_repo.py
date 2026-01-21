from typing import List

from db.models import Customer
from db.sql_queries import ADD_NEW_CUSTOMER_QUERY
from db.utils import dict_from_row, row_to_dataclass


class CustomerRepo:

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # CREATE
    # -----------------------------
    def add_customer(self, new_customer: Customer) -> Customer:
        """Receives an object, not a dict, to ensure complete objects & correct field naming."""
        # convenience wrapper that internally creates a cursor, runs the query, and returns that cursor.

        cursor = self.conn.execute(ADD_NEW_CUSTOMER_QUERY, (new_customer.ssn, new_customer.fname, new_customer.lname, new_customer.birth_date, new_customer.sex, new_customer.tel_home, new_customer.tel_mobile, new_customer.address, new_customer.town, new_customer.postal_code, new_customer.status, new_customer.org, new_customer.occupation, new_customer.hobbies, new_customer.referer, new_customer.glasses_num, new_customer.lenses_num, new_customer.mailing, new_customer.notes))
        self.conn.commit()

        new_customer.id = cursor.lastrowid
        return new_customer

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

    def search_by_name_or_ssn(self, query: str) -> List[Customer]:
        """Search by full name, partial name, or anything in-between"""
        cur = self.conn.cursor()

        words = query.strip().split()

        if not words:
            return []

        conditions = []
        params = []

        for w in words:
            like = f"%{w}%"
            conditions.append("(fname LIKE ? OR lname LIKE ? OR ssn LIKE ?)")
            params.extend([like, like, like])

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
            SET ssn = ?, fname = ?, lname = ?, birth_date = ?, sex = ?, tel_home = ?, tel_mobile = ?, address = ?, town = ?, postal_code = ?, status = ?, org = ?, occupation = ?, hobbies = ?, referer = ?, glasses_num = ?, lenses_num = ?, mailing = ?, notes = ?
            WHERE id = ?
        """, (customer.ssn, customer.fname, customer.lname, customer.birth_date, customer.sex, customer.tel_home, customer.tel_mobile, customer.address, customer.town, customer.postal_code, customer.status, customer.org, customer.occupation, customer.hobbies, customer.referer, customer.glasses_num, customer.lenses_num, customer.mailing, customer.notes, customer.id))

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
