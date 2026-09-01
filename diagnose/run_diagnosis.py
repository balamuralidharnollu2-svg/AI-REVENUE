import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagnose.groq_client import diagnose
from diagnose.context_builder import build_context


def run_diagnosis():
    connection = sqlite3.connect("revenue_recovery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM events WHERE status = 'new'")
    new_events = cursor.fetchall()
    print(f"Found {len(new_events)} new event(s) to diagnose.")

    for (event_id,) in new_events:
        context = build_context(event_id)
        result = diagnose(context)

        cursor.execute(
            """
            INSERT INTO diagnoses (event_id, reason_category, confidence, explanation)
            VALUES (?, ?, ?, ?)
            """,
            (event_id, result["reason_category"], result["confidence"], result["explanation"]),
        )

        cursor.execute(
            "UPDATE events SET status = 'diagnosed' WHERE id = ?",
            (event_id,),
        )

        print(f"Diagnosed {event_id}: {result['reason_category']} (confidence {result['confidence']})")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    run_diagnosis()