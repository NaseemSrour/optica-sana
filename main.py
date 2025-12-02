# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
from dataclasses import asdict
from db.connection import get_connection
from db.models import Customer, RefractionTest
from db.repositories.customer_repo import CustomerRepo

from db.bootstrap import initialize_database
from db.repositories.refraction_repo import RefractionRepo
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
    refr_repo = RefractionRepo(conn)
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

    ref_test = RefractionTest(
        id=None,
        customer_id=1,
        exam_date=datetime(2025, 1, 1),
        examiner="Samer",

        r_sphere=-1.25,
        r_cylinder=-0.75,
        r_axis=180,
        r_add=1.25,
        r_va="20/20",

        l_sphere=-1.00,
        l_cylinder=-0.50,
        l_axis=170,
        l_add=1.00,
        l_va="20/25",

        pupil_distance=64,
        diagnosis="Myopia",
        notes="Patient reported headaches."
    )

    ref_test_dict = asdict(ref_test)  # datetime objects stay objects
    ref_test_dict["exam_date"] = date_to_str(ref_test_dict["exam_date"])
    print("The input exam date: " + ref_test_dict["exam_date"])
    print()

    # customer_service.add_refraction_test(1, ref_test_dict)


    updated_ref_test = RefractionTest(
        id=3,
        customer_id=1,
        exam_date=datetime(2025, 11, 27),
        examiner="Samer",

        r_sphere=-1.25,
        r_cylinder=-0.75,
        r_axis=180,
        r_add=1.25,
        r_va="20/20",

        l_sphere=-1.00,
        l_cylinder=-0.50,
        l_axis=170,
        l_add=1.00,
        l_va="20/25",

        pupil_distance=64,
        diagnosis="Myopia",
        notes="Patient reported headaches."
    )

    updated_test_dict = asdict(updated_ref_test)  # datetime objects stay objects
    updated_test_dict["exam_date"] = date_to_str(updated_test_dict["exam_date"])

    # customer_service.update_refraction_test(1, updated_test_dict)
    # print(customer_service.delete_refraction_test(2))


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
