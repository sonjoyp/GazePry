---
type: source
tags: [overview, entry-point, harness]
aliases: [README, Repo README, Project README]
sources: [readme]
reviewed: false
updated: 2026-07-11
---

The repository's front-door document — since the 2026-07-10 merge of
`prototype/` into the repo root it is **both** the project framing and the
harness manual (the former `prototype/README.md` content lives here now; see
[[prototype-readme]]). It states the thesis up front — [[gaze-re-identification|
cross-site gaze re-identification]] as an unclearable web tracking vector — and
documents the runnable experiment harness that implements the
[[reid-research-plan|research plan]]'s §9 apparatus.

## Key facts

- **Pluggable trackers:** the [[capture-harness]] is tracker-agnostic; one
  self-registering adapter per webcam tracker under `public/trackers/`
  ([[webgazer]] v3.5.3 vendored · [[gazecloud]] hosted/cloud · [[webeyetrack]]
  vendored/on-device · [[eyegestures]] vendored/on-device), selected per
  session from the hub picker, all emitting the same `{t, x, y}` stream — so
  one feature pipeline serves every arm (RQ3).
- **Layout (root):** `server.js` ([[reid-server]]) · `reid-core.js`
  ([[gaze-feature-extraction]]) · `public/` (harness: [[gazepry-tracker]]
  orchestrator, `trackers/`, `lib/` vendored libraries, `tasks/*.html`,
  `reid.html`) · `analysis/` ([[analysis-pipeline]]) · `test/` (regression
  suite) · `scripts/vendor-trackers.sh` · `legacy-searchgazer/` (archived
  [[searchgazer]] demo) · `data/`, `data_sim/`.
- **Quick start:** `node server.js` (or `npm start`) → `http://localhost:8080`
  (secure context needed for `getUserMedia`). Sessions POST to `data/` as
  `P01_S1_<task>_<tracker>_<ts>.json` — the filename now carries the **tracker
  family**.
- **Tests:** `npm test` runs the zero-dependency JS (`node:test`) + Python
  (`unittest`) regression suite — feature contract, adapter registry, server
  endpoints, per-tracker analysis, and a JS↔Python feature-parity test. House
  rule: run after every change.
- **Live demo** (`/reid.html`): 20 s probe & identify; wipe-state
  [[unclearability]] demo; matches only against **same-tracker** gallery
  sessions.
- **Recipes:** [[simultaneous-capture-rig|Gazepoint ground-truth rig]],
  [[cross-origin-collector|two-server cross-origin demo]], multi-tracker
  synthetic verification, and an RQ→code mapping table.
- **Caveats it states:** webcam re-ID numbers are a *lower bound*; GazeCloud
  sends video off-device (consent!); `features.py`/`reid-core.js` must stay in
  sync; `VEL_THRESHOLD` is coarse at ~30 Hz.

## Related

- [[reid-research-plan]] — the plan this harness implements (§9 "Harness
  status" points here).
- [[prototype-readme]] — the pre-merge doc this README absorbed.
- [[prototype-code]] — the source files themselves.

## Mentions in sources

- `README.md` — What's here; Quick start; Tests; Webcam trackers; Verify
  without a webcam; Gazepoint rig; Cross-origin demonstration; Mapping to the
  study protocol; Caveats; Credit & license.

## Open questions

- The README's "Research documents" links point to
  `GazePry_Direction1_ReID_Study_Protocol.md` and
  `GazePry_Information_Leakage_Report.md` at the repo root, but those files
  moved to `raw/` (2026-07-11, c0329bc) and the root now holds
  `GazePry_ReID_Research_Plan.md` instead — the links are dead and the
  "kept current" claim now belongs to the plan.
- **IRB contradiction:** the Caveats say "this project is IRB-exempt", while
  the [[reid-research-plan]] (§10, §20) treats filing the TAMU IRB protocol as
  the critical-path gate for human-subjects capture.
- **Data-hygiene contradiction:** the Caveats admit `data/` holds real
  participant session logs *tracked in the repo*; `.gitignore`'s `data/*.json`
  rule is commented out and 29 session JSONs are committed. `CLAUDE.md` and
  the original prototype policy say participant gaze data must never be
  committed. Needs a human decision (untrack? rewrite history? update policy).
