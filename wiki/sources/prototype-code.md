---
type: source
tags: [prototype, code, implementation]
aliases: [Prototype Code, Prototype Source, prototype code]
sources: [prototype-code]
reviewed: false
updated: 2026-07-10
---

The prototype's actual source, ingested as a source in its own right (distinct
from the [[prototype-readme]] that describes it). Grounds the entity pages for
[[reid-server]], [[gaze-feature-extraction]], [[gazepry-tracker]], and the
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
  /ingest` (store session to `data/`), `GET /status` (tasks done per
  participant/session), `GET /sessions` (gallery metadata), `POST /identify`
  (live re-ID). Permissive CORS so a cross-origin task page can POST. Feature
  cache keyed by filename + mtime.
- **`public/gazepry-tracker.js`** — the "[[third-party-tracking-tag|third-party
  analytics tag]]": boots [[webgazer]] v3.5.3, runs a short click
  [[covert-calibration|calibration]], logs the raw per-frame `{t, x, y}`
  stream, POSTs the session. Same script embedded in every task page. Resolves
  vendored MediaPipe FaceMesh assets relative to the *script* (not the page),
  fixing a 404 that killed the prediction loop on task pages one level deep.
  `saveAcrossSessions` persists the regression model across page loads; a new
  session re-calibrates with `{fresh:true}` (clears the prior model).
- **`analysis/reid.py`** — the authoritative eval. Four
  [[reid-protocols|protocols]]: `all`, `same_task_cross_session`, `cross_task`,
  `cross_task_cross_session` (headline). EER computed by sweeping thresholds on
  genuine/impostor distances; CMC curve optional plot.
- **`analysis/simulate.py`** — synthetic gaze generator; subjects have stable
  oculomotor traits across tasks/sessions (pipeline verification only).

## Related

- [[prototype-readme]] — the prose description of this code.
- [[gaze-feature-extraction]] — the shared feature definition kept in sync
  between `reid-core.js` and `features.py`.
- [[reid-server]], [[gazepry-tracker]], [[analysis-pipeline]] — components.

## Mentions in sources

- `prototype/reid-core.js`; `prototype/server.js`;
  `prototype/public/gazepry-tracker.js`; `prototype/analysis/reid.py`;
  `prototype/analysis/features.py`; `prototype/analysis/simulate.py`.
