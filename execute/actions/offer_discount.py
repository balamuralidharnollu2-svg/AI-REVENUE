def offer_discount(customer_id, max_percent=10):
    """Simulates generating and sending a discount code."""
    code = f"SAVE{max_percent}-{customer_id[:6].upper()}"
    print(f"Simulating discount offer to customer {customer_id}: code {code} ({max_percent}% off)")
    return {
        "result": "success",
        "detail": f"Discount code {code} sent to customer {customer_id} (simulated).",
    }