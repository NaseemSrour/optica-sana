from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, DataTable, Label
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
        return f"{self.customer_name:} | Phone: {self.customer_phone} | ID: {self.customer_id}"


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


class GlassesCheckWindow(Container):
    """Main Glasses Check window widget"""

    BINDINGS = [
        Binding("plus,equals", "next_exam", "Next Exam", show=False),
        Binding("minus", "prev_exam", "Previous Exam", show=False),
        Binding("tab", "next_field", "Next Field", show=False),
        Binding("shift+tab", "prev_field", "Previous Field", show=False),
        Binding("escape", "quit", "Quit", show=True),
    ]

    def __init__(self, customer_name: str, customer_phone: str, customer_id: str, exams: List[ExamData]):
        super().__init__()
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_id = customer_id
        self.exams = exams
        self.current_exam_index = len(exams) - 1  # Start with latest exam
        self.focusable_fields = []

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical(id="main-container"):
            # Customer info header
            yield CustomerInfo(self.customer_name, self.customer_phone, self.customer_id)

            # Exam navigator and dates
            with Horizontal(id="exam-header"):
                yield ExamNavigator(self.current_exam_index + 1, len(self.exams))
                yield Label(id="exam-dates")

            # Main data grid
            yield DataTable(id="exam-table", cursor_type="none")

            # Additional notes section
            with Vertical(id="notes-section"):
                yield Label("Notes and Details:", id="notes-label")
                yield Input(placeholder="Notes...", id="notes-input")

    def on_mount(self) -> None:
        """Setup the table and load initial data"""
        table = self.query_one("#exam-table", DataTable)

        # Add columns
        table.add_column("", width=6)
        table.add_column("FU", width=8)
        table.add_column("Sph.", width=8)
        table.add_column("Cyl.", width=8)
        table.add_column("Ax.", width=6)
        table.add_column("Pris", width=6)
        table.add_column("Base", width=6)
        table.add_column("VA", width=8)
        table.add_column("Read", width=6)
        table.add_column("Int.", width=6)
        table.add_column("Bif.", width=6)
        table.add_column("Mul.", width=6)
        table.add_column("High", width=6)
        table.add_column("PD", width=6)

        # Load current exam data
        self.load_exam_data()

    def load_exam_data(self):
        """Load data for current exam into the table"""
        if not self.exams or self.current_exam_index < 0 or self.current_exam_index >= len(self.exams):
            return

        exam = self.exams[self.current_exam_index]
        table = self.query_one("#exam-table", DataTable)

        # Clear existing rows
        table.clear()

        # Add right eye row
        table.add_row(
            "R",
            exam.r_va or "6/24",
            exam.r_sph or "-1.75",
            exam.r_cyl or "-0.50",
            exam.r_axis or "180",
            exam.r_prism or ".",
            exam.r_base or "",
            exam.r_add or "6/6",
            exam.r_read or ".",
            exam.r_int or ".",
            exam.r_bif or ".",
            exam.r_mul or "",
            exam.r_high or "",
            ""
        )

        # Add left eye row
        table.add_row(
            "L",
            exam.l_va or "6/24",
            exam.l_sph or "-1.75",
            exam.l_cyl or ".",
            exam.l_axis or "",
            exam.l_prism or ".",
            exam.l_base or "",
            exam.l_add or "6/6",
            exam.l_read or ".",
            exam.l_int or ".",
            exam.l_bif or ".",
            exam.l_mul or "",
            exam.l_high or "",
            exam.pd or "58/"
        )

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

    def action_next_field(self):
        """Move to next input field"""
        # For now, focus on notes input
        try:
            self.query_one("#notes-input", Input).focus()
        except NoMatches:
            pass

    def action_prev_field(self):
        """Move to previous input field"""
        pass


class GlassesCheckApp(App):
    """Main application"""

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

    #exam-table {
        width: 100%;
        height: auto;
        background: #0000aa;
        color: white;
        margin: 1 2;
    }

    DataTable {
        background: #0000aa;
        color: white;
    }

    DataTable > .datatable--header {
        background: #0000aa;
        color: yellow;
        text-style: bold;
    }

    DataTable > .datatable--cursor {
        background: #0000dd;
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
        # Sample exam data
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


if __name__ == "__main__":
    app = GlassesCheckApp()
    app.run()
