#!/usr/bin/env python3
"""CI smoke test script for BizStack Perks
This script runs a set of basic HTTP checks against a running local API.
It expects the API to be accessible at http://127.0.0.1:8080 by default.

Exit codes:
  0 - all checks passed
  2 - one or more checks failed
"""
import os
import sys
import time
import requests

BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8080')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'test_admin_token')

TIMEOUT = 30


def wait_for_health(url, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{url}/health", timeout=3)
            if r.status_code == 200:
                print('[ok] /health')
                return True
        except Exception as e:
            print('.', end='', flush=True)
        time.sleep(1)
    print('\n[error] /health did not become available')
    return False


def check_get_deals(url):
    try:
        r = requests.get(f"{url}/api/deals", timeout=5)
        print(f"GET /api/deals -> {r.status_code}")
        if r.status_code != 200:
            print('unexpected status for /api/deals:', r.text)
            return False
        try:
            data = r.json()
            print('deals count:', len(data) if isinstance(data, list) else 'N/A')
        except Exception:
            print('response not JSON for /api/deals')
        return True
    except Exception as e:
        print('error fetching /api/deals', e)
        return False


def simulate_checkout(url):
    try:
        payload = {"product_name": "CI Test Report", "price_cents": 100}
        r = requests.post(f"{url}/api/stripe/create-checkout-session", json=payload, timeout=5)
        print('POST /api/stripe/create-checkout-session ->', r.status_code)
        if r.status_code not in (200, 201):
            print('unexpected status:', r.text)
            return False
        data = r.json()
        simulate_url = data.get('simulate_url') or data.get('url') or data.get('checkout_url')
        if not simulate_url:
            print('no simulate/checkout url in response:', data)
            return False
        print('simulate_url:', simulate_url)
        # follow the simulate URL
        r2 = requests.get(simulate_url, timeout=10)
        print('GET simulate_url ->', r2.status_code)
        return r2.status_code in (200, 302, 303, 307)
    except Exception as e:
        print('error during simulate checkout', e)
        return False


def create_lead(url):
    try:
        payload = {"business_name": "CI Test LLC", "annual_revenue": 50000, "credit_score": 700}
        r = requests.post(f"{url}/api/leads", json=payload, timeout=5)
        print('POST /api/leads ->', r.status_code)
        return r.status_code in (200, 201)
    except Exception as e:
        print('error creating lead', e)
        return False


def admin_export_csv(url, admin_token):
    try:
        headers = {"x-admin-token": admin_token}
        r = requests.get(f"{url}/admin/export/leads/csv", headers=headers, timeout=5)
        print('GET /admin/export/leads/csv ->', r.status_code)
        return r.status_code == 200
    except Exception as e:
        print('error exporting csv', e)
        return False


if __name__ == '__main__':
    print('CI smoke test starting against', BASE_URL)
    ok = True

    if not wait_for_health(BASE_URL, timeout=TIMEOUT):
        sys.exit(2)

    if not check_get_deals(BASE_URL):
        ok = False

    if not simulate_checkout(BASE_URL):
        ok = False

    if not create_lead(BASE_URL):
        ok = False

    if not admin_export_csv(BASE_URL, ADMIN_TOKEN):
        ok = False

    if not ok:
        print('\nOne or more smoke checks failed')
        sys.exit(2)

    print('\nAll smoke checks passed')
    sys.exit(0)
