PR Title: Phase A — Local hardening, migrations, admin UI, and smoke tests

Summary

This PR completes Phase A of the saas-monetize-overhaul work and prepares the codebase for Phase B (Stripe test integration) and Phase C (VAPI streaming). It includes:

- Alembic scaffold and an initial migration (alembic/versions/0001_initial.py) that creates the core tables (deals, leads, click_events, premium_orders, underwrite_assessments).
- Docker Compose adjusted to run `alembic upgrade head` before starting the API.
- scripts/run_migrations.sh to run migrations easily in dev.
- scripts/generate_admin_token.sh to generate a secure ADMIN_TOKEN.
- Streamlit dashboard Admin tab and API admin endpoints requiring X-Admin-Token.
- Simulated Stripe flow endpoints and a /api/stripe/simulate/checkout endpoint for local testing.
- up.sh launcher and systemd unit templates for VM deploy.
- scripts/seed_sample_data.py and scripts/ingest_corpus.py for easy local seeding and RAG corpus ingestion.
- Dockerfile and minimal CI workflow.

Checklist (to verify before merging)

Phase A acceptance criteria:
- [ ] Docker Compose builds and `alembic upgrade head` runs without error (on a clean SQLite or provided Postgres DB).
- [ ] `docker-compose up` starts API and Streamlit successfully and both respond to /health and the UI loads.
- [ ] Seeding: `python scripts/seed_sample_data.py` creates sample deals visible in the dashboard.
- [ ] RAG ingestion: `python scripts/ingest_corpus.py` populates corpus/repo_docs.jsonl.
- [ ] Redirect tracking: clicking a deal (dashboard link /r/<id>) creates a click_events record.
- [ ] Simulated purchase: POST /api/stripe/create-checkout-session returns a simulate URL; visiting the URL creates a premium_orders record.
- [ ] Lead ingestion: POST /api/leads creates a lead and a corresponding underwrite_assessments record.
- [ ] Admin controls: Streamlit Admin tab authenticates with ADMIN_TOKEN and allows creating deals and exporting leads CSV.
- [ ] No secrets are present in the repo.

How to test locally (short)

1) Create a .env at repo root or export env vars in your shell:

```
ADMIN_TOKEN=your_admin_token_here
STRIPE_MODE=simulate
DATABASE_URL=sqlite:///./bizstack.db
PLATFORM_WEB_URL=http://localhost:8080
SENDER_EMAIL=you@yourdomain.test
```

2) Build & run (recommended):

```
docker-compose up --build
```

3) Alternatively, without Docker:

```
./scripts/run_migrations.sh
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
streamlit run dashboard.py --server.port 8501 --server.headless true
```

4) Seed and ingest corpus:

```
python scripts/seed_sample_data.py
python scripts/ingest_corpus.py
```

5) Exercise flows:
- API health: GET /health
- List deals: GET /api/deals
- Redirect: visit /r/<deal_id>
- Simulate purchase: POST /api/stripe/create-checkout-session and visit returned simulate URL
- Create lead: POST /api/leads
- Admin export: use Admin tab or GET /admin/export/leads/csv with X-Admin-Token header

Notes for reviewers
- No production or live API keys are included. Add Stripe and VAPI credentials as environment variables in CI/host when moving to Phase B/C.
- The RAG retrieval is intentionally lightweight (JSONL corpus). For production consider Redis/Weaviate/Milvus.
- I recommend migrating from SQLite to a managed Postgres instance for production.

Next steps (Phase B & C)
- Phase B (Stripe test): switch STRIPE_MODE to test, add test keys to host or GitHub secrets, enable real Checkout flow and webhook verification.
- Phase C (VAPI streaming): add VAPI_API_KEY and VAPI_PROJECT_ID to host secrets, finish vapi_wrapper streaming integration, run RAG tests and tune persona.

