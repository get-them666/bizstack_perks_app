"""Run Alembic migrations easily from scripts.
Usage: ./scripts/run_migrations.sh
"""
#!/usr/bin/env bash
set -euo pipefail

# Ensure we run in repo root
dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$dir"

# Read DATABASE_URL from env
if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL not set. Using sqlite:///./bizstack.db"
  export DATABASE_URL="sqlite:///./bizstack.db"
fi

echo "Running alembic upgrade head with DATABASE_URL=$DATABASE_URL"
alembic upgrade head
