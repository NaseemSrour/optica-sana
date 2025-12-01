# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from db.connection import get_connection
from db.models import Customer
from db.repositories.customer_repo import CustomerRepo

from db.bootstrap import initialize_database
from services.customer_service import CustomerService

DB_PATH = "data/app.db"

def build_container():
    """
    Dependency Injection container.
    Creates reusable objects and returns them.
    """
    repo = CustomerRepo(DB_PATH)
    service = CustomerService(repo)
    return service

def main():
    initialize_database()  # ← Ensures DB exists before app runs
    customer_service = build_container()

    # Example usage:
    new_id = customer_service.add_customer(
        first_name="Naseem",
        last_name="Srour",
        phone="050-1234567",
        email="test@example.com"
    )
    print("Created new customer with ID:", new_id)

    print(customer_service.search_customers("Naseem"))


if __name__ == "__main__":
    connection = get_connection()
    repo = CustomerRepo(connection)

    # Create
    customer = repo.delete_customer(6)
    print(customer)
    connection.close()

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

