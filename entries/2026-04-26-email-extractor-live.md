---
date: 2026-04-26
scope: infra
visibility: public
title: Email Extractor live on the Jetson cluster
flagged: false
links:
  - "[[04-Jetson/Project - Email Extractor]]"
  - "[[04-Jetson/Infrastructure - Jetson Cluster]]"
ids: []
---

Email Extractor — a GitHub stargazer harvester — is live at
`email-extractor.jetson.lan`, running on the 4-node AGX Orin k3s cluster.
SQLite + FTS5 trigram search over ~95 target repos.

This is the first non-protocol workload deployed on the Jetson cluster, and
proves out the cluster as a target for adjacent projects (not just Pilot
Protocol load testing).
