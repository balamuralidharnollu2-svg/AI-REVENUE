def escalate_human(customer_id, reason=""):
    """Simulates escalating to a human by printing/logging instead of a real Slack alert."""
    print(f"ESCALATION: customer {customer_id} needs human review. Reason: {reason}")
    return {
        "result": "escalated",
        "detail": f"Escalated customer {customer_id} to human review. Reason: {reason}",
    }