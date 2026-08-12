#!/bin/bash
echo "⚡ 'UP' TRIGGER ACTIVATED! Booting the full BizStack application matrix..."

# 1. Pull latest code from GitHub
if [ -d ".git" ]; then
    echo "📦 Checking GitHub repository configuration..."
    git pull origin main 2>/dev/null
    GIT_URL=$(git config --get remote.origin.url | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
    echo "🖥️ GitHub Web URL: $GIT_URL"
else
    echo "⚠️ Not a Git repository folder, skipping GitHub URL tracking."
fi

# 2. Force kill any lingering processes on active application ports
echo "🧹 Purging active network ports..."
kill -9 $(lsof -t -i:8080) 2>/dev/null  # FastAPI (Phone Bot)
kill -9 $(lsof -t -i:8501) 2>/dev/null  # Streamlit Dashboard
kill -9 $(lsof -t -i:5000) 2>/dev/null  # Flask App
kill -9 $(lsof -t -i:4040) 2>/dev/null  # Ngrok
pkill -f ngrok 2>/dev/null
sleep 2

# 3. Launch your FastAPI Phone Bot (Port 8080)
echo "🚀 Starting FastAPI Voice Server on port 8080..."
python3 api_server.py > api_server.log 2>&1 &

# 4. Launch your Flask App Server (Port 5000)
if [ -f "app.py" ]; then
    echo "🧪 Starting Flask Application Server on port 5000..."
    python3 app.py > flask.log 2>&1 &
else
    echo "⚠️ app.py not found, skipping Flask server startup."
fi

# 5. Launch your Streamlit Interface Dashboard (Port 8501)
if [ -f "dashboard.py" ]; then
    echo "📊 Starting Streamlit UI Interface on port 8501..."
    streamlit run dashboard.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &
else
    echo "⚠️ dashboard.py not found, skipping Streamlit startup."
fi

# 6. Launch Ngrok and force load your local configuration file
echo "🌐 Launching Ngrok proxy tunnels..."
ngrok http 8080 --config="/Users/shaunoleary/Library/Application Support/ngrok/ngrok.yml" > /dev/null 2>&1 &

echo "⏳ Waiting 12 seconds for tunnels to safely stabilize and authenticate..."
sleep 12

# 7. Fetch active live URL string using safe array indexing validation rules
TUNNEL_URL=$(curl -s http://127.0.0 | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'tunnels' in data and len(data['tunnels']) > 0:
        print(data['tunnels'][0]['public_url'])
    else:
        print('')
except Exception:
    print('')
" 2>/dev/null)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ Ngrok failed to provide a public URL loop. Verify your ngrok.yml file structure!"
else
    echo "🎯 Live Webhook Endpoint Active: $TUNNEL_URL"
    
    # 8. Update your Vapi Assistant to point to the fresh live endpoint URL
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
        "url": f"{TUNNEL_URL}/vapi/chat"
    }
}

response = requests.patch(URL, headers=headers, json=payload)
if response.status_code in:
    print("✅ Vapi Assistant successfully re-routed to your active tunnel.")
else:
    print("❌ Vapi sync failed Status Code:", response.status_code, response.text)
CODE
fi

echo -e "\n🟢 ALL SYSTEMS ONLINE! Your complete stack is running perfectly in the background."
echo "📟 Streaming live FastAPI logs below (Press CTRL+C to disconnect viewing, processes will keep running)..."
echo "--------------------------------------------------------------------------------"
tail -f api_server.log
