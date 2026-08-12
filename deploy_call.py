import requests
import json

# Setup configuration properties targeting your active account environment
API_KEY = "67cd00d8-e651-41c4-ac34-5d8a766212c0"
URL = "https://vapi.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "customer": {
        "number": "+12526655891" # Your mobile device number
    },
    "assistant": {
        "firstMessage": "Hi Shaun! This is your live conversational BizStack agent syncing cleanly from your python codebase. What would you like to know about our perks system?",
        "model": {
            "provider": "custom-llm",
            "url": "https://ngrok-free.dev"
        },
        "voice": {
            "provider": "playht",
            "voiceId": "susan"
        }
    }
}

print("🚀 Dispatching outbound testing data streams directly to your platform line...")
response = requests.post(URL, headers=headers, data=json.dumps(payload))

if response.status_code == 201 or response.status_code == 200:
    print("✅ System confirmation: Outbound call successfully processed by Vapi servers!")
else:
    print(f"❌ Target request failed with code: {response.status_code}")
    print("Error Details:", response.text)
