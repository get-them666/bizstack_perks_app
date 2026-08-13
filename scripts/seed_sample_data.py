"""Seed script to add sample deals and optionally sample leads to a running local API.
Usage: python scripts/seed_sample_data.py
This script assumes the API is running at PLATFORM_WEB_URL (default http://localhost:8080).
"""
import os
import requests

PLATFORM = os.getenv('PLATFORM_WEB_URL', 'http://localhost:8080')

SAMPLE_DEALS = [
    {"brand": "Marriott", "hotel_name": "Marriott Downtown MIA", "city": "MIA", "monetized_url": "https://example.com/book/marriott-downtown"},
    {"brand": "Hilton", "hotel_name": "Hilton Garden LAX", "city": "LAX", "monetized_url": "https://example.com/book/hilton-garden"},
    {"brand": "Marriott", "hotel_name": "Marriott Corporate Hub NYC", "city": "NYC", "monetized_url": "https://example.com/book/marriott-nyc"},
]


def create_deal(d):
    r = requests.post(f"{PLATFORM}/api/deals/", json=d)
    print('create_deal', r.status_code, r.text)


def seed():
    for d in SAMPLE_DEALS:
        create_deal(d)

if __name__ == '__main__':
    seed()
