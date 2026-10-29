#!/usr/bin/env bash
# The one check agents and CI run before calling a change done.
set -euo pipefail
cd "$(dirname "$0")/.."

# Lint and byte-compile the sources in a throwaway container; nothing is installed on the host.
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD:/app" -w /app -e PYTHONPYCACHEPREFIX=/tmp/pyc python:3.12-slim sh -c \
  "pip install --quiet --no-cache-dir --root-user-action=ignore ruff==0.6.8 && ruff check src && python -m compileall -q src"
