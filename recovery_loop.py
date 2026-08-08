import sqlite3
import time
import requests

DB_FILE = "bizstack.db"
TELEGRAM_API_URL = "https://telegram.org"

def process_abandoned_funnels():
    print("🔍 Auditing acquisition pipeline for incomplete checkout states...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Find leads that exist in clicks or forms but haven't converted in premium_orders
        cursor.execute('''
            SELECT DISTINCT user_id FROM card_clicks 
            WHERE user_id NOT IN (SELECT DISTINCT user_id FROM premium_orders)
        ''')
        abandoned_users = cursor.fetchall()
        
        for user in abandoned_users:
            uid = user[0]
            print(f"⚠️ Recovering user session: {uid}")
            
            message_text = (
                "⚡ *Complete Your BizStack Premium Setup*\n\n"
                "We noticed you didn't finish activating your premium analytics account. "
                "Unlock high-ticket underwriting parameters and direct AMEX pre-qualification routing matrices now!\n\n"
                "Return to your bot menu and tap *Buy Premium Access ($49.00)* to go live instantly."
            )
            
            payload = {"chat_id": uid, "text": message_text, "parse_mode": "Markdown"}
            try:
                res = requests.post(TELEGRAM_API_URL, json=payload, timeout=5)
                print(f"Recovery status for {uid}: {res.status_code}")
            except Exception as e:
                print(f"Failed to dispatch recovery text: {e}")
                
    except sqlite3.Error as e:
        print(f"Database error during recovery processing: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Standard continuous loop configuration
    while True:
        process_abandoned_funnels()
        print("💤 Recovery scan completed. Sleeping for 1 hour...")
        time.sleep(3600)  # Scan hourly
