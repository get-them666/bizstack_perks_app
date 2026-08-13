# Cloudflared integration added to up.sh
# Usage: set CF_TUNNEL_NAME and CF_INGRESS_HOST env vars if you created a Cloudflare Tunnel

if command -v cloudflared >/dev/null 2>&1 && [ -n "${CF_TUNNEL_NAME:-}" ]; then
  echo "🌐 Starting cloudflared tunnel for ${CF_TUNNEL_NAME}..."
  # Run tunnel in background (assumes credentials are provisioned via 'cloudflared tunnel create' and 'cloudflared tunnel route dns')
  nohup cloudflared tunnel run "${CF_TUNNEL_NAME}" > "$REPO_ROOT/cloudflared.log" 2>&1 &
  CLOUDFLARED_PID=$!
  sleep 1.5
  if [ -n "${CF_INGRESS_HOST:-}" ]; then
    echo "🎯 Cloudflare Tunnel public hostname: https://${CF_INGRESS_HOST}"
  else
    echo "⚠️  cloudflared started but CF_INGRESS_HOST not set. Set CF_INGRESS_HOST to your routed DNS name (e.g. api.example.com)."
  fi
else
  # fall back to existing ngrok behavior
  if command -v ngrok >/dev/null 2>&1; then
    if [ -n "${NGROK_AUTHTOKEN:-}" ]; then
      echo "🌐 Starting ngrok for FastAPI (port ${FASTAPI_PORT})"
      nohup ngrok http ${FASTAPI_PORT} --log=stdout > /dev/null 2>&1 &
      sleep 1.5
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
fi
