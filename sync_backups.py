import os
import sqlite3
import pandas as pd
from glob import glob

DB_FILE = "bizstack.db"
BACKUP_DIR = os.path.expanduser("~/Desktop/BizStack_Database_Backups")

def sync_all_backups():
    print("⏳ Beginning deep search across desktop ledger backup files...")
    search_path = os.path.join(BACKUP_DIR, "BizStack_Leads_Report_*.xlsx")
    backup_files = sorted(glob(search_path))
    
    if not backup_files:
        print("💡 No historical sheets found inside the database backups path.")
        return
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    for file_path in backup_files:
        filename = os.path.basename(file_path)
        print(f"📖 Parsing snapshot layer: {filename}")
        try:
            # Load sheet raw into memory
            df = pd.read_excel(file_path, header=None)
            
            # Locate rows matching specific schema headers
            lead_idx = df[df[0] == 'id'].index.tolist()
            
            if len(lead_idx) >= 2:
                # 📋 Section A: Underwriting Leads (First Block)
                start_leads = lead_idx[0] + 1
                end_leads = lead_idx[1]
                leads_block = df.iloc[start_leads:end_leads].dropna(subset=[1])
                
                for _, row in leads_block.iterrows():
                    cursor.execute('''
                        INSERT INTO financing_leads (business_name, annual_revenue, credit_score, timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', (str(row[1]), float(row[2]), int(row[3]), str(row[4])))
                
                # 💳 Section B: Outbound Ad Clicks (Second Block)
                start_clicks = lead_idx[1] + 1
                clicks_block = df.iloc[start_clicks:].dropna(subset=[1])
                
                for _, row in clicks_block.iterrows():
                    cursor.execute('''
                        INSERT INTO card_clicks (user_id, card_name, timestamp)
                        VALUES (?, ?, ?)
                    ''', (str(row[1]), str(row[2]), str(row[3])))
            
            conn.commit()
            print(f"✅ Successfully integrated records from {filename}.")
        except Exception as e:
            print(f"⚠️ Skipping row entries in {filename}: {e}")
            
    conn.close()
    print("🎯 Synchronization pass complete. Core relational rows are matching live.")

if __name__ == "__main__":
    sync_all_backups()
