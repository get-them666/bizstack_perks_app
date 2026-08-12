import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def send_mock_data():
    print("📤 Simulating incoming High-Ticket Financing Lead...")
    lead_payload = {"business_name": "O'Leary Enterprises LLC", "annual_revenue": 1250000.0, "credit_score": 765}
    try:
        r = requests.post(f"{BASE_URL}/financing/apply", json=lead_payload, timeout=5)
        print(f"Financing Lead Endpoint Status: {r.status_code} | Response: {r.text}")
    except Exception as e: print(f"Error testing lead channel: {e}")

    print("\n📤 Simulating incoming Paid Premium Conversion Checkout...")
    order_payload = {"user_id": "8844949255", "charge_id": "ch_stripe_live_test_9921", "amount": 49.00, "currency": "USD"}
    try:
        r = requests.post(f"{BASE_URL}/orders/log", json=order_payload, timeout=5)
        print(f"Monetization Order Endpoint Status: {r.status_code} | Response: {r.text}")
    except Exception as e: print(f"Error testing payment channel: {e}")

if __name__ == "__main__":
    send_mock_data()
