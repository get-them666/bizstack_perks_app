if command -v python3 >/dev/null 2>&1; then
    echo "🔎 Attempting to fetch ngrok public URL from ${NGROK_API_LOCAL}/api/tunnels"
    TUNNEL_JSON=$(curl -s ${NGROK_API_LOCAL}/api/tunnels || true)
    
    if [ -n "$TUNNEL_JSON" ]; then
        # 🟢 FIX: Pass the raw JSON string safely into Python as an executable string argument
        NGROK_URL=$(python3 -c "import sys, json; data=json.loads(sys.argv[1]); tunnels=data.get('tunnels', []); print(tunnels[0].get('public_url', '')) if tunnels else print('')" "$TUNNEL_JSON")
        
        if [ -n "$NGROK_URL" ]; then
            echo "🎯 Ngrok public URL: $NGROK_URL"
        else
            echo "⚠️ Ngrok running but couldn't determine public URL from API"
        fi
    else
        echo "⚠️ Ngrok API returned no data. Is ngrok running and authenticated?"
    fi
else
    echo "⚠️ python3 not available to parse ngrok API response"
fi
