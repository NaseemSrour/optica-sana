from dataclasses import fields


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