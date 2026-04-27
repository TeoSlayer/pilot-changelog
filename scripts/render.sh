#!/usr/bin/env bash
# render.sh — regenerate all feed.* outputs from entries/ and private/.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
exec python3 "$SCRIPT_DIR/render.py" "$@"
