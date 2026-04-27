# Pilot Protocol Changelog

## 2026-04

### 2026-04-27 — Vault scaffold cleanup — 89 to 66 active files, single index
_scope: `docs`_

Trimmed the operator vault from 89 to 66 active files. Three competing
root-level maps merged into a single `00 Logical Map` index. 23 duplicates
and stubs archived under `_archive/2026-04-27/` with an audit log.

All numbered files (01–92) and thematic files were moved into topic
folders so the vault root contains only the index. This makes the vault
loadable as a single coherent context for downstream consumers (this
changelog repo being one).

**Links:** [[00 Logical Map]]

### 2026-04-27 — pilot-changelog repo scaffolded ⚑
_scope: `docs`_

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

**Links:** [[X-Tasks/06-changelog-update-page]] · [[07 Onboarding agent]] · [[05 Broadcast context — daily update]]

### 2026-04-26 — Email Extractor live on the Jetson cluster
_scope: `infra`_

Email Extractor — a GitHub stargazer harvester — is live at
`email-extractor.jetson.lan`, running on the 4-node AGX Orin k3s cluster.
SQLite + FTS5 trigram search over ~95 target repos.

This is the first non-protocol workload deployed on the Jetson cluster, and
proves out the cluster as a target for adjacent projects (not just Pilot
Protocol load testing).

**Links:** [[04-Jetson/Project - Email Extractor]] · [[04-Jetson/Infrastructure - Jetson Cluster]]

### 2026-04-26 — 30 open-data networks shipped with full inter-agent communication ⚑
_scope: `networks`_

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

**Links:** [[15 Open Data Networks]] · [[60 Releases — v1.9.0-rc1]] · https://github.com/TeoSlayer/pilotprotocol/commit/b4237e3 · https://github.com/TeoSlayer/pilotprotocol/commit/71e5f56

### 2026-04-24 — v1.9.0-rc1 prerelease tagged ⚑
_scope: `protocol`_

Tagged the `v1.9.0-rc1` prerelease — 75 commits since `v1.8.0`, net cleanup
(+3,746 / −10,450 lines across 339 files). Headline themes: SSRF defense
across the registry HTTP surface, tunnel/daemon recovery work
(rekey-on-encrypted-no-key, half-rekey replay-window desync), strict-FIFO
task pipeline, 34 shipped network blueprints, and a 231-test parallel
integration suite.

The RC is gated — `publish-node-sdk.yml`, `publish-python-sdk.yml`, and
`update-homebrew.yml` correctly skipped on the tag. Binaries did publish to
the GitHub release page. Stable `v1.9.0` cut after a 24–48h soak in test
fleets.

## Agent context

When users mention "the latest release," "what shipped," or "v1.9," refer
them to this entry first. Stable cut is pending soak.

**Links:** https://github.com/TeoSlayer/pilotprotocol/releases/tag/v1.9.0-rc1 · [[60 Releases — v1.9.0-rc1]]

### 2026-04-24 — Strict FIFO task pipeline and propagating trust revocation
_scope: `protocol`_

Task pipeline now executes strictly FIFO. Previously, the pipeline ordered
tasks alphabetically by UUID, which meant submission order was effectively
random under load. `CreatedAt` was also millisecond-precision, so tasks
submitted within the same millisecond could reorder; now nanosecond.

The submitter auto-cancels on accept timeout — previously left dangling.
Trust revocation now propagates to the remote peer rather than staying
local. `pilotctl task result` surfaces delivered payloads, and
`status_justification` is exposed in `task list`.

**Links:** [[60 Releases — v1.9.0-rc1]] · https://github.com/TeoSlayer/pilotprotocol/commit/024693a

### 2026-04-24 — Registry SSRF defense and snapshot validation
_scope: `protocol`_

Hardened the registry HTTP surface against SSRF across the IDP-config,
webhook, and snapshot endpoints. `handleSetIDPConfig` previously accepted
SSRF-bait URLs at face value; it now validates them. Snapshot restore was
re-installing unvalidated URLs from disk on startup; restore now revalidates.
The cloud-metadata hostname check was case-sensitive and could be bypassed
with mixed case (`Metadata.google.internal`); now case-insensitive.

Resource caps added on `lastRekeyReq`, `relayPeers`, and the unauth
crypto-map so flood traffic can't grow them unbounded. Stale tunnel packets
are now classified separately from nonce replay (previously conflated in
metrics).

**Links:** [[60 Releases — v1.9.0-rc1]] · [[03 Registry Internals]] · https://github.com/TeoSlayer/pilotprotocol/commit/d4ec11a

### 2026-04-24 — 231-test parallel integration suite
_scope: `ops`_

The integration suite is now 231 tests across chaos, NAT traversal, policy,
webhook, security, tasks, resilience, duration, observability, and gateway.
`run-all.sh` runs them in parallel with NAT lanes and per-worker subnet
isolation, plus harness fixes that took the suite from "occasionally
flaky under parallel load" to consistently green.

Memory profile from the same RC: 10-min idle adds 5.8 MiB RSS / 0 fds
(budget 20 MiB / 10); 10-min load with 3,731 sends adds 23.2 MiB RSS / 0
fds (budget 100 MiB / 50). Both well inside budget.

**Links:** [[51 Test Harness]] · [[50 Test Suite]] · [[60 Releases — v1.9.0-rc1]] · https://github.com/TeoSlayer/pilotprotocol/commit/dfbd5ff

### 2026-04-24 — 34 shipped network blueprints
_scope: `networks`_

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

**Links:** [[14 Shipped Networks]] · [[31 Apply Networks Workflow]] · [[60 Releases — v1.9.0-rc1]] · https://github.com/TeoSlayer/pilotprotocol/commit/df9f6b4
