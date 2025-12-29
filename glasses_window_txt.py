from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.widgets import Static, Input, Label
from textual.binding import Binding
from textual.css.query import NoMatches
from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class ExamData:
    """Represents a single eye exam"""
    exam_date: str
    check_date: str
    check_num: str
    # Right eye data
    r_sph: str = ""
    r_cyl: str = ""
    r_axis: str = ""
    r_prism: str = ""
    r_base: str = ""
    r_va: str = ""
    r_add: str = ""
    r_read: str = ""
    r_int: str = ""
    r_bif: str = ""
    r_mul: str = ""
    r_high: str = ""
    # Left eye data
    l_sph: str = ""
    l_cyl: str = ""
    l_axis: str = ""
    l_prism: str = ""
    l_base: str = ""
    l_va: str = ""
    l_add: str = ""
    l_read: str = ""
    l_int: str = ""
    l_bif: str = ""
    l_mul: str = ""
    l_high: str = ""
    # PD
    pd: str = ""
    # Additional fields
    notes: str = ""


class CustomerInfo(Static):
    """Customer information header"""

    def __init__(self, name: str, phone: str, id_num: str):
        super().__init__()
        self.customer_name = name
        self.customer_phone = phone
        self.customer_id = id_num

    def render(self) -> str:
        return f"{self.customer_name:^30} | Phone: {self.customer_phone} | ID: {self.customer_id}"


class ExamNavigator(Static):
    """Shows current exam number and allows navigation"""

    def __init__(self, current: int = 1, total: int = 1):
        super().__init__()
        self.current_exam = current
        self.total_exams = total

    def render(self) -> str:
        return f"Exam {self.current_exam} of {self.total_exams}"

    def update_exam(self, current: int):
        self.current_exam = current
        self.refresh()


class TableInput(Input):
    """Custom input field for table cells"""

    def __init__(self, value: str = "", field_id: str = "", **kwargs):
        super().__init__(value=value, **kwargs)
        self.field_id = field_id

    def key_enter(self) -> None:
        """Move to next field when Enter is pressed"""
        self.screen.focus_next()


