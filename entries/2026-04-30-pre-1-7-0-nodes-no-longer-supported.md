---
date: 2026-04-30
scope: protocol
visibility: public
title: Nodes below v1.7.0 no longer supported — update to v1.9.0
flagged: true
links: []
ids: []
---

An update has shipped that drops support for daemon versions below v1.7.0.
Peers running pre-1.7.0 builds will no longer be able to register,
handshake, or maintain tunnels against the current registry and beacon
fleet.

We observed a pool of approximately 14,000 nodes stuck on old pre-autoupdate
versions. These nodes predate the autoupdate mechanism introduced in v1.7.1
and will not self-heal — they require a manual update.

All peers should be running v1.9.0. The autoupdate path handles this
automatically for any node already on v1.7.1 or later. Nodes on v1.7.0
or earlier need a manual binary swap to rejoin the network.
