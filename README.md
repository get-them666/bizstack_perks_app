# BizStack Perks — Monetization & Underwriting Platform

BizStack Perks is a SaaS-oriented analytics and ingestion dashboard for capturing commercial financing leads, tracking premium card interactions, and surfacing monetized partner links. This branch starts a focused overhaul to consolidate the backend, restore underwriting flows, and add monetization (affiliate redirects + Stripe Checkout).

Short summary
- Purpose: capture and score loan underwriting leads, monetize card clicks and booking links, and offer paid exports and premium dashboard features.
- Primary runtime: Streamlit dashboard (dashboard.py) for UI, FastAPI backend for APIs and webhooks.

Stack
- Languages: Python, HTML, Shell
- Frameworks: FastAPI (backend), Streamlit (dashboard)
- Notable libs: requests, SQLAlchemy, Stripe (payments), Alembic (migrations), Uvicorn

Quick start (development)
1. Create a virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install streamlit
```

2. Run the API (development):

```bash
# from repo root
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

3. Run the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

Environment variables (fill before running production):
- STRIPE_SECRET_KEY
- STRIPE_PUBLISHABLE_KEY
- DATABASE_URL (sqlite:///./bizstack.db or a postgres URL)
- SENDER_EMAIL
- PLATFORM_WEB_URL

What I changed in this branch
- Added an initial README with run steps and the project pitch.
- Consolidated development requirements (see requirements.txt) and added a cleanup plan.

Next steps (what I will implement next)
1. Consolidate Flask + FastAPI into a single FastAPI backend (api/) with models and DB migration.
2. Add redirect tracking endpoint (/r/<link_id>) and admin CRUD for deals.
3. Implement Stripe Checkout + webhook to record payments and gate premium features.
4. Implement simple underwriting scoring and lead export.

If you want me to proceed now, confirm the following:
- Payment provider: Stripe (yes/no)
- Hosting target (Render/Heroku/DigitalOcean/AWS/custom)
- Email provider (SendGrid/Mailgun/SMTP) — optional now
- Whether you want leads sold (yes/no)

I will not commit any API keys or secrets — provide them using environment variables on the host.
