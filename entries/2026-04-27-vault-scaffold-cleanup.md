---
date: 2026-04-27
scope: docs
visibility: public
title: Vault scaffold cleanup — 89 to 66 active files, single index
flagged: false
links:
  - "[[00 Logical Map]]"
ids: []
---

Trimmed the operator vault from 89 to 66 active files. Three competing
root-level maps merged into a single `00 Logical Map` index. 23 duplicates
and stubs archived under `_archive/2026-04-27/` with an audit log.

All numbered files (01–92) and thematic files were moved into topic
folders so the vault root contains only the index. This makes the vault
loadable as a single coherent context for downstream consumers (this
changelog repo being one).
