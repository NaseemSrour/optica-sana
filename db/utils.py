from dataclasses import fields
from datetime import datetime

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"


def dict_from_row(row):
    """Converts sqlite3.Row to a plain dict."""
    return dict(row) if row else None


def row_to_dataclass(row, cls):
    """Convert sqlite3.Row to a dataclass instance."""
    if row is None:
        return None
    # Only include the fields that exist in the dataclass
    data = {f.name: row[f.name] for f in fields(cls) if f.name in row.keys()}
    return cls(**data)


def date_to_str(my_date):
    return my_date.strftime("%d/%m/%Y")


def str_to_date(date_str):
    dt_obj = datetime.strptime(date_str, "%d/%m/%Y")  # the input string's format
    return dt_obj


def datetime_to_text(dt: datetime) -> str:
    """Convert datetime to ISO8601 text for SQLite."""
    return dt.strftime(ISO_FORMAT)


def text_to_datetime(text: str) -> datetime:
    """Convert stored ISO8601 text back to datetime."""
    return datetime.strptime(text, ISO_FORMAT)
