from dataclasses import dataclass

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
