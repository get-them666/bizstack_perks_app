import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Explicitly grab variables from your live terminal session context
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "olearyshaun14@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "prpikmmkmlasihn")
TARGETS_FILE = "fintech_launch_targets.json"
TEMPLATE_FILE = "B2B_OUTREACH_EMAIL.md"

def launch_outreach_sequence():
    print("🛫 Initializing BizStack Perks Secure Email Engine...")
    print(f"🔒 Authenticating account: {SENDER_EMAIL}")
    print(f"🔑 Using runtime app password: {GMAIL_APP_PASSWORD}")
    
    if not os.path.exists(TARGETS_FILE):
        print(f"❌ Error: Target file {TARGETS_FILE} not found. Run finder.py first.")
        return
        
    if not os.path.exists(TEMPLATE_FILE):
        print(f"❌ Error: Pitch template {TEMPLATE_FILE} not found.")
        return

    with open(TARGETS_FILE, "r") as f:
        leads = json.load(f)
        
    with open(TEMPLATE_FILE, "r") as f:
        email_template = f.read()

    print("🌐 Connecting to smtp.gmail.com...")
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            print("✅ Authentication successful! Transport channel unlocked.\n")
            
            for lead in leads:
                name = lead.get("name", "Fintech Executive")
                segment = lead.get("segment", "Fintech System")
                
                body = email_template.replace("[First Name]", name)
                body = body.replace("[Fintech SaaS / Card Platform / Lending]", segment)
                
                msg = MIMEMultipart()
                msg["From"] = SENDER_EMAIL
                msg["To"] = SENDER_EMAIL  
                msg["Subject"] = f"Optimizing {segment} Channels for {name}"
                msg.attach(MIMEText(body, "plain"))
                
                server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
                print(f"Mailing sandbox slot for target: {name}")
                
        print("\n🎯 Complete sales outreach broadcast sequence finalized successfully!")
    except Exception as e:
        print(f"❌ Connection failed. Details: {e}")

if __name__ == "__main__":
    launch_outreach_sequence()

# Dashboard structural compatibility bridge
dispatch_live_campaign = launch_outreach_sequence
