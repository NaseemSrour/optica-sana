CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssn INTEGER NOT NULL,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            phone TEXT,
            town TEXT,
            notes TEXT
)