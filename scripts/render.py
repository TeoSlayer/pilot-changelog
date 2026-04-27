#!/usr/bin/env python3
"""Render changelog entries to feed.json (+ windowed variants) and feed.md.

Zero deps — uses a minimal frontmatter parser that handles the bounded
schema we actually use (scalars, booleans, inline lists, block lists).

Outputs (relative to repo root):
  feed.json            all-time, public
  feed-1d.json         last 24h, public
  feed-7d.json         last 7 days, public
  feed-1m.json         last 30 days, public
  feed-flagged.json    flagged: true, public, all-time
  feed.md              human-readable timeline, public
  feed-private.json    all-time, all visibilities (gitignored)
  feed-private.md      same, markdown (gitignored)
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIRS = [REPO_ROOT / "entries", REPO_ROOT / "private"]
ALLOWED_SCOPES = {"protocol", "networks", "skills", "infra", "ops", "docs"}
ALLOWED_VISIBILITY = {"public", "private"}


@dataclass
class Entry:
    id: str
    date: str
    scope: str
    visibility: str
    title: str
    flagged: bool = False
    links: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)
    body: str = ""
    excerpt: str = ""
    source_path: str = ""

    def to_public_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("source_path", None)
        return d


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse a leading `---\\n…\\n---\\n` YAML-ish block.

    Returns ({}, text) when no frontmatter is present.
    """
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        end = text.find("\n---", 4)
        if end == -1:
            return {}, text
        body = text[end + 4:]
    else:
        body = text[end + 5:]
    fm_text = text[4:end]

    fm: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in fm_text.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") or raw.startswith("- "):
            if current_list_key is None:
                continue
            val = raw.split("-", 1)[1].strip()
            val = _unquote(val)
            fm[current_list_key].append(val)
            continue
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()
        if not val:
            fm[key] = []
            current_list_key = key
            continue
        current_list_key = None
        fm[key] = _coerce_scalar(val)
    return fm, body


def _unquote(val: str) -> str:
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        return val[1:-1]
    return val


def _coerce_scalar(val: str) -> Any:
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_unquote(x.strip()) for x in inner.split(",") if x.strip()]
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    return _unquote(val)


def first_paragraph(body: str) -> str:
    body = body.lstrip()
    # Skip HTML comments at the top of the body.
    while body.startswith("<!--"):
        end = body.find("-->")
        if end == -1:
            break
        body = body[end + 3:].lstrip()
    para: list[str] = []
    for line in body.split("\n"):
        if not line.strip():
            if para:
                break
            continue
        if line.startswith("#"):
            continue
        para.append(line.strip())
    return " ".join(para)


def load_entries() -> list[Entry]:
    entries: list[Entry] = []
    for d in ENTRIES_DIRS:
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            if not fm:
                print(f"skip (no frontmatter): {path}", file=sys.stderr)
                continue
            entries.append(
                Entry(
                    id=path.stem,
                    date=str(fm.get("date", "")),
                    scope=str(fm.get("scope", "")),
                    visibility=str(fm.get("visibility", "")),
                    title=str(fm.get("title", "")),
                    flagged=bool(fm.get("flagged", False)),
                    links=[str(x) for x in fm.get("links", []) if x],
                    ids=[str(x) for x in fm.get("ids", [])],
                    body=body.strip(),
                    excerpt=first_paragraph(body),
                    source_path=str(path.relative_to(REPO_ROOT)),
                )
            )
    # Sort newest first by (date, id).
    entries.sort(key=lambda e: (e.date, e.id), reverse=True)
    return entries


def parse_date(s: str) -> datetime | None:
    try:
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def filter_window(entries: list[Entry], days: int, now: datetime) -> list[Entry]:
    cutoff = now - timedelta(days=days)
    out = []
    for e in entries:
        d = parse_date(e.date)
        if d is None:
            continue
        if d >= cutoff:
            out.append(e)
    return out


def write_json_feed(
    path: Path,
    *,
    entries: list[Entry],
    window: str,
    include_private: bool,
    now: datetime,
) -> None:
    payload = {
        "generated_at": now.isoformat(),
        "window": window,
        "include_private": include_private,
        "count": len(entries),
        "entries": [e.to_public_dict() for e in entries],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)} ({len(entries)} entries)")


def write_markdown_feed(path: Path, entries: list[Entry], *, title: str) -> None:
    lines = [f"# {title}", ""]
    last_month = ""
    for e in entries:
        month = e.date[:7] if len(e.date) >= 7 else "unknown"
        if month != last_month:
            lines.append(f"## {month}")
            lines.append("")
            last_month = month
        flag = " ⚑" if e.flagged else ""
        vis = "" if e.visibility == "public" else f" *(private)*"
        lines.append(f"### {e.date} — {e.title}{flag}{vis}")
        lines.append(f"_scope: `{e.scope}`_")
        lines.append("")
        if e.body:
            lines.append(e.body)
            lines.append("")
        if e.links:
            lines.append("**Links:** " + " · ".join(e.links))
            lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)} ({len(entries)} entries)")


def main() -> int:
    now = datetime.now(timezone.utc)
    all_entries = load_entries()
    public = [e for e in all_entries if e.visibility == "public"]

    write_json_feed(REPO_ROOT / "feed.json", entries=public, window="all", include_private=False, now=now)
    write_json_feed(REPO_ROOT / "feed-1d.json", entries=filter_window(public, 1, now), window="1d", include_private=False, now=now)
    write_json_feed(REPO_ROOT / "feed-7d.json", entries=filter_window(public, 7, now), window="7d", include_private=False, now=now)
    write_json_feed(REPO_ROOT / "feed-1m.json", entries=filter_window(public, 30, now), window="1m", include_private=False, now=now)
    write_json_feed(REPO_ROOT / "feed-flagged.json", entries=[e for e in public if e.flagged], window="flagged", include_private=False, now=now)

    write_markdown_feed(REPO_ROOT / "feed.md", public, title="Pilot Protocol Changelog")

    # Private mirror outputs — gitignored, operator console only.
    write_json_feed(REPO_ROOT / "feed-private.json", entries=all_entries, window="all", include_private=True, now=now)
    write_markdown_feed(REPO_ROOT / "feed-private.md", all_entries, title="Pilot Protocol Changelog (operator)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
