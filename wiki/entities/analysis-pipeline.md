---
type: entity
subtype: system
tags: [prototype, analysis, python, evaluation]
aliases: [Analysis Pipeline, analysis/, reid.py, features.py, simulate.py]
sources: [prototype-readme, prototype-code]
reviewed: false
updated: 2026-07-10
---

The **analysis pipeline** (`prototype/analysis/`) is the *authoritative* offline
evaluation for the paper: Python that extracts content-independent
[[gaze-feature-extraction|features]], runs cross-task/cross-session
[[gaze-re-identification|re-ID]] under four [[reid-protocols|protocols]], and
reports [[reid-metrics|rank-1, rank-5, EER and CMC]]. Its feature definitions
mirror `reid-core.js` — the two must stay in sync.

## Key facts

- `features.py` — content-independent feature extraction (mirror of
  [[gaze-feature-extraction|reid-core.js]]).
- `reid.py` — the evaluation: `python reid.py --data ../data --plot cmc.png`.
  Standardizes features, does nearest-gallery-session-per-participant matching,
  computes EER by threshold sweep over genuine/impostor distances, optional CMC
  plot. Headline protocol `cross_task_cross_session`.
- `simulate.py` — synthetic gaze generator: subjects with stable oculomotor
  traits across tasks/sessions, for pipeline verification without a webcam.
  Produces the [[synthetic-data-results]] table (a sanity check, **not** a
  claim about real eyes).
- Requirements: `numpy` (+ `matplotlib` for `--plot`).

## Related

- [[gaze-feature-extraction]] — the shared feature set.
- [[reid-protocols]], [[reid-metrics]] — what it computes.
- [[synthetic-data-results]] — the verify-without-a-webcam numbers.

## Mentions in sources

- `prototype/analysis/reid.py`, `features.py`, `simulate.py`,
  `requirements.txt`; `prototype/README.md` (Offline evaluation, Verify without
  a webcam).
