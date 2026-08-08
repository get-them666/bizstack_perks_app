#!/usr/bin/env bash

echo "=================================================="
echo "🔍 BIZSTACK WORKSPACE DIAGNOSTIC SYSTEM HEALTH"
echo "=================================================="

check_process() {
    local name=$1
    local search_pattern=$2
    if pgrep -f "$search_pattern" > /dev/null; then
        echo -e "  $name ➔ \033[0;32mONLINE\033[0;37m"
    else
        echo -e "  $name ➔ \033[0;31mOFFLINE\033[0;37m"
    fi
}

check_port() {
    local name=$1
    local port=$2
    if lsof -i :$port > /dev/null; then
        echo -e "  Port Check ($name on :$port) ➔ \033[0;32mACTIVE\033[0;37m"
    else
        echo -e "  Port Check ($name on :$port) ➔ \033[0;31mDISCONNECTED\033[0;37m"
    fi
}

check_process "Flask Engine CORE API" "app.py"
check_process "Telegram Automation Loop" "bot.py"
check_process "Checkout Recovery Daemon" "recovery_loop.py"
check_process "Streamlit Commercial UI" "streamlit run dashboard.py"

echo "--------------------------------------------------"
check_port "Flask Core" 8080
check_port "Streamlit Dashboard" 8501
echo "=================================================="
