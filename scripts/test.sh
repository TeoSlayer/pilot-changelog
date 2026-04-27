#!/usr/bin/env bash
# test.sh — run the pilot-changelog self-test suite.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
exec python3 "$SCRIPT_DIR/test.py" "$@"
