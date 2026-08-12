#!/bin/bash
# BizStack Perks App — One-Click Automated Cloud Deployment

LOCAL_DIST="/Users/shaunoleary/bizstack_perks_app"
DOMAIN="bizstack-perks-hub.surge.sh"

echo "🚀 Compiling latest application framework layers..."
python3 "$LOCAL_DIST/daily_reporter.py"

echo "📦 Shipping updated static frontends straight to the web gateway..."
if command -v surge &> /dev/null; then
    # Executes the deployment native engine
    surge "$LOCAL_DIST" --domain "$DOMAIN"
else
    echo "⚠️  Surge CLI tool dependency not detected locally."
    echo "To activate live global tracking sync, run: npm install -g surge"
fi
