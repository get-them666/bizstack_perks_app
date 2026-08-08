import requests
url = "http://127.0.0"
payload = {"business_name": "OLeary Corporate Logistics", "annual_revenue": 2400000.0, "credit_score": 780, "business_address": "701 DANA DRIVE CHESAPEAKE, VA 23321"}
try:
    res = requests.post(url, json=payload, timeout=5)
    print("📊 Status Code:", res.status_code, "| Body:", res.json())
except Exception as e:
    print("❌ Connection error:", e)