class GlassesCheckWindow(Container):
    """Main Glasses Check window widget"""

    BINDINGS = [
        Binding("escape", "quit", "Quit", show=True),
    ]

    def __init__(self, customer_name: str, customer_phone: str, customer_id: str, exams: List[ExamData]):
        super().__init__()
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_id = customer_id
        self.exams = exams
        self.current_exam_index = len(exams) - 1  # Start with latest exam
        self.edit_mode = False  # Track if we're in edit mode

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical(id="main-container"):
            # Customer info header
            yield CustomerInfo(self.customer_name, self.customer_phone, self.customer_id)

            # Exam navigator and dates
            with Horizontal(id="exam-header"):
                yield ExamNavigator(self.current_exam_index + 1, len(self.exams))
                yield Label(id="exam-dates")

            # Main data grid with headers
            with Grid(id="exam-table"):
                # Header row
                yield Label("", classes="table-header")
                yield Label("FU", classes="table-header")
                yield Label("Sph.", classes="table-header")
                yield Label("Cyl.", classes="table-header")
                yield Label("Ax.", classes="table-header")
                yield Label("Pris", classes="table-header")
                yield Label("Base", classes="table-header")
                yield Label("VA", classes="table-header")
                yield Label("Read", classes="table-header")
                yield Label("Int.", classes="table-header")
                yield Label("Bif.", classes="table-header")
                yield Label("Mul.", classes="table-header")
                yield Label("High", classes="table-header")
                yield Label("PD", classes="table-header")

                # Right eye row
                yield Label("R", classes="table-label")
                yield TableInput(field_id="r_va", classes="table-input")
                yield TableInput(field_id="r_sph", classes="table-input")
                yield TableInput(field_id="r_cyl", classes="table-input")
                yield TableInput(field_id="r_axis", classes="table-input")
                yield TableInput(field_id="r_prism", classes="table-input")
                yield TableInput(field_id="r_base", classes="table-input")
                yield TableInput(field_id="r_add", classes="table-input")
                yield TableInput(field_id="r_read", classes="table-input")
                yield TableInput(field_id="r_int", classes="table-input")
                yield TableInput(field_id="r_bif", classes="table-input")
                yield TableInput(field_id="r_mul", classes="table-input")
                yield TableInput(field_id="r_high", classes="table-input")
                yield Label("", classes="table-label")

                # Left eye row
                yield Label("L", classes="table-label")
                yield TableInput(field_id="l_va", classes="table-input")
                yield TableInput(field_id="l_sph", classes="table-input")
                yield TableInput(field_id="l_cyl", classes="table-input")
                yield TableInput(field_id="l_axis", classes="table-input")
                yield TableInput(field_id="l_prism", classes="table-input")
                yield TableInput(field_id="l_base", classes="table-input")
                yield TableInput(field_id="l_add", classes="table-input")
                yield TableInput(field_id="l_read", classes="table-input")
                yield TableInput(field_id="l_int", classes="table-input")
                yield TableInput(field_id="l_bif", classes="table-input")
                yield TableInput(field_id="l_mul", classes="table-input")
                yield TableInput(field_id="l_high", classes="table-input")
                yield TableInput(field_id="pd", classes="table-input")

            # Additional notes section
            with Vertical(id="notes-section"):
                yield Label("Notes and Details:", id="notes-label")
                yield Input(placeholder="Notes...", id="notes-input")

    def on_mount(self) -> None:
        """Load initial data"""
        self.load_exam_data()

    def load_exam_data(self):
        """Load data for current exam into the table"""
        if not self.exams or self.current_exam_index < 0 or self.current_exam_index >= len(self.exams):
            return

        exam = self.exams[self.current_exam_index]

        field_map = {
            "r_va": exam.r_va or "6/24",
            "r_sph": exam.r_sph or "-1.75",
            "r_cyl": exam.r_cyl or "-0.50",
            "r_axis": exam.r_axis or "180",
            "r_prism": exam.r_prism or ".",
            "r_base": exam.r_base or "",
            "r_add": exam.r_add or "6/6",
            "r_read": exam.r_read or ".",
            "r_int": exam.r_int or ".",
            "r_bif": exam.r_bif or ".",
            "r_mul": exam.r_mul or "",
            "r_high": exam.r_high or "",
            "l_va": exam.l_va or "6/24",
            "l_sph": exam.l_sph or "-1.75",
            "l_cyl": exam.l_cyl or ".",
            "l_axis": exam.l_axis or "",
            "l_prism": exam.l_prism or ".",
            "l_base": exam.l_base or "",
            "l_add": exam.l_add or "6/6",
            "l_read": exam.l_read or ".",
            "l_int": exam.l_int or ".",
            "l_bif": exam.l_bif or ".",
            "l_mul": exam.l_mul or "",
            "l_high": exam.l_high or "",
            "pd": exam.pd or "58/",
        }

        for field_id, value in field_map.items():
            try:
                inputs = self.query(TableInput)
                for inp in inputs:
                    if inp.field_id == field_id:
                        inp.value = value
                        break
            except NoMatches:
                pass

        # Update dates
        date_label = self.query_one("#exam-dates", Label)
        date_label.update(f"Check: {exam.check_date} | Follow-up: {exam.exam_date}")

        # Update exam navigator
        navigator = self.query_one(ExamNavigator)
        navigator.update_exam(self.current_exam_index + 1)

        # Update notes
        notes_input = self.query_one("#notes-input", Input)
        notes_input.value = exam.notes

    def action_next_exam(self):
        """Navigate to next exam"""
        if self.current_exam_index < len(self.exams) - 1:
            self.current_exam_index += 1
            self.load_exam_data()

    def action_prev_exam(self):
        """Navigate to previous exam"""
        if self.current_exam_index > 0:
            self.current_exam_index -= 1
            self.load_exam_data()

    def on_key(self, event) -> None:
        """Handle keyboard navigation based on mode"""
        # Check if any input field has focus
        focused = self.screen.focused

        # If an input is focused, we're in edit mode
        if isinstance(focused, (TableInput, Input)):
            self.edit_mode = True
            # Allow Escape to unfocus and return to navigation mode
            if event.key == "escape":
                self.screen.set_focus(None)
                self.edit_mode = False
                event.prevent_default()
                event.stop()
        else:
            self.edit_mode = False

        # In navigation mode, +/- navigate between exams
        if not self.edit_mode:
            if event.key in ("plus", "equals"):
                self.action_next_exam()
                event.prevent_default()
                event.stop()
            elif event.key == "minus":
                self.action_prev_exam()
                event.prevent_default()
                event.stop()


