import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), "bizstack.db")

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financing_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                annual_revenue REAL NOT NULL,
                credit_score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                card_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS premium_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                charge_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

@app.route('/api/v1/financing/apply', methods=['POST'])
def process_loan_lead():
    lead_data = request.json or {}
    required = ['business_name', 'annual_revenue', 'credit_score']
    if not all(field in lead_data for field in required):
        return jsonify({"status": "error", "message": "Missing underwriting details"}), 400
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO financing_leads (business_name, annual_revenue, credit_score)
                VALUES (?, ?, ?)
            ''', (lead_data['business_name'], lead_data['annual_revenue'], lead_data['credit_score']))
            conn.commit()
        return jsonify({"status": "success", "message": "Lead securely saved to BizStack Database."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/v1/cards/click', methods=['POST'])
def track_card_click():
    click_data = request.json or {}
    user_id = click_data.get('user_id', 'UNKNOWN')
    card_name = click_data.get('card_name', 'PREMIUM_CARD')
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO card_clicks (user_id, card_name) VALUES (?, ?)
            ''', (user_id, card_name))
            conn.commit()
        return jsonify({"status": "success", "message": f"Click metric logged for {card_name}."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/v1/orders/log', methods=['POST'])
def log_premium_order():
    order_data = request.json or {}
    required = ['user_id', 'charge_id', 'amount', 'currency']
    if not all(field in order_data for field in required):
        return jsonify({"status": "error", "message": "Missing payment details"}), 400
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO premium_orders (user_id, charge_id, amount, currency)
                VALUES (?, ?, ?, ?)
            ''', (order_data['user_id'], order_data['charge_id'], order_data['amount'], order_data['currency']))
            conn.commit()
        return jsonify({"status": "success", "message": "Monetization payment logged."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "engine": "BizStack Perks Platform"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
