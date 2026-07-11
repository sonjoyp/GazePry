---
type: entity
subtype: system
tags: [prototype, analysis, python, evaluation]
aliases: [Analysis Pipeline, analysis/, reid.py, features.py, simulate.py]
sources: [readme, prototype-code]
reviewed: false
updated: 2026-07-11
---

The **analysis pipeline** (`analysis/`, repo root) is the *authoritative* offline
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
- **Per-tracker reporting:** sessions carry a `tracker_family`; every protocol
  is evaluated per tracker and **never matches across trackers** — the
  per-tracker `cross_task_cross_session` EERs are the RQ3
  [[ceiling-vs-commodity]] gap. Restrict with `--tracker webgazer`.
- `simulate.py` — synthetic gaze generator: subjects with stable oculomotor
  traits across tasks/sessions, for pipeline verification without a webcam;
  `--tracker` labels runs so the multi-tracker path is testable too. Produces
  the [[synthetic-data-results]] table (a sanity check, **not** a claim about
  real eyes).
- `test_analysis.py` — stdlib-`unittest` coverage of features, protocol
  eligibility, per-tracker reporting, and the **JS↔Python parity** test
  (with `test/features-cli.js`) that forces `features.py` and `reid-core.js`
  to stay in sync.
- Requirements: `numpy` (+ `matplotlib` for `--plot`).

## Related

- [[gaze-feature-extraction]] — the shared feature set.
- [[reid-protocols]], [[reid-metrics]] — what it computes.
- [[synthetic-data-results]] — the verify-without-a-webcam numbers.

## Mentions in sources

- `analysis/reid.py`, `features.py`, `simulate.py`, `test_analysis.py`,
  `requirements.txt`; `README.md` (Offline evaluation, Verify without a
  webcam, Tests).
