# CLEANUP_PLAN.md

This branch introduces a cleanup plan and an archive strategy before larger refactors and feature work.

Planned file actions (phase 1):

1. Create /archive and move legacy or backup assets there (non-exhaustive list):
   - bot.py.bak -> archive/bot.py.bak
   - fields.txt -> archive/fields.txt (empty)
   - Any local-only scripts referencing absolute local paths (to be archived or parameterized)

2. Keep the following live and refactor in place:
   - app.py (will be ported or merged into api/)
   - api_server.py (fastapi streaming endpoints - to be consolidated)
   - dashboard.py (Streamlit UI - fix external fetch and gate features)
   - index.html / static pages (update copy and link to new gated features)

3. Consolidate requirements and add SQLAlchemy + Alembic for migrations.

4. Add a proper DB models layout (api/models.py), DB init (api/db.py), and API main app (api/main.py).

5. Implement redirect tracking endpoint (/r/<link_id>) and admin CRUD for deals.

If you want any of the legacy files preserved in root (not archived), list them here.
