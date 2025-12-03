# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
from dataclasses import asdict
from db.connection import get_connection
from db.models import Customer, GlassesTest
from db.repositories.customer_repo import CustomerRepo

from db.bootstrap import initialize_database
from db.repositories.glasses_repo import GlassesRepo
from db.utils import date_to_str
from services.customer_service import CustomerService

DB_PATH = "database.db"


def build_container():
    """
    Dependency Injection container.
    Creates reusable objects and returns them.
    """
    conn = get_connection()
    cus_repo = CustomerRepo(conn)
    refr_repo = GlassesRepo(conn)
    service = CustomerService(cus_repo, refr_repo)
    return service


def main():
    initialize_database()  # ← Ensures DB exists before app runs
    customer_service = build_container()

    # Example usage:
    customer_result = customer_service.get_customer_by_ssn("205350457")
    if customer_result is None:
        print("No customer found with ID: 205350457")
    else:
        print("Retrieved customer with ID 205350547: ", customer_result)


if __name__ == "__main__":
    main()

"""
# USING the Customer Repo:
from db.connection import get_connection
from db.repositories.customers_repo import CustomersRepo

conn = get_connection()
repo = CustomersRepo(conn)

# Create
customer = repo.add_customer("John Doe", phone="1234567")
print(customer)

# Read
print(repo.get_customer(customer.id))

# Update
customer.phone = "7654321"
repo.update_customer(customer)

# List
print(repo.list_customers())

# Delete
repo.delete_customer(customer.id)


"""

# -----------------------------
# MY OWN MANUAL TESTS:
# Put them in the main func above with the initialization of the DB and repos
# -----------------------------


def add_ref_test_and_update_it():
    ref_test = GlassesTest(
        id=999,
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

    ref_test_dict = asdict(ref_test)  # datetime objects stay objects
    ref_test_dict["exam_date"] = date_to_str(ref_test_dict["exam_date"])
    print("The input exam date: " + ref_test_dict["exam_date"])
    print()

    # customer_service.add_glasses_test(1, ref_test_dict)

    updated_ref_test = GlassesTest(
        id=1,
        customer_id=5,

        # --- Exam metadata ---
        exam_date=datetime(2025, 5, 9, 14, 30),
        examiner="Sanaa",

        # --- Right Eye (OD) ---
        r_fv_numerator=6,
        r_fv_denominator=9,
        r_sphere=-2.0,
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
        l_fv_numerator = 6,
        l_fv_denominator = 12,
        l_sphere = -1.75,
        l_cylinder = -0.50,
        l_axis= 10,
        l_prism= 0.25,
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

    updated_test_dict = asdict(updated_ref_test)  # datetime objects stay objects
    updated_test_dict["exam_date"] = date_to_str(updated_test_dict["exam_date"])

    # customer_service.update_glasses_test(updated_test_dict["id"], updated_test_dict)

