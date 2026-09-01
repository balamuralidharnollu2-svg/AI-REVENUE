import random
import time

def retry_payment(customer_id, amount, delay_hours=48, max_retries=3):
    """
    Simulates retrying a failed payment.
    In production, this would call a real payment gateway (Stripe/Razorpay).
    For this demo, it randomly succeeds or fails to mimic real-world behavior.
    """
    print(f"Simulating payment retry for customer {customer_id}, amount ${amount}...")
    print(f"(In production: would wait {delay_hours}h, retry up to {max_retries} times)")

    time.sleep(1)  # small pause so it feels like something is happening during a live demo

    # 80% chance of success, to feel realistic rather than always passing
    success = random.random() < 0.8

    if success:
        return {
            "result": "success",
            "detail": f"Payment of ${amount} for customer {customer_id} retried successfully (simulated).",
        }
    else:
        return {
            "result": "failure",
            "detail": f"Payment retry failed for customer {customer_id} after simulated attempts.",
        }