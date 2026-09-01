import sqlite3

connection = sqlite3.connect("revenue_recovery.db")
cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        e.id, e.type, e.customer_id, e.status,
        d.reason_category, d.confidence,
        dec.action, dec.requires_human,
        a.result, a.detail
    FROM events e
    LEFT JOIN diagnoses d ON e.id = d.event_id
    LEFT JOIN decisions dec ON e.id = dec.event_id
    LEFT JOIN actions_log a ON e.id = a.event_id
    """
)

for row in cursor.fetchall():
    print(row)

connection.close()