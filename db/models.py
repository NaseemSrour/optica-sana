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
class GlassesTest:
    """
    Represents a single glasses exam for a given customer (patient).
    """

    id: int
    customer_id: int  # Foreign key -> customers.id

    # --- Exam metadata ---
    exam_date: datetime  # When the test was performed
    examiner: Optional[str] = None  # Who performed the glasses test

    # --- Right Eye (OD) values ---
    r_fv_numerator: Optional[int] = None
    r_fv_denominator: Optional[int] = None
    r_sphere: Optional[float] = None
    r_cylinder: Optional[float] = None
    r_axis: Optional[int] = None
    r_prism: Optional[float] = None
    r_base: Optional[str] = None
    r_va: Optional[
        str] = None  # Visual Acuity (e.g., "6/6", "20/20") ??????????????????? Split into numerator/denomiator ?
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
    pupil_distance: Optional[float] = None  # ??????????? Split into numerator/denomiator ? Eza aa, change it as well in the validations!
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

    diagnosis: Optional[str] = None  # Free text: "Myopia", "Astigmatism"...
    notes: Optional[str] = None

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return GlassesTest(**dict(row))


@dataclass
class ContactLensesTest:
    id: Optional[int]  # AUTOINCREMENT PK
    customer_id: int
    exam_date: datetime  # ISO date string
    examiner: Optional[str]

    # ===== Keratometry =====
    r_rH: Optional[float]
    r_rV: Optional[float]
    r_aver: Optional[float]
    r_k_cyl: Optional[float]
    r_axH: Optional[int]
    r_rT: Optional[float]
    r_rN: Optional[float]
    r_rI: Optional[float]
    r_rS: Optional[float]

    l_rH: Optional[float]
    l_rV: Optional[float]
    l_aver: Optional[float]
    l_k_cyl: Optional[float]
    l_axH: Optional[int]
    l_rT: Optional[float]
    l_rN: Optional[float]
    l_rI: Optional[float]
    l_rS: Optional[float]

    # ===== Contact Lens Prescription (Right) =====
    r_lens_type: Optional[str]
    r_manufacturer: Optional[str]
    r_brand: Optional[str]
    r_diameter: Optional[float]
    r_base_curve_numerator: Optional[float]
    r_base_curve_denominator: Optional[float]
    r_lens_sph: Optional[float]
    r_lens_cyl: Optional[float]
    r_lens_axis: Optional[int]
    r_material: Optional[str]
    r_tint: Optional[str]
    r_lens_va_numerator: Optional[int]
    r_lens_va_denominator: Optional[int]

    # ===== Contact Lens Prescription (Left) =====
    l_lens_type: Optional[str]
    l_manufacturer: Optional[str]
    l_brand: Optional[str]
    l_diameter: Optional[float]
    l_base_curve_numerator: Optional[float]
    l_base_curve_denominator: Optional[float]
    l_lens_sph: Optional[float]
    l_lens_cyl: Optional[float]
    l_lens_axis: Optional[int]
    l_material: Optional[str]
    l_tint: Optional[str]
    l_lens_va_numerator: Optional[int]
    l_lens_va_denominator: Optional[int]

    notes: Optional[str]

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return ContactLensesTest(**dict(row))

