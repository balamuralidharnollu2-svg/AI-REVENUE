import sys
import os
import json
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_connection
from execute.action_router import route


def run_execution():
    connection = get_connection()
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

    for event_id, customer_id, raw_payload_str, action, params_json in decided_events:
        params = json.loads(params_json) if params_json else {}
        payload = json.loads(raw_payload_str) if raw_payload_str else {}

        if action == "retry_payment":
            params["amount"] = payload.get("amount", 0)

        if action == "escalate_human" and "reason" not in params:
            params["reason"] = "No specific reason provided by decision engine."

        result = route(action, params, customer_id)

        action_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO actions_log (id, event_id, action, result, detail)
            VALUES (?, ?, ?, ?, ?)
            """,
            (action_id, event_id, action, result["status"], result["detail"]),
        )

        final_status = "resolved" if result["status"] == "success" else "failed"
        cursor.execute(
            "UPDATE events SET status = ? WHERE id = ?",
            (final_status, event_id),
        )

        print(f"  -> Executed action={action} for event {event_id}: status={result['status']}")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    run_execution()