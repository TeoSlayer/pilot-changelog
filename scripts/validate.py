#!/usr/bin/env python3
"""Validate frontmatter on every entry. Exits non-zero on the first error."""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path

from render import parse_frontmatter, ALLOWED_SCOPES, ALLOWED_VISIBILITY

REPO_ROOT = Path(os.environ.get("PILOT_CHANGELOG_ROOT") or Path(__file__).resolve().parent.parent)
DIRS = [REPO_ROOT / "entries", REPO_ROOT / "private"]
FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
REQUIRED = ("date", "scope", "visibility", "title")


def err(path: Path, msg: str) -> None:
    print(f"validate: {path.relative_to(REPO_ROOT)}: {msg}", file=sys.stderr)


def validate_file(path: Path) -> bool:
    ok = True
    name = path.name

    m = FILENAME_RE.match(name)
    if not m:
        err(path, f"filename must match YYYY-MM-DD-slug.md (got {name!r})")
        ok = False

    text = path.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    if not fm:
        err(path, "missing or malformed frontmatter")
        return False

    for key in REQUIRED:
        if not fm.get(key):
            err(path, f"missing required field: {key}")
            ok = False

    date_val = str(fm.get("date", ""))
    try:
        datetime.strptime(date_val, "%Y-%m-%d")
    except ValueError:
        err(path, f"date must be YYYY-MM-DD (got {date_val!r})")
        ok = False

    if m and date_val and m.group(1) != date_val:
        err(path, f"filename date {m.group(1)!r} != frontmatter date {date_val!r}")
        ok = False

    scope = str(fm.get("scope", ""))
    if scope and scope not in ALLOWED_SCOPES:
        err(path, f"scope {scope!r} not in {sorted(ALLOWED_SCOPES)}")
        ok = False

    visibility = str(fm.get("visibility", ""))
    if visibility and visibility not in ALLOWED_VISIBILITY:
        err(path, f"visibility {visibility!r} not in {sorted(ALLOWED_VISIBILITY)}")
        ok = False

    # Visibility must match directory.
    parent = path.parent.name
    if visibility == "public" and parent != "entries":
        err(path, f"public entry must live under entries/ (found in {parent}/)")
        ok = False
    if visibility == "private" and parent != "private":
        err(path, f"private entry must live under private/ (found in {parent}/)")
        ok = False

    flagged = fm.get("flagged", False)
    if not isinstance(flagged, bool):
        err(path, f"flagged must be true/false (got {flagged!r})")
        ok = False

    return ok


def main() -> int:
    files: list[Path] = []
    for d in DIRS:
        if d.is_dir():
            files.extend(sorted(d.glob("*.md")))

    if not files:
        print("validate: no entries to check", file=sys.stderr)
        return 0

    failures = 0
    for f in files:
        if not validate_file(f):
            failures += 1

    if failures:
        print(f"validate: {failures} file(s) failed validation", file=sys.stderr)
        return 1
    print(f"validate: ok ({len(files)} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
