#!/usr/bin/env bash
source venv/bin/activate

# Secure Credential Layers
export TELEGRAM_API_TOKEN="8879832172:AAGTA4EqmNJ_gCdeu_oUUd_J5IMVCSZCZYk"
export STRIPE_PROVIDER_TOKEN="YOUR_STRIPE_TOKEN_FROM_BOTFATHER"
export GOOGLE_SMTP_PASS="ykrgfzvzvcyhdtea"

# Analytical Networking Targets
export PORT=8080
export HOST="0.0.0.0"

echo "=================================================="
echo "🚀 BizStack Perks Architecture Stack Going Online"
echo "=================================================="
python3 app.py &
python3 bot.py &
wait
