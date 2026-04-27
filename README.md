# pilot-changelog

Single chronological feed of "what changed across the Pilot Protocol
platform." One git repo, multiple rendered outputs — public ones feed
the onboarding agent and the daily context bundle; private ones stay
in operator hands.

## Add an entry

```bash
bash scripts/new-entry.sh "30 open-data networks shipped" --scope networks --public
```

Opens `$EDITOR` on a pre-filled template. Save, quit, then `git commit`.
The pre-commit hook validates frontmatter and regenerates the feeds.

## Outputs

| File | Window | Visibility |
|---|---|---|
| `feed.json` | all-time | public |
| `feed-1d.json` | last 24h | public |
| `feed-7d.json` | last 7 days | public |
| `feed-1m.json` | last 30 days | public |
| `feed-flagged.json` | flagged entries, all-time | public |
| `feed.md` | all-time | public — human readable |
| `feed-private.*` | all-time, all | gitignored, operator-only |

## Entry format

Each entry is a small frontmatter markdown file in `entries/` (public)
or `private/` (operator-only). Filename: `YYYY-MM-DD-slug.md`.

```markdown
---
date: 2026-04-25
scope: networks                    # protocol | networks | skills | infra | ops | docs
visibility: public                 # public | private
title: 30 open-data networks shipped
flagged: false                     # surface in feed-flagged.json if true
links:
  - "[[15 Open Data Networks]]"
  - https://github.com/TeoSlayer/pilotprotocol/commit/b4237e3
ids: [44-73]
---

Body — couple of paragraphs, plain English. Optional "agent context"
section that the onboarding agent ingests as a system note.
```

## Install the pre-commit hook

```bash
git config core.hooksPath .githooks
```

(One-time per clone. The hook runs `scripts/validate.sh` then
`scripts/render.sh` and stages the regenerated feeds.)

## Render manually

```bash
bash scripts/render.sh           # writes all feed.* files
bash scripts/validate.sh         # validates frontmatter, exits non-zero on error
bash scripts/test.sh             # parser + validator + render self-test
```

Both `render.py` and `validate.py` honour `PILOT_CHANGELOG_ROOT` env var
if you want to point them at a different working tree (used by the
self-test against temp roots).
