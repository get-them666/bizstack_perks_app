import os
import requests
import streamlit as st

PLATFORM_WEB_URL = os.getenv("PLATFORM_WEB_URL", "http://localhost:8080")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me")

st.set_page_config(page_title="BIZSTACK // UNDERWRITING & MONETIZATION CONTROL", layout="wide")

# Expanded navigation tabs
tab = st.sidebar.selectbox("View", ["Fintech Leads Dashboard", "Hotel Management", "Admin Console"])

if tab == "Fintech Leads Dashboard":
    st.title("🛰️ BIZSTACK FINTECH UNDERWRITING PANEL")
    st.write("Real-time incoming commercial loan leads, underwriting metric flows, and asset valuation vectors.")
    
    # Render lead monitoring panel openly on landing page
    token_input = st.sidebar.text_input("Enter Admin Token for Protected Ingestions", type="password", value=ADMIN_TOKEN)
    
    st.subheader("📊 Active Lead Telemetry Pipelines")
    try:
        r = requests.get(f"{PLATFORM_WEB_URL}/admin/leads", headers={"x-admin-token": token_input})
        if r.status_code == 200:
            leads = r.json()
            st.success(f"Successfully tracking {len(leads)} active business applications!")
            
            # Create interactive table view metrics
            for lead in leads[:200]:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                    col1.metric("ID", lead.get('id'))
                    col2.write(f"**Business Name:** {lead.get('business_name')}")
                    col3.metric("Annual Revenue", f"${lead.get('annual_revenue'):,}" if isinstance(lead.get('annual_revenue'), (int, float)) else f"${lead.get('annual_revenue')}")
                    col4.metric("Risk Score", lead.get('score'), delta="Sellable" if lead.get('sellable') else "Flagged", delta_color="normal" if lead.get('sellable') else "inverse")
                    st.markdown("---")
        else:
            st.info("API server is active. Enter your valid configuration token in the sidebar panel to pipe live lead data streams.")
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

elif tab == "Admin Console":
    st.title("🔑 Admin Action Console")
    token_input = st.text_input("Admin token Verification", type="password")
    if token_input != ADMIN_TOKEN:
        st.warning("Enter the correct admin token to access administrative submission features.")
    else:
        st.success("Admin identity verified.")
        
        st.subheader("Create New Corporate Deal Asset")
        with st.form(key='create_deal'):
            brand = st.text_input('Brand')
            hotel_name = st.text_input('Hotel name')
            city = st.text_input('City')
            monetized_url = st.text_input('Monetized URL')
            submit = st.form_submit_button('Create')
            if submit:
                payload = {"brand": brand, "hotel_name": hotel_name, "city": city, "monetized_url": monetized_url}
                try:
                    r = requests.post(f"{PLATFORM_WEB_URL}/api/deals/", json=payload)
                    if r.status_code == 200:
                        st.success('Deal created successfully.')
                    else:
                        st.error(f'Failed to create deal: {r.text}')
                except Exception as e:
                    st.error(f'Error pushing asset matrix: {e}')
                    
        st.markdown('---')
        st.subheader('Export SaaS Underwriting Leads (CSV)')
        if st.button('Generate CSV Datagram'):
            try:
                export_url = f"{PLATFORM_WEB_URL}/admin/export/leads/csv"
                st.markdown(f"[📥 Download Compiled CSV Dataset]({export_url})")
            except Exception as e:
                st.error(f'Error preparing export: {e}')
