import os
import requests
import streamlit as st

PLATFORM_WEB_URL = os.getenv("PLATFORM_WEB_URL", "http://localhost:8080")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me")

st.set_page_config(page_title="BIZSTACK PERKS // SYSTEM MONETIZATION PLATFORM", layout="wide")

# Modernized multi-page tab layout selectors
tab = st.sidebar.selectbox("Navigation Core", [
    "01 / STRATEGIC CAPITAL INTAKE", 
    "02 / CORPORATE YIELD ADVISING", 
    "Hotel Distribution Matrix",
    "System Admin Portal"
])

if tab == "01 / STRATEGIC CAPITAL INTAKE":
    st.title("🛰️ 01 / STRATEGIC CAPITAL INTAKE")
    st.subheader("Secure Underwriting Ingestion Gateway")
    st.write("Submit structural operational metrics, gross annual revenue milestones, and foundational credit assessments directly into our database loops.")
    
    with st.form("lead_ingest_form"):
        biz_name = st.text_input("Commercial Entity Legal Name")
        revenue = st.number_input("Gross Annual Verified Revenue ($)", min_value=0.0, format="%.2f")
        submit_btn = st.form_submit_button("OPEN INGESTION TERMINAL →")
        
        if submit_btn:
            if biz_name:
                try:
                    payload = {"business_name": biz_name, "annual_revenue": revenue}
                    r = requests.post(f"{PLATFORM_WEB_URL}/api/v1/leads/ingest", json=payload)
                    if r.status_code == 200:
                        data = r.json()
                        st.success(f"✔️ Lead ingested successfully! Underwriting Score: {data.get('score')} | Sellable: {data.get('sellable')}")
                    else:
                        st.error("Backend error compiling ingestion files.")
                except Exception as e:
                    st.error(f"Connection failure: {e}")
            else:
                st.warning("Please provide a valid company identity name.")

elif tab == "02 / CORPORATE YIELD ADVISING":
    st.title("⚡ 02 / CORPORATE YIELD ADVISING")
    st.subheader("Enterprise Benefit Monetization Matrix")
    st.write("Unlock optimized organizational asset setups, tax-advantaged operational spending models, and view premium card structures.")
    
    st.info("🔒 Premium Modules Gated. Access requires a valid premium license pass.")
    
    if st.button("EXECUTE PROPOSAL SESSION PIPELINE →"):
        try:
            r = requests.post(f"{PLATFORM_WEB_URL}/api/v1/checkout/premium")
            if r.status_code == 200:
                checkout_link = r.json().get("checkout_url")
                # Native, prominent, unbreakable full-width Stripe check-out pass button
                st.link_button("💳 OPEN SECURE STRIPE CHECKOUT TERMINAL", checkout_link, use_container_width=True, type="primary")
                st.caption("A billing tunnel has been constructed. Click the prominent colored button above to complete your transaction.")
            else:
                st.error("Failed to generate a custom checkout engine session.")
        except Exception as e:
            st.error(f"Unable to contact Stripe infrastructure loops: {e}")

elif tab == "Hotel Distribution Matrix":
    st.title("🏨 HOTEL DISTRIBUTION MANAGEMENT MATRIX")
    st.write("Extract live tracking assets matching targeted Marriott and Hilton corporate properties.")
    
    city_target = st.text_input("ENTER REGIONAL AIRPORT IATA CODE (e.g. NYC, LAX, MIA):", value="MIA").upper()
    if st.button("HARVEST LIVE DEALS"):
        try:
            response = requests.get(f"{PLATFORM_WEB_URL}/api/deals?city={city_target}")
            if response.status_code == 200:
                deals = response.json()
                st.success(f"Surfaced {len(deals)} valid entries!")
                for deal in deals:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(f"🏨 [{deal.get('brand').upper()}] {deal.get('hotel_name')}")
                            st.write(f"Tracking regional point: **{deal.get('city')}**")
                        with col2:
                            # Native, unbreakable layout button matching your primary red panel design theme
                            redirect_path = f"{PLATFORM_WEB_URL}/r/{deal.get('id')}"
                            st.link_button("🔗 SECURE BOOKING LINK", redirect_path, use_container_width=True)
                        st.markdown("---")
            else:
                st.error("Backend returned an error code.")
        except Exception as e:
            st.error(f"Error: {e}")

elif tab == "System Admin Portal":
    st.title("🔑 Admin System Management")
    token_input = st.text_input("Verify Admin Credential Token", type="password")
    if token_input != ADMIN_TOKEN:
        st.warning("Authentication required to view system data streams.")
    else:
        st.success("Developer credential cleared.")
        try:
            r = requests.get(f"{PLATFORM_WEB_URL}/admin/leads", headers={"x-admin-token": token_input})
            if r.status_code == 200:
                leads = r.json()
                st.write(f"Showing {len(leads)} active underwriting profiles:")
                st.json(leads)
            else:
                st.error("Error retrieving background tables.")
        except Exception as e:
            st.error(f"Connection error: {e}")
