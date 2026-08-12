#!/bin/bash
echo "⏳ Waiting 6 seconds for Ngrok to establish a secure tunnel connection..."
sleep 6

# Query the correct local agent API endpoint directly
TUNNEL_URL=$(curl -s http://127.0.0 | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data['tunnels'] else '')" 2>/dev/null)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ Error: Ngrok tunnel is still uninitialized. Let's try running your launcher fresh."
else
    echo "🎯 Live Webhook Endpoint Active: $TUNNEL_URL"
    echo "🔄 Syncing endpoint parameters with Vapi servers..."
    
    python3 - <<CODE
import requests

API_KEY = "67cd00d8-e651-41c4-ac34-5d8a766212c0"
ASSISTANT_ID = "cc6a3ba6-68c6-41b7-96ab-e023b97a2e37"
URL = f"https://vapi.ai{ASSISTANT_ID}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": {
        "provider": "custom-llm",
        "model": "custom-llm",
        "url": "${TUNNEL_URL}/vapi/chat"
    }
}

response = requests.patch(URL, headers=headers, json=payload)
if response.status_code in [200, 201]:
    print("✅ Vapi Assistant successfully re-routed to your active tunnel!")
else:
    print("❌ Vapi sync failed:", response.status_code, response.text)
CODE
fi
