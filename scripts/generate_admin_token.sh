#!/bin/bash
# scripts/generate_admin_token.sh
# Generates a secure ADMIN_TOKEN you can export into your environment

python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY

# Example usage:
# ADMIN_TOKEN=$(./scripts/generate_admin_token.sh)
# export ADMIN_TOKEN
