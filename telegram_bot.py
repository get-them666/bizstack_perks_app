import os
import json
from datetime import datetime
from compliance import FintechComplianceVault

class BizStackTelegramAgent:
    def __init__(self):
        self.log_dest = "/Users/shaunoleary/bizstack_perks_app/live_traffic_stream.json"
        print("🤖 BizStack Perks Telegram Bot Initialized...")

    def handle_incoming_eligibility_check(self, customer_email: str, requested_amount: float, business_type: str):
        """Processes inbound customer interactions from the landing page link"""
        raw_payload = {
            "customer_email": customer_email,
            "requested_loan": requested_amount,
            "business_type": business_type
        }
        
        # Enforce financial data isolation boundaries via compliance engine
        sanitized_data = FintechComplianceVault.isolate_and_hash_pii(raw_payload, "SaaS_Fintech_A")
        
        # Format the event for your Streamlit analytics chart pipeline
        traffic_event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vertical": "Loans_SaaS",
            "action": f"Telegram Check: {business_type} (${requested_amount:,})",
            "estimated_value": requested_amount * 0.03, # 3% baseline origination estimation
            "clicks_added": 0,
            "leads_added": 1
        }
        
        # Append directly to your live data file system
        try:
            with open(self.log_dest, "r") as f: data = json.load(f)
        except Exception: data = []
        data.append(traffic_event)
        with open(self.log_dest, "w") as f: json.dump(data, f, indent=4)
        
        print(f"[TELEGRAM BOT SUCCESFUL] Ingested user lead data safely for validation.")
        return f"Pre-qualification logged. Reference Token: {sanitized_data['customer_email']}"

if __name__ == "__main__":
    agent = BizStackTelegramAgent()
    # Execute a mock user test interaction
    status = agent.handle_incoming_eligibility_check("owner@chesapeakebiz.com", 75000, "LLC")
    print(f"Bot Output Response: {status}")
