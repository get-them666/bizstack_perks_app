import sqlite3
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DB_FILE = "bizstack.db"
GOOGLE_EMAIL = "olearyshaun14@gmail.com"
GOOGLE_APP_PASSWORD = "ykrgfzvzvcyhdtea"

def send_daily_report():
    print("📊 Compiling daily financial performance report...")
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM premium_orders WHERE timestamp >= datetime('now', '-1 day')")
        daily_rev = cursor.fetchone()[0] or 0.0
        cursor.execute("SELECT COUNT(id) FROM financing_leads WHERE timestamp >= datetime('now', '-1 day')")
        daily_leads = cursor.fetchone()[0] or 0
        conn.close()
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📈 BizStack Daily Performance Summary: ${daily_rev:,.2f}"
        msg["From"] = GOOGLE_EMAIL
        msg["To"] = GOOGLE_EMAIL
        
        html = f"<html><body><h2>BizStack Daily Report</h2><hr/><p><strong>Revenue (24h):</strong> ${daily_rev:,.2f}</p><p><strong>New Leads:</strong> {daily_leads}</p></body></html>"
        msg.attach(MIMEText(html, "html"))
        
        try:
            with smtplib.SMTP("://gmail.com", 587, timeout=5) as server:
                server.starttls()
                server.login(GOOGLE_EMAIL, GOOGLE_APP_PASSWORD)
                server.sendmail(GOOGLE_EMAIL, GOOGLE_EMAIL, msg.as_string())
            print("✅ Daily performance metrics emailed successfully via Google Remote Server.")
        except Exception:
            print("⚠️ Remote Google login locked. Falling back to clean local file log...")
            with open("daily_email_output_preview.html", "w") as out_f:
                out_f.write(html)
            print("💾 Saved live HTML compilation layout directly to: daily_email_output_preview.html")
            
    except Exception as e:
        print(f"❌ Failed to compile metric layers: {e}")

if __name__ == "__main__":
    send_daily_report()
