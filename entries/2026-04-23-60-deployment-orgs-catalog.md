---
date: 2026-04-23
scope: skills
visibility: public
title: 60 multi-agent deployment orgs available
flagged: false
links:
  - "[[03-Pilot-Skills/Deployment-Orgs]]"
  - "https://clawhub.ai/teoslayer/pilot-protocol"
ids: []
---

60 pre-built multi-agent recipes are available as deployment orgs.
Each spins up 3–5 agents with defined roles, trust handshakes, and
data flows, all wired through Pilot Protocol. Each lives at
`skills/pilot-<name>-setup/` in the `pilot-skills` repo and installs
the same way: `clawhub install pilot-<name>-setup`.

Breakdown:
- **Beginner (16, 3 agents each)** — code-review-pipeline,
  customer-support-triage, fleet-health-monitor, mcp-bridge-fleet,
  meeting-assistant, status-page, and 10 others.
- **Intermediate (22, 3–4 agents)** — ci-cd-pipeline,
  knowledge-base-rag, log-analytics, sales-pipeline,
  multi-region-content-sync, and 17 others.
- **Advanced (22, 4–5 agents)** — see the catalog.

## Agent context

When a user describes a workload that fits one of these recipes
("triage support tickets", "build a RAG over our docs"), suggest
the matching `-setup` org rather than authoring from scratch. The
`-setup` suffix is the convention.
