# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
from dataclasses import asdict
from db.connection import get_connection
from db.models import Customer, GlassesTest, ContactLensesTest
from db.repositories.contact_lenses_repo import ContactLensesTestRepo
from db.repositories.customer_repo import CustomerRepo

from db.bootstrap import initialize_database
from db.repositories.glasses_repo import GlassesRepo
from db.utils import *
from services.customer_service import CustomerService

DB_PATH = "database.db"


def build_container():
    """
    Dependency Injection container.
    Creates reusable objects and returns them.
    """
    conn = get_connection()
    cus_repo = CustomerRepo(conn)
    glasses_repo = GlassesRepo(conn)
    lenses_repo = ContactLensesTestRepo(conn)
    service = CustomerService(cus_repo, glasses_repo, lenses_repo)
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

    contact_lenses_test = ContactLensesTest(
        id=999,
        customer_id=1,
        exam_date=datetime(2025, 12, 4),
        examiner="סאמר סרור",

        # ===== Keratometry (Right) =====
        r_rH=7.25,
        r_rV=7.65,
        r_aver=7.72,
        r_k_cyl=0.15,
        r_axH=90,
        r_rT=7.90,
        r_rN=7.85,
        r_rI=7.88,
        r_rS=7.87,

        # ===== Keratometry (Left) =====
        l_rH=7.75,
        l_rV=7.60,
        l_aver=7.67,
        l_k_cyl=0.15,
        l_axH=85,
        l_rT=7.82,
        l_rN=7.78,
        l_rI=7.80,
        l_rS=7.79,

        # ===== Right Lens Prescription =====
        r_lens_type="SF",
        r_manufacturer="CooperVision",
        r_brand="Biofinity",
        r_diameter=14.0,
        r_base_curve_numerator=8.6,
        r_base_curve_denominator=None,  # Not used for spherical lenses
        r_lens_sph=-2.50,
        r_lens_cyl=-0.5,
        r_lens_axis=0,
        r_material="Comfilcon A",
        r_tint="Blue",
        r_lens_va_numerator=6,
        r_lens_va_denominator=6,

        # ===== Left Lens Prescription =====
        l_lens_type="Toric",
        l_manufacturer="Alcon",
        l_brand="Air Optix for Astigmatism",
        l_diameter=14.5,
        l_base_curve_numerator=8.7,
        l_base_curve_denominator=None,
        l_lens_sph=-1.75,
        l_lens_cyl=-0.75,  # Toric → requires an axis
        l_lens_axis=120,  # Valid 0–180
        l_material="Lotrafilcon B",
        l_tint="Light Blue",
        l_lens_va_numerator=6,
        l_lens_va_denominator=9,

        notes="Patient prefers monthly lenses. Good comfort. Recheck in 6 months."
    )

    lens_test_dict = asdict(contact_lenses_test)  # datetime objects stay objects
    lens_test_dict["exam_date"] = date_to_str(lens_test_dict["exam_date"])
    print("The input exam date: " + lens_test_dict["exam_date"])
    print()


    history = customer_service.get_latest_contact_lenses(1)
    print(type(history.exam_date))
    print("Last lenses exam date is: " + date_to_str(text_to_datetime(history.exam_date)))

    history = customer_service.add_contact_lenses_test(1, lens_test_dict)
    print(history)


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


def add_glasses_test_and_update_it():
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

    updated_test_dict = asdict(updated_ref_test)  # datetime objects stay objects
    updated_test_dict["exam_date"] = date_to_str(updated_test_dict["exam_date"])

    # customer_service.update_glasses_test(updated_test_dict["id"], updated_test_dict)


def play_around_with_lenses_repo():
    contact_lenses_test = ContactLensesTest(
        id=1,
        customer_id=1,
        exam_date=datetime(2025, 12, 4),
        examiner="Dr. Sarah Cohen",

        # ===== Keratometry (Right) =====
        r_rH=7.25,
        r_rV=7.65,
        r_aver=7.72,
        r_k_cyl=0.15,
        r_axH=90,
        r_rT=7.90,
        r_rN=7.85,
        r_rI=7.88,
        r_rS=7.87,

        # ===== Keratometry (Left) =====
        l_rH=7.75,
        l_rV=7.60,
        l_aver=7.67,
        l_k_cyl=0.15,
        l_axH=85,
        l_rT=7.82,
        l_rN=7.78,
        l_rI=7.80,
        l_rS=7.79,

        # ===== Right Lens Prescription =====
        r_lens_type="SF",
        r_manufacturer="CooperVision",
        r_brand="Biofinity",
        r_diameter=14.0,
        r_base_curve_numerator=8.6,
        r_base_curve_denominator=None,  # Not used for spherical lenses
        r_lens_sph=-2.50,
        r_lens_cyl=None,
        r_lens_axis=None,
        r_material="Comfilcon A",
        r_tint="Blue",
        r_lens_va_numerator=6,
        r_lens_va_denominator=6,

        # ===== Left Lens Prescription =====
        l_lens_type="Toric",
        l_manufacturer="Alcon",
        l_brand="Air Optix for Astigmatism",
        l_diameter=14.5,
        l_base_curve_numerator=8.7,
        l_base_curve_denominator=None,
        l_lens_sph=-1.75,
        l_lens_cyl=-0.75,  # Toric → requires an axis
        l_lens_axis=120,  # Valid 0–180
        l_material="Lotrafilcon B",
        l_tint="Light Blue",
        l_lens_va_numerator=6,
        l_lens_va_denominator=9,

        notes="Patient prefers monthly lenses. Good comfort. Recheck in 6 months."
    )

    conn = get_connection()
    lenses_repo = ContactLensesTestRepo(conn)
    lenses_repo.add_test(contact_lenses_test)
    lenses_repo.update_test(contact_lenses_test)
    print(lenses_repo.get_test(1))
    print(lenses_repo.list_tests_for_customer(1))
    print(lenses_repo.delete_test(1))
    print(lenses_repo.list_tests_for_customer(1))
