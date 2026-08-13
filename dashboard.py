import os
import requests
import streamlit as st

PLATFORM_WEB_URL = os.getenv("PLATFORM_WEB_URL", "http://localhost:8080")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me")

st.set_page_config(page_title="BIZSTACK // BRAND MONETIZATION CONTROL", layout="wide")

# Simple navigation tabs
tab = st.sidebar.selectbox("View", ["Dashboard", "Admin"])

if tab == "Dashboard":
    st.title("🛰️ HOTEL DISTRIBUTION MANAGEMENT MATRIX")
    st.write("Extract live tracking assets matching targeted Marriott and Hilton corporate properties.")

    # 1. User Interface Input Selectors
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
                                # Use redirect route to track clicks
                                st.markdown(f"[🔗 SECURE BOOKING LINK]({PLATFORM_WEB_URL}/r/{deal.get('id')})")
                            st.markdown("---")
        except Exception as e:
            st.error(f"Failed to communicate with active server network: {e}")

elif tab == "Admin":
    st.title("🔐 Admin Console")
    token_input = st.text_input("Admin token", type="password")
    if token_input != ADMIN_TOKEN:
        st.warning("Enter the correct admin token to access admin features.")
    else:
        st.success("Admin authenticated")
        st.subheader("Create Deal")
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
                        st.success('Deal created')
                    else:
                        st.error(f'Failed to create deal: {r.text}')
                except Exception as e:
                    st.error(f'Error: {e}')

        st.subheader("Leads")
        try:
            r = requests.get(f"{PLATFORM_WEB_URL}/admin/leads", headers={"x-admin-token": token_input})
            if r.status_code == 200:
                leads = r.json()
                st.write(f"Showing {len(leads)} leads")
                for lead in leads[:200]:
                    st.write(f"{lead.get('id')} — {lead.get('business_name')} — ${lead.get('annual_revenue')} — score={lead.get('score')} — sellable={lead.get('sellable')}")
            else:
                st.error('Failed to fetch leads')
        except Exception as e:
            st.error(f'Error fetching leads: {e}')

        st.markdown('---')
        st.subheader('Export Leads (CSV)')
        if st.button('Get CSV Export'):
            try:
                export_url = f"{PLATFORM_WEB_URL}/admin/export/leads/csv"
                # Streamlit can't directly download remote CSV without link; show link
                st.markdown(f"[Download CSV]({export_url})")
            except Exception as e:
                st.error(f'Error preparing export: {e}')
