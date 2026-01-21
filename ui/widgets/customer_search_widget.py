from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, ListView, ListItem, Label, Static
from textual.widget import Widget
from textual.reactive import reactive
import uuid

DEBOUNCE_DELAY = 0.3  # 300ms debounce


class SearchResultItem(ListItem):
    """Custom styled list item for search results"""

    def __init__(self, customer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer

    def compose(self) -> ComposeResult:
        with Horizontal(classes="result-item-container"):
            yield Label(f"{self.customer.fname} {self.customer.lname}", classes="customer-name")
            if hasattr(self.customer, 'ssn') and self.customer.ssn:
                yield Label(f"ID: {self.customer.ssn}", classes="customer-ssn")


class CustomerSearchWidget(Widget):
    """Beautiful, intuitive customer search widget with live results"""

    result_count = reactive(0)
    is_searching = reactive(False)

    def __init__(self, repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = repo
        self._search_timer = None

    def compose(self) -> ComposeResult:
        with Container(id="search-container"):
            # Header section
            yield Static("🔍 Search Customers", id="search-header")

            # Search input section
            with Container(id="search-input-container"):
                yield Input(
                    placeholder="Type customer name or SSN...",
                    id="customer-input"
                )

            # Results info bar
            with Horizontal(id="results-info"):
                yield Label("", id="result-count")
                yield Label("", id="search-status")

            # Results list container
            with Container(id="results-container"):
                yield ListView(id="results-list")
                yield Static("Start typing to search for customers", id="empty-state", classes="visible")

    def on_mount(self) -> None:
        """Focus the input when widget mounts"""
        self.query_one("#customer-input", Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Debounced input handler with live search"""
        if self._search_timer:
            self._search_timer.stop()

        # Clear results immediately if input is empty
        if not event.value.strip():
            self.clear_results()
            self.show_empty_state("Start typing to search for customers")
            return

        # Show searching indicator
        self.is_searching = True
        self.update_status("Searching...")

        # Debounced search
        self._search_timer = self.set_timer(
            DEBOUNCE_DELAY,
            lambda: self.run_search(event.value),
        )

    def run_search(self, query: str) -> None:
        """Execute search and populate results"""
        results_view = self.query_one("#results-list", ListView)
        results_view.clear()

        if not query.strip():
            self.clear_results()
            return

        # Perform search
        results = self.repo.search_customers_by_name_or_ssn(query)

        # Update result count
        self.result_count = len(results)
        self.is_searching = False

        # Populate results
        if results:
            self.hide_empty_state()
            for customer in results:
                item = SearchResultItem(
                    customer,
                    id=f"result-{uuid.uuid4()}"
                )
                results_view.append(item)

            # Auto-highlight first result
            if len(results_view) > 0:
                results_view.index = 0

            self.update_count(len(results))
            self.update_status("")
        else:
            self.show_empty_state("No customers found")
            self.update_count(0)
            self.update_status("")

    def clear_results(self) -> None:
        """Clear all search results"""
        results_view = self.query_one("#results-list", ListView)
        results_view.clear()
        self.result_count = 0
        self.update_count(0)
        self.update_status("")

    def show_empty_state(self, message: str) -> None:
        """Show empty state message"""
        empty_state = self.query_one("#empty-state", Static)
        empty_state.update(message)
        empty_state.add_class("visible")

    def hide_empty_state(self) -> None:
        """Hide empty state message"""
        empty_state = self.query_one("#empty-state", Static)
        empty_state.remove_class("visible")

    def update_count(self, count: int) -> None:
        """Update result count display"""
        count_label = self.query_one("#result-count", Label)
        if count > 0:
            count_label.update(f"📊 {count} result{'s' if count != 1 else ''} found")
        else:
            count_label.update("")

    def update_status(self, status: str) -> None:
        """Update search status display"""
        status_label = self.query_one("#search-status", Label)
        status_label.update(status)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle when a customer is selected from the list"""
        if isinstance(event.item, SearchResultItem):
            customer = event.item.customer
            # Post a custom message that parent can handle
            # self.post_message(self.CustomerSelected(customer))
"""
    class CustomerSelected(Widget.Selected):
        "Custom message when a customer is selected"

        def __init__(self, customer):
            super().__init__()
            self.customer = customer
            
            """
