---
type: entity
subtype: system
tags: [prototype, analysis, python, evaluation]
aliases: [Analysis Pipeline, analysis/, reid.py, features.py, simulate.py]
sources: [readme, prototype-code]
reviewed: false
updated: 2026-07-13
---

The **analysis pipeline** (`analysis/`, repo root) is the *authoritative* offline
evaluation for the paper: Python that extracts content-independent
[[gaze-feature-extraction|features]], runs cross-task/cross-session
[[gaze-re-identification|re-ID]] under four [[reid-protocols|protocols]], and
reports [[reid-metrics|rank-1, rank-5, EER and CMC]]. Its feature definitions
mirror `reid-core.js` — the two must stay in sync.

## Key facts

- `features.py` — content-independent feature extraction (mirror of
  [[gaze-feature-extraction|reid-core.js]]); includes `resample()` to equalize
  capture cadence before extraction (the logged-vs-true-rate fix, JS↔Py
  parity-tested).
- `reid.py` — the evaluation: `python reid.py --data ../data --plot cmc.png`.
  Standardizes features, does nearest-gallery-session-per-participant matching
  (diagonal-Mahalanobis NN), computes EER by threshold sweep over
  genuine/impostor distances, optional CMC plot. Headline protocol
  `cross_task_cross_session`.
- **Data-quality guard (added 2026-07-12):** `load_sessions` drops sessions
  failing `min_samples`/`min_dur_s`/`min_valid_frac` and prints what it dropped —
  only valid sessions reach the evaluation (no silent inclusion of garbage
  captures).
- **Returning-visitor honesty:** `eligible(..., min_gap_days)` gates the
  ≥1-week cross-session cell on real elapsed time (`startedAt`); on the
  same-sitting pilot `cross_session_gap_report` correctly prints **"no eligible
  pairs"** rather than letting same-day blocks masquerade as the RQ1/RQ4 threat.
- **Confound battery (RQ0):** `shuffle_null` (label-permuted null), `rate_control`
  (rate-equalized negative control at 30 Hz, printed by default),
  `within_session_bound` (leakage upper bound), and `capture_rate_summary`
  (per-session logged rate) — the [[reid-confound-controls]] decisions, in code.
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

- [[gaze-feature-extraction]] — the shared feature set (incl. `resample`).
- [[reid-protocols]], [[reid-metrics]] — what it computes.
- [[synthetic-data-results]] — the verify-without-a-webcam numbers.
- [[reid-confound-controls]] — the shuffle-null / rate-equalized / leakage-bound
  controls this module runs.
- [[pilot-empirical-status]] — the N=2 pilot numbers this pipeline currently
  produces, and why they are not yet evidence.

## Mentions in sources

- `analysis/reid.py` (data-quality guard, `eligible`/`cross_session_gap_report`,
  `rate_control`, `shuffle_null`, `confound_battery`), `features.py` (`resample`),
  `simulate.py`, `test_analysis.py`, `requirements.txt`; plan §9, §19a;
  `README.md` (Offline evaluation, Verify without a webcam, Tests).
