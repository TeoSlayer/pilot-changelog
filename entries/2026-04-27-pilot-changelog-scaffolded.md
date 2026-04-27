---
date: 2026-04-27
scope: docs
visibility: public
title: pilot-changelog repo scaffolded
flagged: true
links:
  - "[[X-Tasks/06-changelog-update-page]]"
  - "[[07 Onboarding agent]]"
  - "[[05 Broadcast context — daily update]]"
ids: []
---

Stood up `pilot-changelog` — the single chronological feed for "what
changed across the Pilot Protocol platform." One git repo, multiple
rendered outputs: `feed.json` (all-time public), windowed variants
`feed-1d.json` / `feed-7d.json` / `feed-1m.json`, `feed-flagged.json`
for important features, and a human-readable `feed.md`. Private mirror
outputs (`feed-private.*`) are gitignored.

Pipeline: `scripts/new-entry.sh` for authoring (same ergonomics as
`git commit -m`), `scripts/validate.sh` for frontmatter, `scripts/render.sh`
for the feeds. A `pre-commit` hook runs validate + render and stages the
generated feeds. CI re-runs validate + render and fails if generated feeds
drift from entries.

## Agent context

This is the source the onboarding agent should read on every interaction —
last 5 public entries from `feed.json`, plus everything in
`feed-flagged.json`. Don't read private entries.
