#!/usr/bin/env bash
set -euo pipefail

# up.sh - Unified launcher for BizStack Perks (FastAPI + Streamlit + optional Flask + ngrok)
# Usage: ./up.sh
# This script mirrors the previous workflow but updated for the consolidated FastAPI backend
# and Streamlit dashboard. It starts services in the background and prints log tails.

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$REPO_ROOT"

echo "⚡ BizStack Perks - UP script starting..."

# Default ports used by the app
FASTAPI_PORT=${FASTAPI_PORT:-8080}
STREAMLIT_PORT=${STREAMLIT_PORT:-8501}
FLASK_PORT=${FLASK_PORT:-5000}
NGROK_API_LOCAL=${NGROK_API_LOCAL:-http://127.0.0.1:4040}

# Helper: kill process listening on a port (ignore errors)
kill_port() {
  local port=$1
  if command -v lsof >/dev/null 2>&1; then
    PIDS=$(lsof -t -i:${port} || true)
    if [ -n "$PIDS" ]; then
      echo "🧹 Killing processes on port ${port}: $PIDS"
      kill -9 $PIDS || true
    fi
  else
    echo "⚠️  lsof not installed; skipping kill for port ${port}" 
  fi
}

# 1) Update repository (if running inside a git clone)
if [ -d .git ]; then
  echo "📦 Pulling latest from remote (if available)..."
  git pull origin main || true
fi

# 2) Kill lingering processes
kill_port ${FASTAPI_PORT}
kill_port ${STREAMLIT_PORT}
kill_port ${FLASK_PORT}
kill_port 4040  # ngrok local API

# 3) Start FastAPI (api.main:app)
API_LOG="$REPO_ROOT/api.log"
echo "🚀 Starting FastAPI (uvicorn) on port ${FASTAPI_PORT} -> ${API_LOG}"
# Use python -m uvicorn to ensure module resolution
nohup python -m uvicorn api.main:app --host 0.0.0.0 --port ${FASTAPI_PORT} > "$API_LOG" 2>&1 &
API_PID=$!
sleep 0.6
echo "   FastAPI PID: ${API_PID}"

# 4) Start Flask app (legacy) if present
if [ -f "$REPO_ROOT/app.py" ]; then
  FLASK_LOG="$REPO_ROOT/flask.log"
  echo "🧪 Starting Flask app on port ${FLASK_PORT} -> ${FLASK_LOG}"
  nohup python app.py > "$FLASK_LOG" 2>&1 &
  FLASK_PID=$!
  echo "   Flask PID: ${FLASK_PID}"
else
  echo "ℹ️  app.py not found - skipping Flask startup"
fi

# 5) Start Streamlit dashboard
if [ -f "$REPO_ROOT/dashboard.py" ]; then
  STREAM_LOG="$REPO_ROOT/streamlit.log"
  echo "📊 Starting Streamlit on port ${STREAMLIT_PORT} -> ${STREAM_LOG}"
  nohup streamlit run dashboard.py --server.port ${STREAMLIT_PORT} --server.headless true > "$STREAM_LOG" 2>&1 &
  STREAM_PID=$!
  echo "   Streamlit PID: ${STREAM_PID}"
else
  echo "ℹ️  dashboard.py not found - skipping Streamlit startup"
fi

# 6) Start ngrok tunnel if binary exists and user wants it
if command -v ngrok >/dev/null 2>&1; then
  if [ -n "${NGROK_AUTHTOKEN:-}" ]; then
    # If user provided NGROK_AUTHTOKEN env var we assume they want ngrok; otherwise still start but without auth
    echo "🌐 Starting ngrok for FastAPI (port ${FASTAPI_PORT})"
    nohup ngrok http ${FASTAPI_PORT} --log=stdout > /dev/null 2>&1 &
    sleep 1.5
    # Try to fetch public URL from ngrok API
    if command -v python3 >/dev/null 2>&1; then
      echo "🔎 Attempting to fetch ngrok public URL from ${NGROK_API_LOCAL}/api/tunnels"
      TUNNEL_JSON=$(curl -s ${NGROK_API_LOCAL}/api/tunnels || true)
      if [ -n "$TUNNEL_JSON" ]; then
        NGROK_URL=$(python3 - <<PY
import sys, json
try:
  data = json.load(sys.stdin)
  tunnels = data.get('tunnels') or []
  if tunnels:
    print(tunnels[0].get('public_url'))
except Exception:
  pass
PY
<<< "$TUNNEL_JSON")
        if [ -n "$NGROK_URL" ]; then
          echo "🎯 Ngrok public URL: $NGROK_URL"
        else
          echo "⚠️  Ngrok running but couldn't determine public URL from API"
        fi
      else
        echo "⚠️  Ngrok API returned no data. Is ngrok running and authenticated?"
      fi
    else
      echo "⚠️  python3 not available to parse ngrok API response"
    fi
  else
    echo "⚠️  ngrok installed but NGROK_AUTHTOKEN not provided; you can still start ngrok manually."
  fi
else
  echo "ℹ️  ngrok not found on PATH - skipping ngrok startup (install ngrok if you need a public tunnel)"
fi

sleep 1

# 7) Quick health checks
echo "
🔬 Health checks (basic):"
if curl -sS "http://127.0.0.1:${FASTAPI_PORT}/health" >/dev/null 2>&1; then
  echo "   ✅ FastAPI /health OK"
else
  echo "   ❌ FastAPI /health did not respond. Check $API_LOG"
fi

if [ -f "$REPO_ROOT/dashboard.py" ]; then
  if curl -sS "http://127.0.0.1:${STREAMLIT_PORT}" >/dev/null 2>&1; then
    echo "   ✅ Streamlit interface available on port ${STREAMLIT_PORT}"
  else
    echo "   ❌ Streamlit not responding on port ${STREAMLIT_PORT}. Check $STREAM_LOG"
  fi
fi

# 8) Tail logs (press CTRL+C to detach - processes keep running)
echo -e "\n🟢 ALL SYSTEMS STARTED. Tailing logs (api.log then streamlit.log) - press CTRL+C to stop tailing but leave processes running.\n"

# Tail logs if they exist
if [ -f "$API_LOG" ]; then
  tail -n +1 -f "$API_LOG" &
  TAIL_PID1=$!
fi
if [ -f "$STREAM_LOG" ]; then
  tail -n +1 -f "$STREAM_LOG" &
  TAIL_PID2=$!
fi

wait
