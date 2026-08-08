import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="BizStack Commercial Analytics Hub",
    page_icon="🚀",
    layout="wide"
)

DB_FILE = "bizstack.db"

def fetch_analytics_data():
    conn = sqlite3.connect(DB_FILE)
    try:
        leads_df = pd.read_sql_query("SELECT * FROM financing_leads ORDER BY timestamp DESC", conn)
    except Exception: leads_df = pd.DataFrame()
        
    try:
        clicks_df = pd.read_sql_query("SELECT * FROM card_clicks ORDER BY timestamp DESC", conn)
    except Exception: clicks_df = pd.DataFrame()

    try:
        orders_df = pd.read_sql_query("SELECT * FROM premium_orders ORDER BY timestamp DESC", conn)
    except Exception: orders_df = pd.DataFrame()
    
    conn.close()
    return leads_df, clicks_df, orders_df

st.title("🚀 BizStack Perks Commercial Analytics Hub")
st.markdown("Monitor real-time incoming traffic loops, card affiliate conversions, and underwriting data structures below.")

if st.button("🔄 Sync Database Metric Data Rows"):
    st.rerun()

leads, clicks, orders = fetch_analytics_data()

# --- TOP LINE METRIC CARD LAYOUT ROWS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_leads = len(leads) if not leads.empty else 0
    st.metric(label="💰 Total Financing Requests", value=total_leads)

with col2:
    total_clicks = len(clicks) if not clicks.empty else 0
    st.metric(label="💳 Premium Card Ad Clicks", value=total_clicks)

with col3:
    total_revenue = orders['amount'].sum() if not orders.empty else 0.0
    st.metric(label="💵 Total Membership Revenue", value=f"${total_revenue:,.2f}")

with col4:
    if not leads.empty and 'annual_revenue' in leads.columns:
        avg_revenue = leads['annual_revenue'].mean()
        st.metric(label="📈 Avg Underwriting Revenue", value=f"${avg_revenue:,.2f}")
    else:
        st.metric(label="📈 Avg Underwriting Revenue", value="$0.00")

st.markdown("---")

# --- DATA MATRIX CONTAINER TABS ---
tab1, tab2, tab3 = st.tabs(["📋 Underwriting Leads Table", "🔗 Link Tracking Activity", "⭐ Paid Premium Orders"])

with tab1:
    st.subheader("High-Ticket Business Financing Submissions")
    if not leads.empty:
        st.dataframe(leads, use_container_width=True, hide_index=True)
    else:
        st.info("Waiting for users to fill out the eligibility form in @BizStackPerksBot...")

with tab2:
    st.subheader("Affiliate Card Tracking Metrics Log")
    if not clicks.empty:
        st.dataframe(clicks, use_container_width=True, hide_index=True)
    else:
        st.info("No outbound card link interactions recorded yet.")

with tab3:
    st.subheader("Stripe Monetization Conversion Audit")
    if not orders.empty:
        st.dataframe(orders, use_container_width=True, hide_index=True)
    else:
        st.info("No premium conversions recorded on account gateway yet.")


# --- CREDIT SCORE VS AD CLICK METRIC CORRELATIONS ---
st.markdown("---")
st.subheader("📊 Lead Credit Quality vs Premium Card Ad Clicks")
if not leads.empty and not clicks.empty:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("**Credit Distribution of Incoming Funding Leads**")
        st.bar_chart(leads["credit_score"].value_counts())
    with col_chart2:
        st.markdown("**Outbound Conversion Counts by Card Type**")
        st.bar_chart(clicks["card_name"].value_counts())
else:
    st.info("Awaiting structural credit metrics and click loops to render correlation data models.")


# --- CREDIT SCORE VS AD CLICK METRIC CORRELATIONS ---
st.markdown("---")
st.subheader("📊 Lead Credit Quality vs Premium Card Ad Clicks")
if not leads.empty and not clicks.empty:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("**Credit Distribution of Incoming Funding Leads**")
        st.bar_chart(leads["credit_score"].value_counts())
    with col_chart2:
        st.markdown("**Outbound Conversion Counts by Card Type**")
        st.bar_chart(clicks["card_name"].value_counts())
else:
    st.info("Awaiting structural credit metrics and click loops to render correlation data models.")

# --- GEOGRAPHIC LEAD DISTRIBUTION MAP VIEWS ---
st.markdown("---")
st.subheader("📍 Regional Lead Concentration Data")
if not leads.empty and 'business_address' in leads.columns:
    # Safely parse city or full address blocks for visual mapping
    address_series = leads['business_address'].dropna().astype(str)
    if not address_series.empty:
        st.bar_chart(address_series.value_counts())
else:
    st.info("Awaiting compliant verified corporate address entries to construct geographical metrics charts.")
