from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    id: int
    ssn: str
    fname: str
    lname: str
    phone: str
    town: str
    notes: str

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Customer(**dict(row))

@dataclass
class RefractionTest:
    """
    Represents a single refraction exam for a given customer (patient).
    """

    id: int
    customer_id: int       # Foreign key -> customers.id

    # --- Exam metadata ---
    exam_date: datetime    # When the test was performed
    examiner: Optional[str] = None  # Who performed the refraction

    # --- Right Eye (OD) values ---
    od_sphere: Optional[float] = None
    od_cylinder: Optional[float] = None
    od_axis: Optional[int] = None
    od_add: Optional[float] = None  # Presbyopia addition
    od_va: Optional[str] = None     # Visual Acuity (e.g., "6/6", "20/20")

    # --- Left Eye (OS) values ---
    os_sphere: Optional[float] = None
    os_cylinder: Optional[float] = None
    os_axis: Optional[int] = None
    os_add: Optional[float] = None
    os_va: Optional[str] = None

    # --- Symptoms / Notes ---
    pupil_distance: Optional[float] = None
    diagnosis: Optional[str] = None   # Free text: "Myopia", "Astigmatism"...
    notes: Optional[str] = None

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return RefractionTest(**dict(row))

