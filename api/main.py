import os
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI(title="BizStack Perks Platform API")

# Temporary in-memory lookup map to redirect affiliate links
DEALS_DATABASE = {
    "D001": "https://marriott.com",
    "D002": "https://hilton.com"
}

@app.get("/")
async def health_check():
    return {"status": "healthy", "engine": "BizStack Perks Platform"}

# FIX THE REDIRECT ROUTE (Resolves affiliate link 404s)
@app.get("/r/{link_id}")
async def redirect_to_deal(link_id: str):
    target_url = DEALS_DATABASE.get(link_id)
    if not target_url:
        # If specific ID isn't found, fallback to your main site home page
        return RedirectResponse(url="http://localhost:8501")
    return RedirectResponse(url=target_url)

# FINTECH LEADS ROUTE
@app.get("/admin/leads")
async def get_admin_leads(x_admin_token: str = Header(None)):
    if x_admin_token != "change-me":
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    mock_leads = [
        {"id": "L101", "business_name": "Apex Fintech Solutions", "annual_revenue": 1450000, "score": 88, "sellable": True},
        {"id": "L102", "business_name": "Vanguard Logistics Group", "annual_revenue": 620000, "score": 42, "sellable": False},
        {"id": "L103", "business_name": "Beacon E-Commerce Hub", "annual_revenue": 2100000, "score": 95, "sellable": True}
    ]
    return mock_leads

# HOTEL DEALS ROUTE
@app.get("/api/deals")
async def get_deals(city: str = Query("MIA")):
    city_upper = city.upper()
    mock_deals = [
        {"id": "D001", "brand": "Marriott", "hotel_name": f"{city_upper} Airport Marriott Premium", "city": city_upper},
        {"id": "D002", "brand": "Hilton", "hotel_name": f"The Hilton Downtown {city_upper} Core", "city": city_upper}
    ]
    return mock_deals
