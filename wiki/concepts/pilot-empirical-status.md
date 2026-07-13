---
type: concept
tags: [empirical-status, pilot, caveat, evaluation, honesty]
aliases: [Pilot Empirical Status, Current Empirical Status, Read Before Quoting Any Number, N=2 Pilot, Pilot Status]
sources: [reid-research-plan, prototype-code]
reviewed: false
updated: 2026-07-13
---

The **current empirical status** of [[gazepry]] (plan **§19a**, added
2026-07-12): **no re-identification claim in the plan is yet supported by data.**
The captured pilot is a pipeline/feasibility check, not evidence — read this
before quoting any number from the harness. The gating dependency for an actual
verdict is a real collection (N ≥ 50, true ≥ 1-week separation, the
[[simultaneous-capture-rig|simultaneous Gazepoint rig]], and populated condition
metadata), with [[reid-confound-controls|RQ0]] passing first.

## Key facts

- **N = 2 real participants.** P01 and P02 on [[webgazer]] (gallery size 2 →
  chance rank-1 = 0.5); P01 alone on [[webeyetrack]] cannot be scored (1-person
  gallery). The plan's headline cells need N ≥ 50 (§10) — the pilot fills none.
- **The headline pilot number is not a result.** WebGazer
  [[cross-task-generalization|cross-task]]/cross-session **rank-1 ≈0.75**
  (chance 0.5), **EER ≈0.32**, with the **shuffled-label null at rank-1 ≈0.50** —
  a thin margin over two identities.
- **No returning-visitor separation.** All pilot "sessions" are **same-sitting**
  (P01 S1↔S2 ≈14 min; P02 S1↔S2 ≈6 min). The ≥1-week cross-session cells — the
  actual RQ1/[[unclearability|RQ4]] threat — are **empty**; `reid.py` reports
  them as such rather than letting same-day blocks masquerade as the threat.
- **A rate confound sits on top of the signal.** WebGazer logs at ~50 Hz for P01
  and ~110 Hz for P02, so capture rate is correlated with identity and part of
  the (weak) discrimination may be **cadence, not eyes**. The rate-equalized
  control must clear before any number is quoted ([[ceiling-vs-commodity]],
  [[reid-confound-controls]]).
- **RQ0 is unanswered.** The confound battery (calibration-swap, cross-tracker,
  shuffled-null, rate-equalized) is the precondition; until it runs on a real
  cohort, "is this the person or the apparatus?" is genuinely open.
- **Synthetic `data_sim/` numbers** (cross-task/cross-session rank-1 ≈0.28 at
  N=12) are a **code sanity check on generated data**, not a claim about real
  eyes ([[synthetic-data-results]]).
- **Modeling status.** Route (a) = 16 hand-crafted features + a
  diagonal-Mahalanobis nearest-neighbour matcher; the learned metric / richer
  features are deferred until N supports validating them
  ([[gaze-feature-extraction]]).
- **Bottom line:** treat H1–H4 as **pre-registered predictions to be tested**,
  not findings — with RQ0 as the gate.

## Related

- [[reid-confound-controls]] — RQ0, the gate that must pass first.
- [[synthetic-data-results]] — the synthetic sanity numbers, distinct from this
  real pilot.
- [[research-questions-rq1-rq5]] — the questions these predictions belong to.
- [[evidence-summary]] — external literature numbers (real, but not GazePry's own
  data).
- [[analysis-pipeline]] — the code that produces (and honestly caveats) these
  pilot numbers.

## Mentions in sources

- Plan **§19a** (Current empirical status — read before quoting any number),
  §10 (N target), §20 (next steps); `analysis/reid.py`
  (`cross_session_gap_report`, `rate_control`, `confound_battery`);
  `data/` (P01/P02 WebGazer session logs, git-ignored — never copied here).
