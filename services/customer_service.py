from db.models import Customer, RefractionTest
from db.repositories.customer_repo import CustomerRepo
from db.repositories.refraction_repo import RefractionRepo
from datetime import datetime

from db.utils import *


class CustomerService:

    def __init__(self, customer_repo: CustomerRepo, refraction_repo: RefractionRepo):
        self.cus_repo = customer_repo
        self.refraction_repo = refraction_repo

    def add_customer(self, ssn: str, first_name: str, last_name: str, phone: str = None, town: str = None, notes: str = None):
        """
        Apply validation/business logic here.
        """
        if not ssn:
            raise ValueError("Must provide customer ID!")
        if len(ssn) != 9:
            raise ValueError("ID should be 9 digits long!")
        if not first_name.strip() or not last_name.strip():
            raise ValueError("First and last name are required!")
        if not phone and (len(phone) != 10 or not phone.isdigit()):
            raise ValueError("Invalid phone number!")

        if len(first_name.strip()) > 50 or len(last_name.strip()) > 50 or (not town and len(town) > 50) or (not notes and len(notes) > 500):
            raise ValueError("Values are too long!")

        return self.cus_repo.add_customer(ssn, first_name.strip(), last_name.strip(), phone, town, notes)

    def search_customers_by_full_name(self, query: str):
        # Example: normalize input
        return self.cus_repo.search_by_name(query=query.strip())

    def get_customer_by_ssn(self, customer_ssn: str):
        if not customer_ssn:
            raise ValueError("ID must be provided!")
        if len(customer_ssn) != 9:
            raise ValueError("Invalid ID provided!")
        if not customer_ssn.isdigit():
            raise ValueError("ID must contain only numbers!")
        return self.cus_repo.get_customer_by_ssn(customer_ssn)

    def get_customer(self, customer_id: int):
        if not customer_id:
            raise ValueError("Customer internal ID must be provided!")

        if not str(customer_id).isdigit():
            raise ValueError("Customer internal ID must be number only!")

        return self.cus_repo.get_customer(customer_id)

    def update_customer(self, customer: Customer):
        if not customer.id:
            raise ValueError("Customer does not contain an ID!")
        cus_exists = self.cus_repo.get_customer(customer.id)
        if cus_exists is None:
            raise ValueError("Customer does not exist in DB!")
        if not customer.ssn:
            raise ValueError("Must provide customer ID!")
        if len(customer.ssn) != 9:
            raise ValueError("ID should be 9 digits long!")
        if not customer.fname.strip() or not customer.lname.strip():
            raise ValueError("First and last name are required!")
        if not customer.phone and (len(customer.phone) != 10 or not customer.phone.isdigit()):
            raise ValueError("Invalid phone number!")

        if len(customer.fname.strip()) > 50 or len(customer.lname.strip()) > 50 or (not customer.town and len(customer.town) > 50) or (not customer.notes and len(customer.notes) > 500):
            raise ValueError("Values are too long!")
        self.cus_repo.update_customer(customer)

    def delete_customer(self, customer_id: int):
        self.cus_repo.delete_customer(customer_id)

    # -----------------------------------------
    # 'Refraction Test' Operations
    # -----------------------------------------

    def add_refraction_test(self, customer_id, test_data: dict):
        # Adds and returns a newly-created RefractionTest object

        # Validate fields:
        valid = self.validate_input_refraction_test(customer_id, test_data)
        if not valid:
            return None

        # Convert exam_date string → datetime
        test_data["exam_date"] = str_to_date(test_data["exam_date"]) # convert String '27/1/2025' --> datetime object -- and in the Ref repo: --> the ISO format of that object, as a String.

        # Create dataclass
        ref_test = RefractionTest(**test_data)

        return self.refraction_repo.add_test(ref_test) # is passed an object, not a dict, to ensure complete and correct objects.

    def get_refraction_history(self, customer_id):
        # Returns a list of RefractionTest
        if not self.validate_customer_exists(customer_id):
            return None

        return self.refraction_repo.list_tests_for_customer(customer_id)

    def get_latest_refraction(self, customer_id) -> RefractionTest:
        if not self.validate_customer_exists(customer_id):
            return None

        history = self.refraction_repo.list_tests_for_customer(customer_id)
        return history[0] if history else None

    def update_refraction_test(self, customer_id, updated_test_data: dict):
        """Returns a boolean"""

        if not self.validate_customer_exists(customer_id):
            return None
        valid = self.validate_input_refraction_test(customer_id, updated_test_data)
        if not valid:
            return None

        # Convert exam_date string → datetime
        updated_test_data["exam_date"] = str_to_date(updated_test_data["exam_date"])
        # Create dataclass
        ref_test = RefractionTest(**updated_test_data)  # is passed an object, not a dict, to ensure complete and correct objects.

        return self.refraction_repo.update_test(ref_test)

    def delete_refraction_test(self, test_id: int):
        return self.refraction_repo.delete_test(test_id)  # DB doesn't fail if the test_id doesn't exist.

    # -----------------------------------------
    # Validation helper functions:
    # -----------------------------------------

    def validate_input_refraction_test(self, customer_id, test_data: dict):
        # --- Step 1: Validate customer_id ---
        if not isinstance(customer_id, int) or customer_id <= 0:
            print("Invalid customer ID")
            return False

        # Check that customer actually exists
        customer = self.cus_repo.get_customer(customer_id)
        if customer is None:
            print(f"Customer {customer_id} does not exist")
            return False

        # --- Step 2: Validate required field(s) ---
        if "exam_date" not in test_data:
            print("exam_date is required")
            return False

        # --- Step 3: Validate exam_date (must be YYYY-MM-DD) ---
        try:
            str_to_date(test_data["exam_date"])
        except ValueError:
            print("exam_date must be in format YYYY-MM-DD")
            return False

        # --- Step 4: Validate numeric fields (optional, if given) ---
        numeric_fields = [
            "r_sphere", "r_cylinder", "r_axis",
            "l_sphere", "l_cylinder", "l_axis",
            "pd", "addition"
        ]

        for field in numeric_fields:
            if field in test_data and test_data[field] is not None:
                if not isinstance(test_data[field], (int, float)):
                    print(f"{field} must be numeric")
                    return False
        return True

    def validate_customer_exists(self, customer_id):
        # Validate customer exists
        customer = self.cus_repo.get_customer(customer_id)
        if not customer:
            print(f"Customer with ID {customer_id} is not found")
            return False
        return True
