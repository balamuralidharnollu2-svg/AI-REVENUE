import sqlite3
import uuid

connection = sqlite3.connect("revenue_recovery.db")
cursor = connection.cursor()

event_id = str(uuid.uuid4())

# 1. events
cursor.execute(
    """
    INSERT INTO events (id, type, customer_id, source, raw_payload, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (event_id, "payment_failed", "cust_001", "stripe",
     '{"reason": "insufficient_funds"}', "diagnosed"),
)

# 2. diagnoses
cursor.execute(
    """
    INSERT INTO diagnoses (event_id, reason_category, confidence, explanation)
    VALUES (?, ?, ?, ?)
    """,
    (event_id, "insufficient_funds", 0.92,
     "Card declined due to insufficient funds on the linked bank account."),
)

# 3. decisions
cursor.execute(
    """
    INSERT INTO decisions (event_id, action, params, requires_human)
    VALUES (?, ?, ?, ?)
    """,
    (event_id, "retry_payment", '{"delay_hours": 48, "max_retries": 3}', 0),
)

# 4. actions_log
cursor.execute(
    """
    INSERT INTO actions_log (id, event_id, action, result, detail)
    VALUES (?, ?, ?, ?, ?)
    """,
    (str(uuid.uuid4()), event_id, "retry_payment", "success",
     "Payment retried successfully after 48 hour delay."),
)

connection.commit()
connection.close()

print("Seeded one full event trail across all four tables.")
