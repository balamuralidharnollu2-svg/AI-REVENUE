import sqlite3
import json
import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execute.action_router import route


def run_execution():
    connection = sqlite3.connect("revenue_recovery.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT e.id, e.customer_id, e.raw_payload, dec.action, dec.params
        FROM events e
        JOIN decisions dec ON e.id = dec.event_id
        LEFT JOIN actions_log a ON e.id = a.event_id
        WHERE e.status = 'decided' AND a.event_id IS NULL
        """
    )
    decided_events = cursor.fetchall()
    print(f"Found {len(decided_events)} decided event(s) to execute.")

    for event_id, customer_id, raw_payload, action, params_json in decided_events:
        params = json.loads(params_json)
        payload = json.loads(raw_payload)

        if action == "retry_payment":
            params["amount"] = payload.get("amount", 0)

        if action == "escalate_human" and "reason" not in params:
            params["reason"] = "No specific reason provided by decision engine."

        result = route(action, params, customer_id)

        cursor.execute(
            """
            INSERT INTO actions_log (id, event_id, action, result, detail)
            VALUES (?, ?, ?, ?, ?)
            """,
            (str(uuid.uuid4()), event_id, action, result["result"], result["detail"]),
        )

        new_status = "escalated" if result["result"] == "escalated" else "resolved"
        cursor.execute(
            "UPDATE events SET status = ? WHERE id = ?",
            (new_status, event_id),
        )

        print(f"Executed {event_id}: {action} -> {result['result']}")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    run_execution()