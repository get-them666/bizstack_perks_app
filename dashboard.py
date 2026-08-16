import os
import requests
import streamlit as st

PLATFORM_WEB_URL = os.getenv("PLATFORM_WEB_URL", "http://localhost:8080")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me")

st.set_page_config(page_title="BIZSTACK // UNDERWRITING & MONETIZATION CONTROL", layout="wide")

# Navigation Sidebar
tab = st.sidebar.selectbox("View", ["Fintech Leads Dashboard", "Hotel Management"])

if tab == "Fintech Leads Dashboard":
    st.title("🛰️ BIZSTACK FINTECH UNDERWRITING PANEL")
    st.write("Real-time incoming commercial loan leads, underwriting metric flows, and asset valuation vectors.")
    
    # Inline verification box that registers instantly upon pressing Enter
    st.sidebar.markdown("---")
    token_input = st.sidebar.text_input("Admin Verification Token (Press Enter)", type="password", value="")
    
    if token_input == "":
        st.info("🔒 Access Protected. Please input your validation token into the sidebar panel to unlock live streaming fintech telemetry.")
    elif token_input != ADMIN_TOKEN:
        st.error("❌ Invalid Token. Please enter the correct admin validation credentials.")
    else:
        st.sidebar.success("🔓 Authenticated Successfully")
        st.subheader("📊 Active Lead Telemetry Pipelines")
        try:
            r = requests.get(f"{PLATFORM_WEB_URL}/admin/leads", headers={"x-admin-token": token_input})
            if r.status_code == 200:
                leads = r.json()
                st.success(f"Successfully tracking {len(leads)} active business applications!")
                
                # Render interactive metrics table panel
                for lead in leads[:200]:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                        col1.metric("Lead ID", lead.get('id'))
                        col2.markdown(f"### {lead.get('business_name')}")
                        col3.metric("Annual Revenue", f"${lead.get('annual_revenue'):,}" if isinstance(lead.get('annual_revenue'), (int, float)) else f"${lead.get('annual_revenue')}")
                        col4.metric("Underwriting Risk", lead.get('score'), delta="Sellable Asset" if lead.get('sellable') else "Flagged/High Risk", delta_color="normal" if lead.get('sellable') else "inverse")
                        st.markdown("---")
            else:
                st.error(f"Backend Server error: {r.status_code}. Unable to extract database tables.")
        except Exception as e:
            st.error(f"Failed to communicate with active server network: {e}")

elif tab == "Hotel Management":
    st.title("🏨 HOTEL DISTRIBUTION MANAGEMENT MATRIX")
    st.write("Extract live tracking assets matching targeted Marriott and Hilton corporate properties.")
    
    city_target = st.text_input("ENTER REGIONAL AIRPORT IATA CODE (e.g. NYC, LAX, MIA):", value="MIA").upper()
    if st.button("HARVEST LIVE DEALS"):
        st.write(f"🔄 Scanning travel networks for {city_target} tracking vectors...")
        try:
            response = requests.get(f"{PLATFORM_WEB_URL}/api/deals?city={city_target}")
            if response.status_code != 200:
                st.error("Backend returned an error or no data.")
            else:
                deals = response.json()
                if not deals:
                    st.warning("No active properties returned or backend variables initialized.")
                else:
                    st.success(f"Surfaced {len(deals)} valid corporate partnership entries!")
                    for deal in deals:
                        brand_badge = "🏨 [MARRIOTT]" if deal.get('brand') == "Marriott" else "🏨 [HILTON]"
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.subheader(f"{brand_badge} {deal.get('hotel_name')}")
                                st.write(deal.get('city'))
                            with col2:
                                st.markdown(f"[🔗 SECURE BOOKING LINK]({PLATFORM_WEB_URL}/r/{deal.get('id')})")
                            st.markdown("---")
        except Exception as e:
            st.error(f"Failed to communicate with active server network: {e}")
