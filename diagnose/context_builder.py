import sqlite3
import json

def build_context(event_id):
    connection = sqlite3.connect("revenue_recovery.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, type, customer_id, raw_payload FROM events WHERE id = ?",
        (event_id,),
    )
    event = cursor.fetchone()
    connection.close()

    if event is None:
        raise ValueError(f"No event found with id {event_id}")

    event_id, event_type, customer_id, raw_payload = event

    fake_history = {
        "past_failed_payments": 1,
        "customer_since_days": 240,
        "total_lifetime_value": 1450.00,
    }

    context = {
        "event_type": event_type,
        "customer_id": customer_id,
        "raw_payload": json.loads(raw_payload),
        "customer_history": fake_history,
    }
    return context