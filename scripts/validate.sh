#!/usr/bin/env bash
# validate.sh — validate frontmatter on every entry. Exits non-zero on error.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
exec python3 "$SCRIPT_DIR/validate.py" "$@"
