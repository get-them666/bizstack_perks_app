#!/bin/bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FASTAPI_PORT="${FASTAPI_PORT:-8080}"
NGROK_API_LOCAL="${NGROK_API_LOCAL:-http://127.0.0.1:4040}"

echo "🚀 Starting All Backend Services Automatically..."

# 1. Kill any existing zombie server or tunnel processes
killall ngrok python3 python uvicorn 2>/dev/null || true

# 2. Fire up the Core Python App Servers in the background
echo "📦 Initializing Flask Ingestion App Server on port 8080..."
nohup python3 "$REPO_ROOT/app.py" > "$REPO_ROOT/flask_server.log" 2>&1 &

echo "⚡ Initializing FastAPI Matrix App Server on port 8000..."
nohup uvicorn api_server:app --port 8000 --host 0.0.0.0 > "$REPO_ROOT/api_server.log" 2>&1 &

sleep 2

# 3. Handle Cloudflare or Ngrok Network Tunnel Pipeline
if command -v cloudflared >/dev/null 2>&1 && [ -n "${CF_TUNNEL_NAME:-}" ]; then
    echo "🌐 Starting cloudflared tunnel for ${CF_TUNNEL_NAME}..."
    nohup cloudflared tunnel run "${CF_TUNNEL_NAME}" > "$REPO_ROOT/cloudflared.log" 2>&1 &
    if [ -n "${CF_INGRESS_HOST:-}" ]; then
        echo "🎯 Cloudflare Tunnel public hostname: https://${CF_INGRESS_HOST}"
    fi
else
    # Fall back to native ngrok behavior
    if command -v ngrok >/dev/null 2>&1; then
        export NGROK_AUTHTOKEN="${NGROK_AUTHTOKEN:-3Fv1rvZc5VvYThGCMBL9gsHiE78_4AC9GZ78t7M1uciSWy6H5}"
        echo "🌐 Starting ngrok network bridge map..."
        nohup ngrok http 8000 --authtoken="${NGROK_AUTHTOKEN}" --log=stdout > /dev/null 2>&1 &
        sleep 2
        
        TUNNEL_JSON=$(curl -s http://127.0.0 || true)
        if [ -n "$TUNNEL_JSON" ] && command -v python3 >/dev/null 2>&1; then
            NGROK_URL=$(python3 -c "import sys, json; data=json.load(sys.stdin); t=data.get('tunnels', []); print(t[0].get('public_url')) if t else print('')" <<< "$TUNNEL_JSON")
            if [ -n "$NGROK_URL" ]; then
                echo "🎯 Public Gateway Live Address: $NGROK_URL"
            fi
        fi
    fi
fi

echo "✅ All servers successfully initialized and running in the background!"
