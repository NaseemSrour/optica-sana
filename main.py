# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from db.connection import get_connection
from db.models import Customer
from db.repositories.customer_repo import CustomerRepo

from db.bootstrap import initialize_database
from services.customer_service import CustomerService

DB_PATH = "database.db"

def build_container():
    """
    Dependency Injection container.
    Creates reusable objects and returns them.
    """
    conn = get_connection()
    cus_repo = CustomerRepo(conn)
    service = CustomerService(cus_repo)
    return service

def main():
    initialize_database()  # ← Ensures DB exists before app runs
    customer_service = build_container()

    # Example usage:
    customer_result = customer_service.get_customer_by_ssn("205350457")
    if(customer_result is None):
        print("No customer fonud with ID: 205350457")
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

