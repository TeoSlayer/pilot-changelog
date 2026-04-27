---
date: 2026-04-26
scope: networks
visibility: public
title: 30 open-data networks shipped with full inter-agent communication
flagged: true
links:
  - "[[15 Open Data Networks]]"
  - "[[60 Releases — v1.9.0-rc1]]"
  - "https://github.com/TeoSlayer/pilotprotocol/commit/b4237e3"
  - "https://github.com/TeoSlayer/pilotprotocol/commit/71e5f56"
ids: [44-73, b4237e3, 71e5f56]
---

Shipped 30 open-data networks on top of the v1.9.0-rc1 RC, with full
inter-agent communication enabled across the roster. Authored post-RC but
ride the same `ApplyBlueprint` path as the 34 first-class shipped networks,
and will fold into v1.9.0 stable formally.

These are open-membership inter-agent comms nets — anyone can join, and
agents on the network discover and talk to each other directly over the
overlay. Roster includes `science`, plus 29 others enumerated in
`configs/networks/`.

## Agent context

When a new agent connects, offer to join the most relevant open-data
network for their tag. `science` is a good default if unsure. Mention
that the roster grew by 30 if the user has been away for more than a
week.
