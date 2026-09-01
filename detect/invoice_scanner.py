import sys
import os
import uuid
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_connection

def scan_invoices():
    connection = get_connection()
    cursor = connection.cursor()

    today = str(date.today())

    cursor.execute(
        """
        SELECT id, customer_id, amount, due_date
        FROM invoices
        WHERE status = 'unpaid'
          AND due_date < ?
          AND converted_to_event = 0
        """,
        (today,),
    )

    overdue_invoices = cursor.fetchall()
    print(f"Found {len(overdue_invoices)} overdue invoice(s).")

    for invoice_id, customer_id, amount, due_date in overdue_invoices:
        event_id = str(uuid.uuid4())
        raw_payload = f'{{"invoice_id": "{invoice_id}", "amount": {amount}, "due_date": "{due_date}"}}'

        cursor.execute(
            """
            INSERT INTO events (id, type, customer_id, source, raw_payload, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (event_id, "invoice_overdue", customer_id, "invoice_scanner", raw_payload, "new"),
        )

        cursor.execute(
            "UPDATE invoices SET converted_to_event = 1 WHERE id = ?",
            (invoice_id,),
        )

        print(f"  -> Created event {event_id} for customer {customer_id} (amount: ${amount})")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    scan_invoices()