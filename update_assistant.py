import requests
import json

# Setup configuration properties targeting your active account environment
API_KEY = "67cd00d8-e651-41c4-ac34-5d8a766212c0"
ASSISTANT_ID = "cc6a3ba6-68c6-41b7-96ab-e023b97a2e37"
# Fixed explicit path string connection
URL = f"https://vapi.ai{ASSISTANT_ID}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Entire BizStack framework profile payload
payload = {
    "name": "BizStack Perks Message Agent",
    "firstMessage": "Thanks for checking out BizStack Perks! I can help answer questions about our rewards program or dashboard setup. What can I do for you today?",
    "model": {
        "provider": "custom-llm",
        "model": "custom-llm",
        "url": "https://ngrok-free.dev"
    },
    "systemPrompt": (
        "# Identity & Purpose\n"
        "You are Morgan, the official AI assistant for BizStack Perks. Your role is to handle inbound "
        "and outbound inquiries from users, providing helpful context regarding our platform features, "
        "integrated analytics tracking systems, and member rewards.\n\n"
        "# Style & Tone\n"
        "- Speak warmly, clearly, and conversationally.\n"
        "- Keep your answers highly concise (under two sentences max) so it sounds like a fast, natural phone conversation.\n"
        "- Do not repeat long code frameworks or technical logs over the voice lines.\n\n"
        "# Core Objectives\n"
        "- Answer customer questions regarding BizStack application dashboards.\n"
        "- If a caller expresses interest in setting up an account, ask for their preferred contact email address."
    )
}

print("⚡ Overwriting Assistant profile via API...")
response = requests.patch(URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("✅ Success! Assistant configuration fully updated inside your shell pipeline.")
else:
    print(f"❌ Configuration failed with code: {response.status_code}")
    print("Error Details:", response.text)
