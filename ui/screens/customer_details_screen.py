
from db.models import Customer
from services.customer_service import CustomerService

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Header, Footer, Label, Input, Button, Static
from textual.binding import Binding



class CustomerDetailsScreen(Static):

    def __init__(self, customer: Customer, customer_service: CustomerService) -> None:
        super().__init__()
        self.customer = customer
        self.customer_service = customer_service
        self.is_editing = False

    def compose(self) -> ComposeResult:
        yield Header(name="Customer Details")
        with VerticalScroll(id="customer-details-container"):
            yield Label("SSN:")
            yield Input(value=str(self.customer.ssn), id="ssn", disabled=True)
            yield Label("First Name:")
            yield Input(value=self.customer.fname, id="fname", disabled=True)
            yield Label("Last Name:")
            yield Input(value=self.customer.lname, id="lname", disabled=True)
            yield Label("Birth Date:")
            yield Input(value=self.customer.birth_date, id="birth_date", disabled=True)
            yield Label("Sex:")
            yield Input(value=self.customer.sex, id="sex", disabled=True)
            yield Label("Home Phone:")
            yield Input(value=self.customer.tel_home, id="tel_home", disabled=True)
            yield Label("Mobile Phone:")
            yield Input(value=self.customer.tel_mobile, id="tel_mobile", disabled=True)
            yield Label("Address:")
            yield Input(value=self.customer.address, id="address", disabled=True)
            yield Label("Town:")
            yield Input(value=self.customer.town, id="town", disabled=True)
            yield Label("Postal Code:")
            yield Input(value=self.customer.postal_code, id="postal_code", disabled=True)
            yield Label("Status:")
            yield Input(value=self.customer.status, id="status", disabled=True)
            yield Label("Organization:")
            yield Input(value=self.customer.org, id="org", disabled=True)
            yield Label("Occupation:")
            yield Input(value=self.customer.occupation, id="occupation", disabled=True)
            yield Label("Hobbies:")
            yield Input(value=self.customer.hobbies, id="hobbies", disabled=True)
            yield Label("Referer:")
            yield Input(value=self.customer.referer, id="referer", disabled=True)
            yield Label("Notes:")
            yield Input(value=self.customer.notes, id="notes", disabled=True)
        yield Footer()

    def on_key(self, event) -> None:
        if event.key == "f2":
            self.toggle_edit_mode()
        elif event.key == "ctrl+s":
            if self.is_editing:
                self.save_customer()

    def toggle_edit_mode(self):
        self.is_editing = not self.is_editing
        for _input in self.query(Input):
            _input.disabled = not self.is_editing
        self.query_one(Header).title = "Customer Details" + (" (Editing)" if self.is_editing else "")

    def save_customer(self):
        # Collect data from inputs
        customer_data = {
            "id": self.customer.id,
            "ssn": self.query_one("#ssn", Input).value,
            "fname": self.query_one("#fname", Input).value,
            "lname": self.query_one("#lname", Input).value,
            "birth_date": self.query_one("#birth_date", Input).value,
            "sex": self.query_one("#sex", Input).value,
            "tel_home": self.query_one("#tel_home", Input).value,
            "tel_mobile": self.query_one("#tel_mobile", Input).value,
            "address": self.query_one("#address", Input).value,
            "town": self.query_one("#town", Input).value,
            "postal_code": self.query_one("#postal_code", Input).value,
            "status": self.query_one("#status", Input).value,
            "org": self.query_one("#org", Input).value,
            "occupation": self.query_one("#occupation", Input).value,
            "hobbies": self.query_one("#hobbies", Input).value,
            "referer": self.query_one("#referer", Input).value,
            "notes": self.query_one("#notes", Input).value,
            # These fields are not editable in this screen
            "glasses_num": self.customer.glasses_num,
            "lenses_num": self.customer.lenses_num,
            "mailing": self.customer.mailing,
        }

        try:
            # Create a new Customer object from the data
            updated_customer = Customer(**customer_data)
            self.customer_service.update_customer(updated_customer)
            self.customer = updated_customer
            self.toggle_edit_mode()
            # Optionally, show a notification that the customer was saved
        except Exception as e:
            # Handle validation errors or other exceptions
            # You could show a dialog with the error message
            pass

if __name__ == '__main__':
    from db.repositories.customer_repo import CustomerRepo
    from db.connection import get_db_connection

    class MyApp(App):
        def __init__(self):
            super().__init__()
            self.connection = get_db_connection()
            self.customer_repo = CustomerRepo(self.connection)
            self.customer_service = CustomerService(self.customer_repo, None, None)
            self.customer = self.customer_service.get_customer(1) # Assuming customer with id 1 exists

        def on_mount(self):
            self.push_screen(CustomerDetailsScreen(self.customer, self.customer_service))

    app = MyApp()
    app.run()
