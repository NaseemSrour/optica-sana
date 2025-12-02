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
    r_sphere: Optional[float] = None
    r_cylinder: Optional[float] = None
    r_axis: Optional[int] = None
    r_add: Optional[float] = None  # Presbyopia addition
    r_va: Optional[str] = None     # Visual Acuity (e.g., "6/6", "20/20")

    # --- Left Eye (OS) values ---
    l_sphere: Optional[float] = None
    l_cylinder: Optional[float] = None
    l_axis: Optional[int] = None
    l_add: Optional[float] = None
    l_va: Optional[str] = None

    # --- Symptoms / Notes ---
    pupil_distance: Optional[float] = None
    diagnosis: Optional[str] = None   # Free text: "Myopia", "Astigmatism"...
    notes: Optional[str] = None

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return RefractionTest(**dict(row))

