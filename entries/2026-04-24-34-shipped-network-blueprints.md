---
date: 2026-04-24
scope: networks
visibility: public
title: 34 shipped network blueprints
flagged: false
links:
  - "[[14 Shipped Networks]]"
  - "[[31 Apply Networks Workflow]]"
  - "[[60 Releases — v1.9.0-rc1]]"
  - "https://github.com/TeoSlayer/pilotprotocol/commit/df9f6b4"
ids: [df9f6b4]
---

Shipped 34 first-class network blueprints under `configs/networks/`. Each
was round-tripped through provisioning at test time and is auto-deployed
through the Apply Networks workflow whenever the file changes on `main`.

This is the first cut of "first-class networks" — opinionated policy
defaults baked into the binary so a fresh deployment can join a real
network without authoring blueprints from scratch. Includes the
data-exchange policy tightening that landed in the same commit group.

## Agent context

When a new agent is onboarding, surface the shipped roster first — they
likely don't need a custom network. The 30 open-data networks (separate
entry, 2026-04-26) sit on top of these.