class GlassesCheckApp(App):
    """Main application"""

    BINDINGS = [
        Binding("tab", "focus_next", "Next Field", show=True),
        Binding("shift+tab", "focus_previous", "Prev Field", show=True),
        Binding("plus,equals", "app_next_exam", "Next Exam", show=True),
        Binding("minus", "app_prev_exam", "Prev Exam", show=True),
        Binding("escape", "quit", "Quit", show=True),
    ]

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
        background: #0000aa;
        color: white;
        border: thick cyan;
    }

    CustomerInfo {
        width: 100%;
        height: 3;
        background: cyan;
        color: black;
        text-align: center;
        content-align: center middle;
        text-style: bold;
    }

    #exam-header {
        width: 100%;
        height: 3;
        background: #0000aa;
        padding: 0 2;
    }

    ExamNavigator {
        width: 30%;
        color: yellow;
        text-style: bold;
    }

    #exam-dates {
        width: 70%;
        color: white;
        text-align: right;
        text-style: bold;
    }

    /* Added grid layout with borders for table */
    #exam-table {
        grid-size: 14 3;
        grid-gutter: 1;
        width: 100%;
        height: auto;
        background: #0000aa;
        margin: 1 2;
        padding: 1;
        border: solid white;
    }

    .table-header {
        width: 100%;
        height: 3;
        background: #0000aa;
        color: yellow;
        text-style: bold;
        text-align: center;
        content-align: center middle;
        border: solid white;
    }

    .table-label {
        width: 100%;
        height: 3;
        background: #0000aa;
        color: white;
        text-style: bold;
        text-align: center;
        content-align: center middle;
        border: solid white;
    }

    .table-input {
        width: 100%;
        height: 3;
        background: #0000aa;
        color: white;
        text-align: center;
        border: solid white;
    }

    .table-input:focus {
        background: #0000dd;
        border: double yellow;
    }

    #notes-section {
        width: 100%;
        height: auto;
        padding: 1 2;
        background: #0000aa;
    }

    #notes-label {
        color: yellow;
        text-style: bold;
        margin-bottom: 1;
    }

    #notes-input {
        width: 100%;
        background: #0000dd;
        color: white;
    }

    Input {
        border: solid cyan;
    }

    Input:focus {
        border: double yellow;
    }
    """

    TITLE = "Glasses Check - Optics Shop CRM"

    def compose(self) -> ComposeResult:
        exams = [
            ExamData(
                exam_date="15/07/24",
                check_date="15/07/22",
                check_num="1",
                r_sph="-1.75", r_cyl="-0.50", r_axis="180",
                r_va="6/24", r_add="6/6", r_read=".",
                l_sph="-1.75", l_va="6/24", l_add="6/6",
                pd="58/",
                notes="Check only - no changes"
            ),
            ExamData(
                exam_date="15/07/24",
                check_date="15/07/22",
                check_num="2",
                r_sph="-1.75", r_cyl="-0.50", r_axis="180",
                r_va="6/24", r_add="6/6",
                l_sph="-1.75", l_va="6/24", l_add="6/6",
                pd="58/"
            ),
            ExamData(
                exam_date="15/07/24",
                check_date="15/07/22",
                check_num="3",
                r_sph="-1.75", r_cyl="-0.50", r_axis="180",
                r_va="6/24", r_add="6/6",
                l_sph="-1.75", l_va="6/24", l_add="6/6",
                pd="58/"
            ),
            ExamData(
                exam_date="15/07/24",
                check_date="15/07/22",
                check_num="4",
                r_sph="-1.75", r_cyl="-0.50", r_axis="180",
                r_va="6/24", r_add="6/6",
                l_sph="-1.75", l_va="6/24", l_add="6/6",
                pd="58/"
            ),
            ExamData(
                exam_date="15/07/24",
                check_date="15/07/22",
                check_num="5",
                r_sph="-1.75", r_cyl="-0.50", r_axis="180",
                r_va="6/24", r_add="6/6", r_read=".", r_int=".", r_bif=".",
                l_sph="-1.75", l_cyl=".", l_va="6/24", l_add="6/6",
                l_read=".", l_int=".", l_bif=".",
                pd="58/",
                notes="Follow-up / Check only - no changes"
            ),
        ]

        yield GlassesCheckWindow(
            customer_name="John Smith",
            customer_phone="04-6784163",
            customer_id="Test123",
            exams=exams
        )

    def action_app_next_exam(self):
        """Show next exam binding"""
        pass  # Actual handling is in GlassesCheckWindow.on_key

    def action_app_prev_exam(self):
        """Show prev exam binding"""
        pass  # Actual handling is in GlassesCheckWindow.on_key


if __name__ == "__main__":
    app = GlassesCheckApp()
    app.run()
