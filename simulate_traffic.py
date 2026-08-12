import json
import time
import random
from datetime import datetime

LOG_FILE = "/Users/shaunoleary/bizstack_perks_app/live_traffic_stream.json"

verticals = ["Fintech_SaaS", "Credit_Card", "Loans_SaaS"]
actions = {
    "Fintech_SaaS": ["API Docs Abandonment Salvaged", "Pricing Page Exit Intercepted"],
    "Credit_Card": ["Premium Card Ad Click Tracked", "Application Form Re-engagement"],
    "Loans_SaaS": ["Pre-Screening Data Ingested", "Underwriting Pipeline Push"]
}

print("🚀 Starting Live Fintech Traffic Simulator... Press Ctrl+C to stop.")

# Initialize the file with empty array if it doesn't exist
with open(LOG_FILE, "w") as f:
    json.dump([], f)

while True:
    try:
        # Load existing data
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
        
        # Keep only the last 50 entries to keep it fast
        if len(data) > 50:
            data = data[-50:]
            
        # Generate new random traffic event
        vert = random.choice(verticals)
        act = random.choice(actions[vert])
        rev = round(random.uniform(500, 2500), 2) if vert == "Fintech_SaaS" else 0
        clicks = random.randint(10, 50) if vert == "Credit_Card" else 0
        leads = 1 if vert == "Loans_SaaS" else 0
        
        new_event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vertical": vert,
            "action": act,
            "estimated_value": rev,
            "clicks_added": clicks,
            "leads_added": leads
        }
        
        data.append(new_event)
        
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=4)
            
        print(f"[SIMULATOR] Dispatched event for {vert}: {act}")
        time.sleep(random.uniform(1.5, 3.5)) # Send a new signal every couple of seconds
        
    except KeyboardInterrupt:
        print("\nSimulator stopped.")
        break
