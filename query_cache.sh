#!/bin/bash
# BizStack Perks App — SQLite Payload Log Extractor

DB_PATH="/Users/shaunoleary/bizstack_perks_app/telegram_cache.db"

echo "=== 🔒 BizStack Perks App — Active Telegram DB Cache Records ==="
if [ -f "$DB_PATH" ]; then
    sqlite3 "$DB_PATH" "SELECT id, timestamp, tenant_id, vertical_tag, payload_text FROM telegram_payload_cache ORDER BY id DESC LIMIT 10;" -header -column
else
    echo "⚠️  Database cache file not found. Ensure bot.py has been executed to populate data."
fi
