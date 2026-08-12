import requests

URL = "https://vapi.ai"
HEADERS = {
    "Authorization": "Bearer 67cd00d8-e651-41c4-ac34-5d8a766212c0",
    "Content-Type": "application/json"
}
PAYLOAD = {
    "assistantId": "b674d4e0-d227-46bc-9577-f1e6649e3fce",
    "phoneNumberId": "4c89a2d8-4e76-4802-85d8-4ab6000dc297",
    "customer": {
        "number": "+12526655891"
    }
}

def fire_call():
    print("📞 Triggering live production voice call via Vapi...")
    try:
        r = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=10)
        
        # Fixed condition statement check
        if r.status_code == 200 or r.status_code == 201:
            print(f"✅ Call Dispatched Successfully! (Status Code: {r.status_code})")
            if r.text:
                try:
                    print(f"🆔 Tracking ID: {r.json().get('id')}")
                except Exception:
                    pass
        else:
            print(f"❌ Refused. Status: {r.status_code} | Body: {r.text}")
    except Exception as e:
        print(f"❌ Fatal Network Protocol Error: {e}")

if __name__ == "__main__":
    fire_call()
