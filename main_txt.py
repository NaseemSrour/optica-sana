from db.bootstrap import initialize_database
from main import build_container
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from db.connection import get_connection
from db.repositories.customer_repo import CustomerRepo
from services.customer_service import CustomerService
from ui.screens.customer_details_screen import CustomerDetailsScreen


class CustomerApp(App):
    """A Textual app to display customer details."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        connection = get_connection()
        customer_repo = CustomerRepo(connection)
        # Note: Passing None for glasses_repo and lenses_repo as they are not needed for this screen
        customer_service = CustomerService(customer_repo, None, None)
        customer = customer_service.get_customer(1)  # Assuming customer with id 1 exists
        yield CustomerDetailsScreen(customer, customer_service)
    """
    def on_mount(self) -> None:
        "Called when the app is mounted."
        connection = get_connection()
        customer_repo = CustomerRepo(connection)
        # Note: Passing None for glasses_repo and lenses_repo as they are not needed for this screen
        customer_service = CustomerService(customer_repo, None, None)
        customer = customer_service.get_customer(1)  # Assuming customer with id 1 exists
        if customer:
            self.push_screen(CustomerDetailsScreen(customer, customer_service))
        else:
            self.exit("Customer with ID 1 not found.")
            """


if __name__ == "__main__":
    customer_dict = {
    "id": -1,
    "ssn": 987654321,
    "fname": "Jane",
    "lname": "Smith",
    "birth_date": "1992-11-20",
    "sex": "Female",
    "tel_home": "6785488",
    "tel_mobile": "0527481711",
    "address": "456 Oak St",
    "town": "Shelbyville",
    "postal_code": "62705",
    "status": "Lead",
    "org": "School District",
    "occupation": "Teacher",
    "hobbies": "Reading",
    "referer": "Referral",
    "glasses_num": 0,
    "lenses_num": 1,
    "mailing": 0,
    "notes": "No allergies."
}
    # initialize_database()  # ← Ensures DB exists before app runs
    # customer_service = build_container()
    # customer_service.add_customer(customer_dict)
    app = CustomerApp()
    app.run()