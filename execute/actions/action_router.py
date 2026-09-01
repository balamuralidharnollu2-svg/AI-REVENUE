import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execute.actions.retry_payment import retry_payment
from execute.actions.send_update_link import send_update_link
from execute.actions.offer_discount import offer_discount
from execute.actions.escalate_human import escalate_human

ACTION_MAP = {
    "retry_payment": retry_payment,
    "send_update_link": send_update_link,
    "offer_discount": offer_discount,
    "escalate_human": escalate_human,
}


def route(action, params, customer_id):
    fn = ACTION_MAP.get(action)

    if fn is None:
        return {
            "result": "failure",
            "detail": f"Unknown action '{action}' - no function registered for it.",
        }

    try:
        return fn(customer_id=customer_id, **params)
    except TypeError as e:
        return {
            "result": "failure",
            "detail": f"Action '{action}' failed to run with params {params}: {e}",
        }