import urllib.request
import json

try:
    # Query your local Ngrok background routing agent
    req = urllib.request.Request("http://127.0.0")
    response = json.loads(urllib.request.urlopen(req).read().decode())
    
    # Locate the active secure HTTPS tunnel endpoint
    tunnel = next(t["public_url"] for t in response["tunnels"] if t["public_url"].startswith("https"))
    print(f"🎯 Linked Tunnel: {tunnel}")
    
    # Download the matrix interface template layout
    gist_url = "https://githubusercontent.com"
    html_content = urllib.request.urlopen(gist_url).read().decode()
    
    # Inject your live secure tunnel parameters
    patched_html = html_content.replace("TARGET_TUNNEL_ENDPOINT", tunnel)
    
    with open("consult.html", "w") as f:
        f.write(patched_html)
    print("✅ Successfully patched consult.html with your active secure tunnel.")

except Exception as e:
    print(f"❌ Automation failed: {e}")
    print("👉 Verify your launcher.sh or ngrok process is running in the background!")
