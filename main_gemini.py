from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, DataTable
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.binding import Binding


# --- MOCK BACKEND PLACEHOLDER ---
class DataBackend:
    def get_customer_data(self, record_id):
        # Your logic here
        return {"name": "NADER RA'FAT SURUR", "id": "1897", "sph_r": "-1.75"}

    def save_data(self, data):
        # Your logic here
        print(f"Saving to database: {data}")


backend = DataBackend()


class DOSGlassesApp(App):
    CSS = """
    Screen { background: #0000AA; color: white; }

    #header-area { height: 3; background: #00AAAA; color: yellow; text-align: center; text-style: bold; border-bottom: tall white; }

    .table-container {
        height: auto;
        border: double white;
        margin: 1;
        background: #0000AA;
    }

    Input {
        background: #0000AA;
        color: yellow;
        border: none;
        height: 1;
        padding: 0 1;
    }
    Input:focus {
        background: #AAAAAA;
        color: black;
        text-style: bold;
    }

    .label { color: #55FFFF; }
    .data-row { height: 1; margin: 0 2; }

    #footer-hint {
        dock: bottom;
        background: #AAAAAA;
        color: black;
        height: 1;
    }
    """

    # DOS-style Key Bindings
    BINDINGS = [
        Binding("f5", "save", "F5 Save", show=True),
        Binding("f10", "quit", "F10 Exit", show=True),
        Binding("tab", "focus_next", "Tab Next Field", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Static("CUSTOMER RECORD: 1897 - NADER RA'FAT SURUR", id="header-area")

        with Vertical(classes="table-container"):
            # Header Row for the Grid
            yield Static("       Sph.    Cyl.    Ax.    VA     PD", classes="label")

            with Horizontal(classes="data-row"):
                yield Static("R: ", classes="label")
                yield Input(value="-1.75", id="sph_r")
                yield Input(value="-0.50", id="cyl_r")
                yield Input(value="180", id="ax_r")
                yield Input(value="6/6", id="va_r")
                yield Input(value="58", id="pd_r")

            with Horizontal(classes="data-row"):
                yield Static("L: ", classes="label")
                yield Input(value="-1.75", id="sph_l")
                yield Input(value="-", id="cyl_l")
                yield Input(value="-", id="ax_l")
                yield Input(value="6/6", id="va_l")
                yield Input(value="", id="pd_l")

        with Grid(id="details-pane"):
            # You can add more Inputs here for Catalog No, Frame, etc.
            yield Static("CATALOG NO:", classes="label")
            yield Input(placeholder="000000", id="catalog_no")

        yield Static(" F1: Help  |  F5: Save  |  F10: Exit ", id="footer-hint")
        yield Footer()

    def action_save(self) -> None:
        """Called when F5 is pressed."""
        # Pull data from widgets and send to your backend
        data_to_save = {
            "sph_r": self.query_one("#sph_r").value,
            "catalog": self.query_one("#catalog_no").value,
        }
        backend.save_data(data_to_save)
        self.notify("Data Saved Successfully!")

    def on_key(self, event):
        if event.key == "down":
            self.screen.focus_next()
        elif event.key == "up":
            self.screen.focus_previous()


if __name__ == "__main__":
    app = DOSGlassesApp()
    app.run()