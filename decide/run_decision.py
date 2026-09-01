import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_connection
from decide.decision_engine import decide


def run_decision():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT e.id, e.raw_payload, d.reason_category
        FROM events e
        JOIN diagnoses d ON e.id = d.event_id
        LEFT JOIN decisions dec ON e.id = dec.event_id
        WHERE e.status = 'diagnosed' AND dec.event_id IS NULL
        """
    )
    diagnosed_events = cursor.fetchall()
    print(f"Found {len(diagnosed_events)} diagnosed event(s) to decide on.")

    for event_id, raw_payload_str, reason_category in diagnosed_events:
        order_value = 0
        if raw_payload_str:
            try:
                payload = json.loads(raw_payload_str)
                order_value = payload.get("amount", 0)
            except Exception:
                pass

        result = decide(reason_category, order_value=order_value)

        cursor.execute(
            """
            INSERT INTO decisions (event_id, action, params, requires_human)
            VALUES (?, ?, ?, ?)
            """,
            (event_id, result["action"], json.dumps(result["params"]), int(result["requires_human"])),
        )

        new_status = "escalated" if result["requires_human"] else "decided"
        cursor.execute(
            "UPDATE events SET status = ? WHERE id = ?",
            (new_status, event_id),
        )

        print(f"  -> Decided for event {event_id}: action={result['action']}, requires_human={result['requires_human']}")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    run_decision()