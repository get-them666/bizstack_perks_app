import os
import shutil
import sqlite3
from datetime import datetime

DB_FILE = "bizstack.db"
BACKUP_DIR = os.path.expanduser("~/Desktop/BizStack_Database_Backups")

def run_database_backup():
    print(f"⏳ [{datetime.now()}] Initializing automated backup routine...")
    
    # Ensure backup folder exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"📁 Created backup repository directory: {BACKUP_DIR}")
        
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: Source database {DB_FILE} not found.")
        return

    # Verify database integrity before backing up
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        status = cursor.fetchone()[0]
        conn.close()
        
        if status != "ok":
            print(f"⚠️ Integrity check failed ({status}). Aborting snapshot.")
            return
    except Exception as e:
        print(f"❌ Database access check crash: {e}")
        return

    # Generate a unique timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"bizstack_backup_{timestamp}.db"
    dest_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copy2(DB_FILE, dest_path)
        print(f"💾 Snapshot successfully archived to: {dest_path}")
        
        # Enforce rolling retention: Delete files older than 7 days
        all_backups = sorted(
            [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.startswith("bizstack_backup_")]
        )
        if len(all_backups) > 7:
            for old_backup in all_backups[:-7]:
                os.remove(old_backup)
                print(f"🗑️ Cleaned up expired historical archive layer: {os.path.basename(old_backup)}")
                
    except IOError as e:
        print(f"❌ Backup failed due to system write exception: {e}")

if __name__ == "__main__":
    run_database_backup()
