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
            "r_fv_numerator", "r_fv_denominator",
            "r_sphere", "r_cylinder", "r_axis", "r_prism", "r_add_read", "r_add_int",
            "r_add_bif", "r_add_mul", "r_high",
            "l_fv_numerator", "l_fv_denominator",
            "l_sphere", "l_cylinder", "l_axis", "l_prism", "l_add_read", "l_add_int",
            "l_add_bif", "l_add_mul", "l_high",
            "pupil_distance", "lenses_diameter", "segment_diameter",
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
