def send_update_link(customer_id, channel="email"):
    """Simulates sending a payment-method-update link to the customer."""
    fake_link = f"https://yourapp.example.com/update-payment?customer={customer_id}"
    print(f"Simulating {channel} to customer {customer_id}: 'Please update your payment method: {fake_link}'")
    return {
        "result": "success",
        "detail": f"Update link sent to customer {customer_id} via {channel} (simulated).",
    }