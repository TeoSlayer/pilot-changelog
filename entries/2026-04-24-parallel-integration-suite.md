---
date: 2026-04-24
scope: ops
visibility: public
title: 231-test parallel integration suite
flagged: false
links:
  - "[[51 Test Harness]]"
  - "[[50 Test Suite]]"
  - "[[60 Releases — v1.9.0-rc1]]"
  - "https://github.com/TeoSlayer/pilotprotocol/commit/dfbd5ff"
ids: [dfbd5ff]
---

The integration suite is now 231 tests across chaos, NAT traversal, policy,
webhook, security, tasks, resilience, duration, observability, and gateway.
`run-all.sh` runs them in parallel with NAT lanes and per-worker subnet
isolation, plus harness fixes that took the suite from "occasionally
flaky under parallel load" to consistently green.

Memory profile from the same RC: 10-min idle adds 5.8 MiB RSS / 0 fds
(budget 20 MiB / 10); 10-min load with 3,731 sends adds 23.2 MiB RSS / 0
fds (budget 100 MiB / 50). Both well inside budget.
