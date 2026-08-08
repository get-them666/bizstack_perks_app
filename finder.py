import requests
import pandas as pd
import time
import webbrowser

ZIP_CODE = "23321"
RADIUS = "75"
START_YEAR = 2013
END_YEAR = 2018
MAKERS = ["honda", "toyota", "subaru"]

# Coordinates approximate to 23321 center for geo-targeted API boundaries
LATITUDE = 36.8444
LONGITUDE = -76.4111

def fetch_craigslist():
    print("🚗 [SOURCE 1/3] Pulling Private Owner Listings from Craigslist...")
    listings = []
    for make in MAKERS:
        url = "https://craigslist.org"
        params = {"search_distance": RADIUS, "postal": ZIP_CODE, "query": make, "purveyor": "owner"}
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        
        try:
            res = requests.get(url, params=params, headers=headers, timeout=10)
            if res.status_code == 200:
                items = res.json().get("items", [])
                for item in items:
                    title = item.get("title", "Unknown Title")
                    url_path = item.get("url", "")
                    link = f"https://craigslist.org{url_path}" if url_path.startswith("/") else url_path
                    
                    year_match = next((y for y in range(START_YEAR, END_YEAR + 1) if str(y) in title.lower()), None)
                    if year_match:
                        listings.append({
                            "Source": "Craigslist (Private)",
                            "Make": make.capitalize(),
                            "Year": year_match,
                            "Title": title,
                            "Price": item.get("price", "N/A"),
                            "Link": link
                        })
            time.sleep(1)
        except Exception:
            continue
    return listings

def generate_facebook_marketplace_links():
    print("\n🌐 [SOURCE 2/3] Generating Authenticated Facebook Marketplace Portals...")
    # FB Marketplace tracks location by explicit coordinates or structured strings
    # We construct a pre-filtered direct interface layout mapping 2013-2018 models within 75 miles (121 KM)
    fb_links = []
    for make in MAKERS:
        fb_url = (
            f"https://facebook.com"
            f"?exact=false"
            f"&latitude={LATITUDE}"
            f"&longitude={LONGITUDE}"
            f"&radius=121"  # 75 miles in kilometers
            f"&minYear={START_YEAR}"
            f"&maxYear={END_YEAR}"
            f"&query={make}"
        )
        fb_links.append({"Source": "Facebook Marketplace Link", "Make": make.capitalize(), "Portal URL": fb_url})
    return fb_links

def generate_local_dealer_links():
    print("🏢 [SOURCE 3/3] Generating Major Dealer Inventory Portals (Chesapeake/Norfolk/VA Beach)...")
    # Generates deep links directly into localized platforms handling inventory near 23321
    dealer_links = []
    for make in MAKERS:
        # Priority Toyota Chesapeake inventory filtering path
        priority_url = f"https://prioritytoyotachesapeake.com{START_YEAR}-{END_YEAR}&make={make.capitalize()}"
        dealer_links.append({"Source": "Priority Auto Group Network", "Make": make.capitalize(), "Portal URL": priority_url})
        
        # Broad regional network inventory aggregation via Edmunds API link targeting local parameters
        edmunds_url = f"https://edmunds.com{RADIUS}&zip={ZIP_CODE}&year={START_YEAR}-{END_YEAR}&make={make}"
        dealer_links.append({"Source": "Regional Dealer Aggregator (Edmunds)", "Make": make.capitalize(), "Portal URL": edmunds_url})
    return dealer_links

def main():
    # Execute structural background scrapes
    cl_results = fetch_craigslist()
    cl_df = pd.DataFrame(cl_results)
    
    # Generate secure front-end interaction link sets
    fb_data = generate_facebook_marketplace_links()
    fb_df = pd.DataFrame(fb_data)
    
    dealer_data = generate_local_dealer_links()
    dealer_df = pd.DataFrame(dealer_data)
    
    # Export dedicated logs for your dashboard
    if not cl_df.empty:
        cl_df.to_csv("craigslist_listings.csv", index=False)
        print(f"\n📊 Extracted {len(cl_df)} raw private listings to 'craigslist_listings.csv'")
        
    fb_df.to_csv("facebook_search_links.csv", index=False)
    dealer_df.to_csv("local_dealers_search_links.csv", index=False)
    print("💾 Compiled secure live entry points to 'facebook_search_links.csv' and 'local_dealers_search_links.csv'")
    
    print("\n🚀 UI Prompt: Do you want to instantly launch your browser portals to scan Facebook & Local Dealers?")
    choice = input("Type 'yes' to open windows, or press Enter to skip: ").strip().lower()
    
    if choice == 'yes':
        print("\nOpening live matching interfaces...")
        # Open the generated portal URLs seamlessly in your system browser
        for link in fb_data + dealer_data:
            print(f"🔗 Launching filtered search window for {link['Make']} via {link['Source']}...")
            webbrowser.open(link['Portal URL'])
            time.sleep(1) # Paced timing prevent system window freezing

if __name__ == "__main__":
    main()
