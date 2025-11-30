# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = StopwatchApp()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

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

