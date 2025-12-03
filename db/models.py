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
    r_fv_numerator: Optional[int] = None
    r_fv_denominator: Optional[int] = None
    r_sphere: Optional[float] = None
    r_cylinder: Optional[float] = None
    r_axis: Optional[int] = None
    r_prism: Optional[float] = None
    r_base: Optional[str] = None
    r_va: Optional[str] = None  # Visual Acuity (e.g., "6/6", "20/20") ??????????????????? Split into numerator/denomiator ?
    r_add_read: Optional[float] = None  # Presbyopia addition
    r_add_int: Optional[float] = None
    r_add_bif: Optional[float] = None
    r_add_mul: Optional[float] = None
    r_high: Optional[float] = None  # ????????????????

    # --- Left Eye (OS) values ---
    l_fv_numerator: Optional[int] = None
    l_fv_denominator: Optional[int] = None
    l_sphere: Optional[float] = None
    l_cylinder: Optional[float] = None
    l_axis: Optional[int] = None
    l_prism: Optional[float] = None
    l_base: Optional[str] = None
    l_va: Optional[str] = None
    l_add_read: Optional[float] = None  # Presbyopia addition
    l_add_int: Optional[float] = None
    l_add_bif: Optional[float] = None
    l_add_mul: Optional[float] = None
    l_high: Optional[float] = None  # ????????????????

    # --- Symptoms / Notes ---
    pupil_distance: Optional[float] = None  # ??????????? Split into numerator/denomiator ?
    dominant_eye: Optional[str] = None
    iop: Optional[str] = None  # ??????????? String? Or what? R/L ?
    glasses_role: Optional[str] = None  # tafked meshkfaim
    lenses_material: Optional[str] = None
    lenses_diameter: Optional[float] = None  # ???????????????? something / something ????
    segment_diameter: Optional[float] = None
    lenses_manufacturer: Optional[str] = None
    lenses_color: Optional[str] = None
    ######### V? H?   "Dest"? In the middle of the picture
    catalog_num: Optional[str] = None
    frame_manufacturer: Optional[str] = None
    frame_supplier: Optional[str] = None
    frame_model: Optional[str] = None
    frame_size: Optional[str] = None
    frame_bar_length: Optional[str] = None
    frame_color: Optional[str] = None

    diagnosis: Optional[str] = None   # Free text: "Myopia", "Astigmatism"...
    notes: Optional[str] = None

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return RefractionTest(**dict(row))

