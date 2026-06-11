#!/usr/bin/env bash
# Grihine Soap — push hostinger-deploy/ live to Hostinger.
# Usage: ./deploy.sh        (credentials read from .deploy.env next to this script)
set -euo pipefail

cd "$(dirname "$0")"

if [[ -f .deploy.env ]]; then
  set -a
  source .deploy.env
  set +a
else
  echo "✗ .deploy.env not found."
  echo "  cp .deploy.env.example .deploy.env   — then fill in the FTP details from hPanel."
  exit 1
fi

python3 deploy/deploy.py
