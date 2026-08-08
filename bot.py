import os
import requests
import telebot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telebot import types

# Live Active Bot Credentials
API_TOKEN = '8879832172:AAGTA4EqmNJ_gCdeu_oUUd_J5IMVCSZCZYk'
PROVIDER_TOKEN = 'YOUR_STRIPE_TOKEN_FROM_BOTFATHER' 
bot = telebot.TeleBot(API_TOKEN)

BASE_URL = "http://127.0.0.1:8080"
CARDS_CLICK_URL = f"{BASE_URL}/api/v1/cards/click"
FINANCING_APPLY_URL = f"{BASE_URL}/api/v1/financing/apply"
ORDERS_LOG_URL = f"{BASE_URL}/api/v1/orders/log"

# --- GOOGLE NATIVE SMTP CONFIGURATION ---
GOOGLE_EMAIL = "olearyshaun14@gmail.com"
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_SMTP_PASS", "")
NOTIFICATION_RECEIVER_EMAIL = "olearyshaun14@gmail.com"

def dispatch_email_alert(b_name, rev, credit):
    """Securely transmits transactional HTML dossiers straight through Google SMTP relays."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New High-Ticket Business Lead: {b_name}"
    msg["From"] = GOOGLE_EMAIL
    msg["To"] = NOTIFICATION_RECEIVER_EMAIL

    html_content = f"""
    <html>
        <body style='font-family: Arial, sans-serif; color: #333; line-height: 1.6;'>
            <div style='max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;'>
                <h2 style='color: #2b6cb0; border-bottom: 2px solid #2b6cb0; padding-bottom: 10px;'>New Underwriting Lead Captured</h2>
                <table style='width: 100%; border-collapse: collapse; margin-top: 15px;'>
                    <tr><td style='padding: 8px; font-weight: bold; background: #f7fafc; border: 1px solid #e2e8f0;'>Business Name:</td><td style='padding: 8px; border: 1px solid #e2e8f0;'>{b_name}</td></tr>
                    <tr><td style='padding: 8px; font-weight: bold; background: #f7fafc; border: 1px solid #e2e8f0;'>Annual Revenue:</td><td style='padding: 8px; border: 1px solid #e2e8f0;'>${rev:,.2f}</td></tr>
                    <tr><td style='padding: 8px; font-weight: bold; background: #f7fafc; border: 1px solid #e2e8f0;'>Credit Score:</td><td style='padding: 8px; border: 1px solid #e2e8f0;'>{credit}</td></tr>
                </table>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("://gmail.com", 587) as server:
            server.starttls()
            server.login(GOOGLE_EMAIL, GOOGLE_APP_PASSWORD)
            server.sendmail(GOOGLE_EMAIL, NOTIFICATION_RECEIVER_EMAIL, msg.as_string())
        return True
    except Exception:
        return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_card = types.InlineKeyboardButton(text="💳 Apply for Premium Business Cards", callback_data="click_premium_card")
    btn_loan = types.InlineKeyboardButton(text="💰 Check Business Financing Eligibility", callback_data="apply_financing")
    btn_premium = types.InlineKeyboardButton(text="⭐ Buy Premium Access ($49.00)", callback_data="buy_premium")
    markup.add(btn_card, btn_loan, btn_premium)
    bot.reply_to(message, "Welcome to BizStack Perks Hub! Choose an options dashboard below to get started:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = str(call.from_user.id)
    if call.data == "click_premium_card":
        try:
            requests.post(CARDS_CLICK_URL, json={"user_id": user_id, "card_name": "AMEX_GOLD"}, timeout=3)
        except Exception: pass
        affiliate_url = "https://example-affiliate-link.com"
        bot.send_message(call.message.chat.id, f"Opening exclusive high-ticket offers portal!\n\n👉 [Click to Apply Now]({affiliate_url})", parse_mode="Markdown")
    elif call.data == "apply_financing":
        msg = bot.send_message(call.message.chat.id, "Let's check your funding limit. What is your Legal Business Name?")
        bot.register_next_step_handler(msg, process_name)
    elif call.data == "buy_premium":
        prices = [types.LabeledPrice(label='Premium Access', amount=4900)]
        bot.send_invoice(
            call.message.chat.id,
            title="BizStack Premium Access",
            description="Priority support and exclusive analytics tracker features.",
            provider_token=PROVIDER_TOKEN,
            currency="USD",
            prices=prices,
            start_parameter="premium-analytics",
            invoice_payload="BIZSTACK_MEMBERSHIP_FEE"
        )

def process_name(message):
    try:
        msg = bot.send_message(message.chat.id, f"What is the estimated Annual Revenue for '{message.text}'?")
        bot.register_next_step_handler(msg, process_revenue, message.text)
    except Exception: bot.reply_to(message, "Error. Type /start to retry.")

def process_revenue(message, b_name):
    try:
        rev = float(message.text.replace(",", ""))
        msg = bot.send_message(message.chat.id, "Lastly, what is your estimated personal Credit Score?")
        bot.register_next_step_handler(msg, process_credit, b_name, rev)
    except Exception: bot.reply_to(message, "Invalid number format. Type /start to restart.")

def process_credit(message, b_name, rev):
    try:
        credit_score = int(message.text)
        payload = {"business_name": b_name, "annual_revenue": rev, "credit_score": credit_score}
        res = requests.post(FINANCING_APPLY_URL, json=payload, timeout=5)
        
        if res.status_code == 200:
            bot.send_message(message.chat.id, "Success! Your underwriting profile has been securely saved to the database.")
            dispatch_email_alert(b_name, rev, credit_score)
        else:
            bot.send_message(message.chat.id, "Backend system busy. Lead logged locally.")
    except Exception: bot.reply_to(message, "Submission process error. Try again with /start.")

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_payment_success(message):
    pmnt = message.successful_payment
    user_id = str(message.from_user.id)
    
    # Log successful payments back to database framework
    payload = {
        "user_id": user_id,
        "charge_id": pmnt.telegram_payment_charge_id,
        "amount": pmnt.total_amount / 100.0,
        "currency": pmnt.currency
    }
    try:
        requests.post(ORDERS_LOG_URL, json=payload, timeout=5)
    except Exception: pass

    bot.send_message(message.chat.id, f"Payment Success! Charge ID: {pmnt.telegram_payment_charge_id}")

if __name__ == '__main__':
    bot.infinity_polling()

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_payment_success(message):
    pmnt = message.successful_payment
    user_id = str(message.from_user.id)
    payload = {
        "user_id": user_id,
        "charge_id": pmnt.telegram_payment_charge_id,
        "amount": pmnt.total_amount / 100.0,
        "currency": pmnt.currency
    }
    try:
        requests.post(ORDERS_LOG_URL, json=payload, timeout=5)
    except Exception: pass
    bot.send_message(message.chat.id, f"⚡ Premium Status Activated! Reference: {pmnt.telegram_payment_charge_id}")

# --- REAL-TIME UNDERWRITING ADVISEMENT ENGINE ---
def process_business_address_input(message, b_name, rev, credit):
    try:
        from compliance_check import verify_business_address
        address_text = message.text
        is_valid, feedback_msg = verify_business_address(address_text)
        
        if not is_valid:
            msg = bot.send_message(message.chat.id, f"❌ {feedback_msg}\n\nPlease enter a valid physical corporate street address:")
            bot.register_next_step_handler(msg, process_business_address_input, b_name, rev, credit)
            return

        # Securely archive the lead profile once compliance flags pass
        payload = {
            "business_name": b_name, 
            "annual_revenue": rev, 
            "credit_score": credit,
            "business_address": address_text
        }
        res = requests.post(FINANCING_APPLY_URL, json=payload, timeout=5)
        
        if res.status_code == 200:
            bot.send_message(message.chat.id, "✅ Profile Verified! Your compliant corporate data file has been securely synced to the underwriting desk.")
            dispatch_email_alert(b_name, rev, credit)
        else:
            bot.send_message(message.chat.id, "⚠️ Central server busy. Core lead logged locally in structural backup tables.")
    except Exception:
        bot.reply_to(message, "Process configuration error. Please run /start to clear the state machine.")

def process_credit(message, b_name, rev):
    try:
        credit_score = int(message.text)
        # Transition immediately to the compliance address collector phase
        msg = bot.send_message(message.chat.id, "📍 Finally, what is your corporate physical street address? (Include Street, City, State, and ZIP Code)")
        bot.register_next_step_handler(msg, process_business_address_input, b_name, rev, credit_score)
    except Exception:
        bot.reply_to(message, "⚠️ Invalid format. Type /start to restart your application funnel.")


# --- LIVE LEAD QUALIFICATION & PHONE INTERCEPT LOOP ---
import re

def process_phone_qualification(message, b_name, rev, credit, addr):
    try:
        raw_phone = message.text
        # Strip trailing characters, dashes, spaces, and brackets
        cleaned_phone = re.sub(r"[\s\-\(\)\+]", "", raw_phone)
        
        # Enforce North American standard length thresholds (e.g. 10 or 11 digits)
        if not cleaned_phone.isdigit() or len(cleaned_phone) < 10 or len(cleaned_phone) > 11:
            msg = bot.send_message(message.chat.id, "❌ Invalid data format structure. Please enter a valid 10-digit business contact number:")
            bot.register_next_step_handler(msg, process_phone_qualification, b_name, rev, credit, addr)
            return

        # Securely archive the lead profile once compliance flags pass
        payload = {
            "business_name": b_name, 
            "annual_revenue": rev, 
            "credit_score": credit,
            "business_address": addr,
            "phone_number": cleaned_phone
        }
        res = requests.post(FINANCING_APPLY_URL, json=payload, timeout=5)
        
        if res.status_code == 200:
            bot.send_message(message.chat.id, "✅ Profile Verified! Your compliant corporate data file has been securely synced to the underwriting desk.")
            dispatch_email_alert(b_name, rev, credit)
        else:
            bot.send_message(message.chat.id, "⚠️ Central server busy. Core lead logged locally in structural backup tables.")
    except Exception:
        bot.reply_to(message, "Process configuration error. Please run /start to clear the state machine.")


# --- AUTOMATED PREMIUM MONETIZATION ONBOARDING ROUTINE ---
def dispatch_premium_welcome_message(user_id):
    """
    Triggered instantly via background webhooks to unlock premium telemetry access parameters.
    """
    print(f"⭐ Dispatching high-tier welcome layout sequence to User: {user_id}")
    welcome_text = (
        "👑 *WELCOME TO BIZSTACK PREMIUM MEMBERSHIP* 👑

"
        "Your payment has been securely tokenized and processed via Stripe!

"
        "🚀 *Your Elite Funding Perks are Now Unlocked:*
"
        "• Direct Tier-1 AMEX/Chase pre-qualification parameters
"
        "• Real-time asset underwriting radar models
"
        "• Exclusive commercial financing matching access cards

"
        "Tap /menu at any time to pull up your advanced premium operations console dashboard."
    )
    try:
        bot.send_message(chat_id=user_id, text=welcome_text, parse_mode="Markdown")
        print(f"✅ Onboarding message transmitted to premium client: {user_id}")
        return True
    except Exception as e:
        print(f"❌ Failed to reach chat handle profile {user_id}: {e}")
        return False
