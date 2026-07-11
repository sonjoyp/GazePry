---
type: source
tags: [prototype, code, implementation]
aliases: [Prototype Code, Prototype Source, prototype code, Harness Code]
sources: [prototype-code]
reviewed: false
updated: 2026-07-11
---

The harness's actual source, ingested as a source in its own right (distinct
from the [[readme]] that describes it). Since the 2026-07-10 merge it lives at
the **repo root**. Grounds the entity pages for [[reid-server]],
[[gaze-feature-extraction]], [[gazepry-tracker]], the tracker adapters, and the
[[analysis-pipeline]] in the code as written.

## Key facts

- **`reid-core.js`** — content-independent [[gaze-feature-extraction]] + NN
  matching for the live demo; a faithful JS port of `analysis/features.py`.
  16 features in `FEATURE_NAMES` (fixation-duration mean/median/std/p90,
  saccade-amplitude mean/median/std/p90, saccade-velocity mean/median/p90,
  fix_rate, sacc_rate, fix_ratio, gap_rate, main_seq_slope). I-VT split with
  `VEL_THRESHOLD = 2.0` (screen-diagonal units/sec), `MIN_FIX_MS = 80`. Spatial
  features normalized by screen diagonal → resolution/device independent.
  Matching: column-wise standardize, Euclidean distance, nearest gallery
  session per participant.
- **`server.js`** — [[reid-server]], zero dependencies. Endpoints: `POST
  /ingest` (store session to `data/`; filename carries the tracker family),
  `GET /status`, `GET /sessions`, `POST /identify` (live re-ID, **never mixes
  trackers**). Permissive CORS so a cross-origin task page can POST. Feature
  cache keyed by filename + mtime; static serving path-jailed to `public/`.
- **`public/gazepry-tracker.js`** — the tracker-**agnostic** orchestrator (see
  [[gazepry-tracker]]): identity, calibration overlay, capture, watchdog,
  submission; drives whichever `public/trackers/*.js` adapter matches the
  selected tracker. Adapters self-register via `GazePry.registerTracker`
  (contract in `public/trackers/README-adapter.md`; minimum: `family`,
  `start`, `onGaze` emitting `{x, y}` viewport pixels; `null` = blink/lost
  face).
- **`public/trackers/`** — [[webgazer]].js, [[gazecloud]].js,
  [[webeyetrack]].js, [[eyegestures]].js; vendored libraries under
  `public/lib/` (fetched by `scripts/vendor-trackers.sh`; WebEyeTrack's
  BlazeGaze model served from `public/web/` because its loader hardcodes
  `${origin}/web/model.json`).
- **`analysis/reid.py`** — the authoritative eval. Four
  [[reid-protocols|protocols]]: `all`, `same_task_cross_session`, `cross_task`,
  `cross_task_cross_session` (headline). EER by threshold sweep on
  genuine/impostor distances; CMC plot optional; reports **per tracker** and
  never matches across trackers (`--tracker` to restrict).
- **`analysis/simulate.py`** — synthetic gaze generator (stable per-subject
  oculomotor traits; `--tracker` label for multi-tracker verification);
  pipeline check only.
- **`test/` + `analysis/test_analysis.py`** — zero-dependency regression
  suite (`npm test`): feature contract, segmentation, standardize/identify
  edge cases; adapter registry + capability flags + vendored-library presence;
  server ingest/status/sessions/identify incl. path-traversal guard and
  legacy-filename family inference; Python features, protocol eligibility,
  per-tracker reporting; JS↔Python parity via `test/features-cli.js`.

## Related

- [[readme]] — the prose description of this code.
- [[gaze-feature-extraction]] — the shared feature definition kept in sync
  between `reid-core.js` and `features.py` (enforced by the parity test).
- [[reid-server]], [[gazepry-tracker]], [[analysis-pipeline]],
  [[capture-harness]] — components.

## Mentions in sources

- `reid-core.js`; `server.js`; `public/gazepry-tracker.js`;
  `public/trackers/*.js`; `public/trackers/README-adapter.md`;
  `analysis/reid.py`, `features.py`, `simulate.py`, `test_analysis.py`;
  `test/*.js`; `scripts/vendor-trackers.sh`.
