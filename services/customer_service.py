from dataclasses import asdict

from db.models import Customer, GlassesTest, ContactLensesTest
from db.repositories.contact_lenses_repo import ContactLensesTestRepo
from db.repositories.customer_repo import CustomerRepo
from db.repositories.glasses_repo import GlassesRepo
from db.utils import *


class CustomerService:

    def __init__(self, customer_repo: CustomerRepo, glasses_repo: GlassesRepo, lenses_repo: ContactLensesTestRepo):
        self.cus_repo = customer_repo
        self.glasses_repo = glasses_repo
        self.lenses_repo = lenses_repo

    def add_customer(self, customer_data: dict):
        # Adds and returns a newly-created Customer object

        # Validate fields:
        valid = self.validate_input_customer(customer_data)
        if not valid:
            return None

        # No need: as customer.birth_date is a String, not a datetime.
        # Convert birth_date string → datetime
        # customer_data["birth_date"] = str_to_date(customer_data["birth_date"]) # convert String '27/1/2025' --> datetime object -- and in the Glasses repo: --> the ISO format of that object, as a String.

        # Create dataclass
        new_customer = Customer(**customer_data)

        return self.cus_repo.add_customer(new_customer) # is passed an object, not a dict, to ensure complete and correct objects.

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
            raise ValueError("Must provide customer SSN!")
        if len(str(customer.ssn)) != 9:
            raise ValueError("ID should be 9 digits long!")
        if not customer.fname.strip() or not customer.lname.strip():
            raise ValueError("First and last name are required!")

        # Validate fields:
        valid = self.validate_input_customer(asdict(customer))
        if not valid:
            return None

        self.cus_repo.update_customer(customer)

    def delete_customer(self, customer_id: int):
        self.cus_repo.delete_customer(customer_id)

    # -----------------------------------------
    # 'Glasses Test' Operations
    # -----------------------------------------

    def add_glasses_test(self, customer_id, test_data: dict):
        # Adds and returns a newly-created GlassesTest object

        # Validate fields:
        valid = self.validate_input_glasses_test(customer_id, test_data)
        if not valid:
            return None

        # Convert exam_date string → datetime
        test_data["exam_date"] = str_to_date(test_data["exam_date"]) # convert String '27/1/2025' --> datetime object -- and in the Glasses repo: --> the ISO format of that object, as a String.

        # Create dataclass
        ref_test = GlassesTest(**test_data)

        return self.glasses_repo.add_test(ref_test) # is passed an object, not a dict, to ensure complete and correct objects.

    def get_glasses_history(self, customer_id):
        # Returns a list of GlassesTest
        if not self.validate_customer_exists(customer_id):
            return None

        return self.glasses_repo.list_tests_for_customer(customer_id)

    def get_latest_glasses(self, customer_id) -> GlassesTest:
        if not self.validate_customer_exists(customer_id):
            return None

        history = self.glasses_repo.list_tests_for_customer(customer_id)
        return history[0] if history else None

    def update_glasses_test(self, customer_id, updated_test_data: dict):
        """Returns a boolean"""

        if not self.validate_customer_exists(customer_id):
            return None
        valid = self.validate_input_glasses_test(customer_id, updated_test_data)
        if not valid:
            return None

        # Convert exam_date string → datetime
        updated_test_data["exam_date"] = str_to_date(updated_test_data["exam_date"])
        # Create dataclass
        ref_test = GlassesTest(**updated_test_data)  # is passed an object, not a dict, to ensure complete and correct objects.

        return self.glasses_repo.update_test(ref_test)

    def delete_glasses_test(self, test_id: int):
        return self.glasses_repo.delete_test(test_id)  # DB doesn't fail if the test_id doesn't exist.

    # -----------------------------------------
    # 'Contact Lenses Test' Operations
    # -----------------------------------------

    def add_contact_lenses_test(self, customer_id, test_data: dict):
        # Adds and returns a newly-created ContactLensesTest object

        # Validate fields:
        valid = self.validate_input_contact_lenses_test(customer_id, test_data)
        if not valid:
            return None

        # Convert exam_date string → datetime
        test_data["exam_date"] = str_to_date(test_data["exam_date"]) # convert String '27/1/2025' --> datetime object -- and in the Lenses repo: --> the ISO format of that object, as a String.

        # Create dataclass
        lenses_test = ContactLensesTest(**test_data)

        return self.lenses_repo.add_test(lenses_test)  # is passed an object, not a dict, to ensure complete and
        # correct objects.

    def get_contact_lenses_history(self, customer_id):
        # Returns a list of ContactLensesTest
        if not self.validate_customer_exists(customer_id):
            return None

        return self.lenses_repo.list_tests_for_customer(customer_id)

    def get_latest_contact_lenses(self, customer_id) -> ContactLensesTest:
        if not self.validate_customer_exists(customer_id):
            return None

        history = self.lenses_repo.list_tests_for_customer(customer_id)
        return history[0] if history else None

    def update_contact_lenses_test(self, customer_id, updated_test_data: dict):
        """Returns a boolean"""

        if not self.validate_customer_exists(customer_id):
            return None
        valid = self.validate_input_contact_lenses_test(customer_id, updated_test_data)
        if not valid:
            return None

        # Convert exam_date string → datetime
        updated_test_data["exam_date"] = str_to_date(updated_test_data["exam_date"])
        # Create dataclass
        ref_test = ContactLensesTest(**updated_test_data)  # is passed an object, not a dict, to ensure complete and correct objects.

        return self.lenses_repo.update_test(ref_test)

    def delete_contact_lenses_test(self, test_id: int):
        return self.lenses_repo.delete_test(test_id)  # DB doesn't fail if the test_id doesn't exist.

    # -----------------------------------------------------------------------------------------------------------------
    #                                               Validation helper functions:
    # -----------------------------------------------------------------------------------------------------------------

    def validate_input_customer(self, customer_data: dict):
        """
        Apply validation/business logic here.
        """
        if not customer_data["ssn"]:
            print("Must provide customer SSN!")
            return False

        if len(str(customer_data["ssn"])) != 9:
            print("ID should be 9 digits long!")
            return False

        if not customer_data["fname"].strip() or not customer_data["lname"].strip():
            print("First and last name are required!")
            return False

        if customer_data["tel_mobile"] and (len(customer_data["tel_mobile"]) != 10 or not customer_data["tel_mobile"].isdigit()):
            print("Invalid phone number!")
            return False

        if len(customer_data["fname"].strip()) > 50 or len(customer_data["lname"].strip()) > 50:
            print("Name is too long!")
            return False

        if customer_data["town"] and len(customer_data["town"]) > 50:
            print("Town name is too long!")
            return False

        if customer_data["notes"] and len(customer_data["notes"]) > 500:
            print("Notes exceed maximum length of 500 characters!")
            return False

        if customer_data["glasses_num"] and not isinstance(customer_data["glasses_num"], int):
            print("Error: Glasses number must be an integer!")
            return False

        if customer_data["lenses_num"] and not isinstance(customer_data["lenses_num"], int):
            print("Error: Lenses number must be an integer!")
            return False
        if customer_data["mailing"] and not isinstance(customer_data["mailing"], int):
            print("Error: Mailing must be an integer!")
            return False

        # Lengths checks:
        if customer_data["birth_date"] and len(customer_data["birth_date"]) > 50:
            print("Birth date exceed maximum length of 50 characters!")
            return False
        if customer_data["sex"] and len(customer_data["sex"]) > 20:
            print("Sex exceed maximum length of 20 characters!")
            return False
        if customer_data["tel_home"] and len(customer_data["tel_home"]) > 15:
            print("Tel. Home exceed maximum length of 15 characters!")
            return False
        if customer_data["address"] and len(customer_data["address"]) > 100:
            print("Address exceed maximum length of 100 characters!")
            return False
        if customer_data["postal_code"] and len(customer_data["postal_code"]) > 20:
            print("Postal code exceed maximum length of 20 characters!")
            return False
        if customer_data["status"] and len(customer_data["status"]) > 50:
            print("Status exceed maximum length of 50 characters!")
            return False
        if customer_data["org"] and len(customer_data["org"]) > 50:
            print("Org exceed maximum length of 50 characters!")
            return False
        if customer_data["occupation"] and len(customer_data["occupation"]) > 50:
            print("Occupation exceed maximum length of 50 characters!")
            return False
        if customer_data["hobbies"] and len(customer_data["hobbies"]) > 50:
            print("Hobbies exceed maximum length of 50 characters!")
            return False
        if customer_data["referer"] and len(customer_data["referer"]) > 50:
            print("Referer exceed maximum length of 50 characters!")
            return False

        return True


    def validate_input_glasses_test(self, customer_id, test_data: dict):
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
            "r_cylinder", "r_axis", "r_prism", "r_add_read", "r_add_int",
            "r_add_bif", "r_add_mul", "r_high",
            "l_cylinder", "l_axis", "l_prism", "l_add_read", "l_add_int",
            "l_add_bif", "l_add_mul", "l_high",
            "lenses_diameter_1", "lenses_diameter_2", "segment_diameter",
        ]

        for field in numeric_fields:
            if field in test_data and test_data[field] is not None:
                if not isinstance(test_data[field], (int, float)):
                    print(f"{field} must be numeric")
                    return False

        # If Right cylinder is 0 → axis must be None
        if test_data["r_cylinder"] is None:  #  or test_data["r_cylinder"] == 0
            if test_data["r_axis"] not in (None,):
                raise ValueError("R_Axis must be None when cylinder is 0.00")
        # Otherwise must be 0–180 integer
        if not isinstance(test_data["r_axis"], int):
            raise ValueError("R_Axis must be an integer between 0 and 180")

        if not (0 <= test_data["r_axis"] <= 180):
            raise ValueError("R_Axis must be between 0 and 180")

        # Left Cylinder/Axis validation:
        if test_data["l_cylinder"] is None:  # or test_data["l_cylinder"] == 0
            if test_data["l_axis"] not in (None,):
                raise ValueError("L_Axis must be None when cylinder is 0.00")
        # Otherwise must be 0–180 integer
        if not isinstance(test_data["l_axis"], int):
            raise ValueError("L_Axis must be an integer between 0 and 180")

        if not (0 <= test_data["l_axis"] <= 180):
            raise ValueError("L_Axis must be between 0 and 180")

        return True

    def validate_input_contact_lenses_test(self, customer_id, test_data: dict):
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
            "r_lens_sp", "r_lens_cyl", "r_lens_axis",
            "l_lens_sph", "l_lens_cyl", "l_lens_axis"
        ]

        for field in numeric_fields:
            if field in test_data and test_data[field] is not None:
                if not isinstance(test_data[field], (int, float)):
                    print(f"{field} must be numeric")
                    return False

        # --- Step 5: Validation Cylinder/Axis relationship ---


        # If RIGHT cylinder is 0 → RIGHT axis must be None
        if test_data["r_lens_cyl"] is None:  # or test_data["r_lens_cyl"] == 0
            if test_data["r_lens_axis"] not in (None,):
                raise ValueError("R_lens_axis must be None when cylinder is None")
        # Otherwise must be 0–180 integer
        if not isinstance(test_data["r_lens_axis"], int):
            raise ValueError("R_lens_axis must be an integer between 0 and 180")

        if not (0 <= test_data["r_lens_axis"] <= 180):
            raise ValueError("R_lens_Axis must be between 0 and 180")

        # If LEFT cylinder is 0 → LEFT axis must be None:
        if test_data["l_lens_cyl"] is None:  # or test_data["l_lens_cyl"] == 0
            if test_data["l_lens_axis"] not in (None,):
                raise ValueError("L_lens_Axis must be None when cylinder is 0.00")
        # Otherwise must be 0–180 integer
        if not isinstance(test_data["l_lens_axis"], int):
            raise ValueError("L_lens_Axis must be an integer between 0 and 180")

        if not (0 <= test_data["l_lens_axis"] <= 180):
            raise ValueError("L_lens_Axis must be between 0 and 180")

        return True

    def validate_customer_exists(self, customer_id):
        # Validate customer exists
        customer = self.cus_repo.get_customer(customer_id)
        if not customer:
            print(f"Customer with ID {customer_id} is not found")
            return False
        return True
