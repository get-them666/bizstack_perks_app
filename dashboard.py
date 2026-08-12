import streamlit as st
import requests

st.set_page_config(page_title="BIZSTACK // BRAND MONETIZATION CONTROL", layout="wide")
st.title("🛰️ HOTEL DISTRIBUTION MANAGEMENT MATRIX")
st.write("Extract live tracking assets matching targeted Marriott and Hilton corporate properties.")

# 1. User Interface Input Selectors
city_target = st.text_input("ENTER REGIONAL AIRPORT IATA CODE (e.g. NYC, LAX, MIA):", value="MIA").upper()

if st.button("HARVEST LIVE DEALS"):
    st.write(f"🔄 Scanning travel networks for {city_target} tracking vectors...")
    
    try:
        # Route natively through your permanent secure Cloudflare API subdomain pathway
        response = requests.get(f"https://bizstackperks.com{city_target}").json()
        
        deals = response.get("deals", [])
        if not deals:
            st.warning("No active properties returned or backend variables initialized.")
        else:
            st.success(f"Surfaced {len(deals)} valid corporate partnership entries!")
            
            # 2. Render Interactive Visual Data Grid Layout Cards
            for deal in deals:
                brand_badge = "🏨 [MARRIOTT]" if deal['brand'] == "Marriott" else "🏨 [HILTON]"
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(f"{brand_badge} {deal['hotel_name']}")
                    with col2:
                        # Clicking this routes traffic over your profitable link infrastructure
                        st.markdown(f"[🔗 SECURE BOOKING LINK]({deal['monetized_url']})")
                    st.markdown("---")
    except Exception as e:
        st.error(f"Failed to communicate with active server network: {e}")
