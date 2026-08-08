import sqlite3
import os

DB_FILE = "bizstack.db"

# Historical production records retrieved from your backup logs
leads_data = [
    (1, "BizStack Final Test LLC", 500000.0, 740, "2026-08-02 21:31:26")
]

clicks_data = [
    (1, "8844949255", "AMEX_GOLD", "2026-08-05 16:32:44")
]

def restore_database():
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found. Run your app.py first to initialize tables.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Injecting historical underwriting leads
        print("📥 Restoring financing leads...")
        cursor.executemany('''
            INSERT OR REPLACE INTO financing_leads (id, business_name, annual_revenue, credit_score, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', leads_data)
        
        # Injecting historical affiliate link trackings
        print("📥 Restoring card click tracking loops...")
        cursor.executemany('''
            INSERT OR REPLACE INTO card_clicks (id, user_id, card_name, timestamp)
            VALUES (?, ?, ?, ?)
        ''', clicks_data)
        
        conn.commit()
        print("✅ Success! Historical records successfully re-injected into bizstack.db.")
        
    except sqlite3.Error as e:
        print(f"❌ Database error encountered: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    restore_database()
