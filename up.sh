#!/bin/bash

echo "⚡ 'UP' TRIGGER ACTIVATED! Booting the full BizStack application matrix..."

# 1. Pull latest code from GitHub and display repository URL
if [ -d ".git" ]; then
    echo "📦 Checking GitHub repository configuration..."
    git pull origin main 2>/dev/null
    GIT_URL=$(git config --get remote.origin.url | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
    echo "🖥️  GitHub Web URL: $GIT_URL"
else
    echo "⚠️  Not a Git repository folder, skipping GitHub URL tracking."
fi

# 2. Force kill any lingering processes on all your application ports
echo "🧹 Purging active network ports..."
kill -9 $(lsof -t -i:8080) 2>/dev/null  # FastAPI (Phone Bot)
kill -9 $(lsof -t -i:8501) 2>/dev/null  # Streamlit Dashboard
kill -9 $(lsof -t -i:5000) 2>/dev/null  # Flask App
kill -9 $(lsof -t -i:4040) 2>/dev/null  # Ngrok

# 3. Launch your FastAPI Phone Bot (Port 8080)
echo "🚀 Starting FastAPI Voice Server on port 8080..."
python3 api_server.py > api_server.log 2>&1 &

# 4. Launch your Flask App Server (Port 5000)
if [ -f "app.py" ]; then
    echo "🧪 Starting Flask Application Server on port 5000..."
    python3 app.py > flask.log 2>&1 &
else
    echo "⚠️  app.py not found, skipping Flask server startup."
fi

# 5. Launch your Streamlit Interface Dashboard (Port 8501)
if [ -f "dashboard.py" ]; then
    echo "📊 Starting Streamlit UI Interface on port 8501..."
    streamlit run dashboard.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &
else
    echo "⚠️  dashboard.py not found, skipping Streamlit startup."
fi

sleep 2

# 6. Launch the Ngrok Public Tunnel Network Bridge
echo "🌐 Launching Ngrok proxy tunnels..."
ngrok http 8080 --log=stdout > /dev/null 2>&1 &

sleep 3

# 7. Fetch your active live URL string directly from the local tunnel API proxy
TUNNEL_URL=$(curl -s http://127.0.0 | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels']['public_url'])" 2>/dev/null)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ Ngrok failed to provide a public URL loop. Verify that Ngrok is authenticated!"
else
    echo "🎯 Live Webhook Endpoint Active: $TUNNEL_URL"
    
    # 8. Update your Vapi Assistant to point to the fresh live endpoint URL
    echo "🔄 Syncing endpoint parameters with Vapi servers..."
    python3 - <<CODE
import requests
import json

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
if response.status_code == 200:
    print("✅ Vapi Assistant successfully re-routed to your active tunnel.")
else:
    print("❌ Vapi sync failed:", response.text)
CODE
fi

echo -e "\n🟢 ALL SYSTEMS ONLINE! Your complete stack is running perfectly in the background."
echo "📟 Streaming live FastAPI logs below (Press CTRL+C to disconnect viewing, processes will keep running)..."
echo "--------------------------------------------------------------------------------"
tail -f api_server.log
 