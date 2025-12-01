from db.models import Customer
from db.repositories.customer_repo import CustomerRepo


class CustomerService:

    def __init__(self, repo: CustomerRepo):
        self.repo = repo

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

        return self.repo.add_customer(ssn, first_name.strip(), last_name.strip(), phone, town, notes)

    def search_customers_by_full_name(self, query: str):
        # Example: normalize input
        return self.repo.search_by_name(query=query.strip())

    def get_customer_by_ssn(self, customer_ssn: str):
        if not customer_ssn:
            raise ValueError("ID must be provided!")
        if len(customer_ssn) != 9:
            raise ValueError("Invalid ID provided!")
        if not customer_ssn.isdigit():
            raise ValueError("ID must contain only numbers!")
        return self.repo.get_customer_by_ssn(customer_ssn)

    def get_customer(self, customer_id: int):
        if not customer_id:
            raise ValueError("Customer internal ID must be provided!")
        if not customer_id.isdigit():
            raise ValueError("Customer internal ID must be number only!")

        return self.repo.get_customer(customer_id)

    def update_customer(self, customer: Customer):
        if not customer.id:
            raise ValueError("Customer does not contain an ID!")
        if not customer.ssn:
            raise ValueError("Must provide customer ID!")
        if len(customer.ssn) != 9:
            raise ValueError("ID should be 9 digits long!")
        if not customer.fname.strip() or not customer.lnames.strip():
            raise ValueError("First and last name are required!")
        if not customer.phone and (len(customer.phone) != 10 or not customer.phone.isdigit()):
            raise ValueError("Invalid phone number!")

        if len(customer.fname.strip()) > 50 or len(customer.lname.strip()) > 50 or (not customer.town and len(customer.town) > 50) or (not customer.notes and len(customer.notes) > 500):
            raise ValueError("Values are too long!")
        self.repo.update_customer(customer)

    def delete_customer(self, customer_id: int):
        self.repo.delete_customer(customer_id)
