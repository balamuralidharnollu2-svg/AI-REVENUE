import sqlite3
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decide.decision_engine import decide


def run_decision():
    connection = sqlite3.connect("revenue_recovery.db")
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

    for event_id, raw_payload, reason_category in diagnosed_events:
        payload = json.loads(raw_payload)
        order_value = payload.get("amount", 0)

        result = decide(reason_category, order_value=order_value)

        cursor.execute(
            """
            INSERT INTO decisions (event_id, action, params, requires_human)
            VALUES (?, ?, ?, ?)
            """,
            (event_id, result["action"], json.dumps(result["params"]), int(result["requires_human"])),
        )

        cursor.execute(
            "UPDATE events SET status = 'decided' WHERE id = ?",
            (event_id,),
        )

        print(f"Decided {event_id}: {result['action']} (requires_human={result['requires_human']})")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    run_decision()