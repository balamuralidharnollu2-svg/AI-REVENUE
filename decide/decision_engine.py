import json
import os

RULES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.json")
HIGH_VALUE_THRESHOLD = 500  # dollars - guardrail: force human escalation above this

with open(RULES_PATH, "r") as f:
    RULES = json.load(f)


def decide(reason_category, order_value=0):
    """
    Turns a diagnosis reason into a bounded decision.

    Args:
        reason_category (str): one of the categories from diagnose (e.g. "insufficient_funds")
        order_value (float): dollar value tied to this event, used for the guardrail check

    Returns:
        dict: {"action": ..., "params": {...}, "requires_human": bool}
    """
    rule = RULES.get(reason_category, RULES["unknown"])

    action = rule["action"]
    params = rule["params"]
    requires_human = action == "escalate_human"

    # GUARDRAIL: no matter what the rules say, high-value events always go to a human
    if order_value > HIGH_VALUE_THRESHOLD:
        action = "escalate_human"
        params = {"reason": f"order_value ${order_value} exceeds threshold ${HIGH_VALUE_THRESHOLD}"}
        requires_human = True

    return {
        "action": action,
        "params": params,
        "requires_human": requires_human,
    }