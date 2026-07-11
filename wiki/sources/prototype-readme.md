---
type: source
tags: [prototype, implementation, how-to]
aliases: [Prototype README, Direction 1 Prototype, prototype/README]
sources: [prototype-readme]
reviewed: false
updated: 2026-07-10
---

Documents the working **Direction 1 prototype** — the runnable implementation
of the [[direction-1-study-protocol]]. Built on current [[webgazer]] v3.5.3
(not the dead 2016 [[searchgazer]] fork). Three pieces: a browser
[[capture-harness]], a zero-dependency Node [[reid-server]] with a live re-ID
endpoint, and a Python [[analysis-pipeline]] verifiable end-to-end on synthetic
data.

## Key facts

- **Layout:** `server.js` ([[reid-server]]), `reid-core.js`
  ([[gaze-feature-extraction|JS features + matching]]), `public/` (the
  [[capture-harness]]: [[gazepry-tracker|gazepry-tracker.js]], `task-runner.js`,
  `index.html`, `tasks/*.html`, `reid.html`), `analysis/` (the authoritative
  [[analysis-pipeline]]: `features.py`, `reid.py`, `simulate.py`).
- **Two regimes on purpose:** the prototype does *not* attempt content peeking
  ([[same-origin-policy]] blocks it); it targets [[gaze-re-identification]],
  which is content-independent and not SOP-blocked.
- **Capture flow:** enter participant ID + session, consent, run click
  [[covert-calibration|calibration]], complete five [[task-suite|tasks]]. Each
  finished task POSTs a session to `data/` as
  `P01_S1_reading_<ts>.json` — a raw stream `{t, x, y}` with `x=null` for a
  blink/lost-face gap. Server down → tracker downloads the file instead.
- **Live demo (`/reid.html`):** *Capture 20 s probe & identify* ranks enrolled
  participants by gaze-feature distance; *Wipe all browser state* clears
  cookies + localStorage + sessionStorage + the WebGazer model, then
  re-identifies — the match still lands ([[unclearability]]).
- **Offline eval:** `python reid.py --data ../data --plot cmc.png` reports
  rank-1/rank-5/EER under four [[reid-protocols|protocols]]; headline is
  `cross_task_cross_session`.
- **Verify without a webcam:** `simulate.py` generates synthetic subjects with
  stable oculomotor traits; the [[synthetic-data-results]] table is a code
  sanity check, **not** a claim about real eyes.
- **`features.py` and `reid-core.js` must stay in sync** if features change.
- **RQ mapping** and the [[simultaneous-capture-rig|Gazepoint rig]] /
  cross-origin collector recipes are given at the end of the README.

## Related

- [[direction-1-study-protocol]] — the design this implements; see the RQ→code
  mapping table.
- [[reid-server]], [[gazepry-tracker]], [[analysis-pipeline]],
  [[capture-harness]] — the entity pages for its components.

## Mentions in sources

- `prototype/README.md` — What's here; Quick start; Verify without a webcam;
  Gazepoint ground-truth rig; Cross-origin demo; Mapping to the study protocol;
  Caveats.
