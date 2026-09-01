import sqlite3
import uuid
from datetime import date, timedelta

connection = sqlite3.connect("revenue_recovery.db")
cursor = connection.cursor()

# Create table if not exists
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS invoices (
        id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        amount REAL NOT NULL,
        due_date TEXT NOT NULL,
        status TEXT NOT NULL,
        converted_to_event INTEGER DEFAULT 0
    )
    """
)

today = date.today()

invoices = [
    # overdue, unpaid -> scanner SHOULD catch this one
    (str(uuid.uuid4()), "cust_002", 1200.00, str(today - timedelta(days=10)), "unpaid", 0),
    # not due yet -> scanner should NOT catch this one
    (str(uuid.uuid4()), "cust_003", 450.00, str(today + timedelta(days=5)), "unpaid", 0),
    # overdue but already paid -> scanner should NOT catch this one
    (str(uuid.uuid4()), "cust_004", 800.00, str(today - timedelta(days=15)), "paid", 0),
]

cursor.executemany(
    """
    INSERT INTO invoices (id, customer_id, amount, due_date, status, converted_to_event)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    invoices,
)

connection.commit()
connection.close()

print("Seeded 3 fake invoices (1 should trigger an overdue event, 2 should not).")