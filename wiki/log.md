# GazePry Wiki — Operation Log

Append-only, most-recent-last. Each entry: timestamp, operation, what changed.

---

## 2026-07-10 — INGEST (initial build)

Bootstrapped the wiki per [[SCHEMA]] from the repository's existing sources.

**Sources ingested (5):**
- `README.md` → [[readme]]
- `GazePry_Information_Leakage_Report.md` → [[information-leakage-report]]
- `GazePry_Direction1_ReID_Study_Protocol.md` → [[direction-1-study-protocol]]
- `prototype/README.md` → [[prototype-readme]]
- prototype code (`server.js`, `reid-core.js`, `gazepry-tracker.js`,
  `analysis/*.py`) → [[prototype-code]]

**Entities created (15):** [[webgazer]], [[webeyetrack]], [[gazepoint]],
[[searchgazer]], [[reid-server]], [[gazepry-tracker]], [[capture-harness]],
[[analysis-pipeline]], [[gaze-feature-extraction]], [[task-suite]], [[eyetell]],
[[gazerevealer]], [[gazebase]], [[target-venues]], [[gazepry]].

**Concepts created (27):** [[drive-by-web-adversary]], [[two-regimes-of-leakage]],
[[leakage-vectors-d1-d6]], [[gaze-re-identification]], [[person-bound-fingerprint]],
[[hardware-grounded-fingerprint]], [[same-origin-policy]], [[unclearability]],
[[survives-de-identification]], [[eye-movement-biometrics]],
[[cross-task-generalization]], [[ceiling-vs-commodity]], [[simultaneous-capture-rig]],
[[reid-protocols]], [[reid-metrics]], [[conditions-matrix]],
[[research-questions-rq1-rq5]], [[gaze-perturbation-defense]],
[[covert-calibration]], [[enabling-conditions]], [[form-factor-analysis]],
[[evidence-summary]], [[third-party-tracking-tag]], [[cross-origin-collector]],
[[gaze-estimation]], [[synthetic-data-results]], [[related-work-direction-1]].

**Infrastructure:** created `raw/` inbox; `wiki/SCHEMA.md`, `wiki/index.md`,
this log.

Page totals: 5 sources, 15 entities, 27 concepts (+ SCHEMA, index, log).

**Deduplication:** removed a stray `sources/project-readme.md` — a duplicate of
[[readme]] with dead links (`direction1-study-protocol`, `gazepry-prototype`)
that did not match the wiki's slugs.

**Open items for the next lint pass:**
- No page is `reviewed: true` yet — a human should verify claims and set the
  flag on load-bearing pages.
- Bibliography entry [38] (JuDo1000) is a reserved placeholder in the source;
  [[gazebase]] notes it as such.
