---
type: concept
tags: [methodology, threats-to-validity, confounds, evaluation, rq]
aliases: [Confound Controls, Calibration Artifact, Threats to Validity, Reviewer Traps, ReID Confounds]
sources: [reid-research-plan]
reviewed: false
updated: 2026-07-13
---

The **confound controls** are the battery of negative controls that decide
whether a webcam re-ID match reflects the **person** or an **apparatus
artifact** — the single objection most likely to sink the paper (plan
Appendix A.3). The plan now elevates this battery to **RQ0**, the **gate every
other RQ depends on** and the pilot to run *first* (§19a, §20 step 7): until it
passes on a real cohort, H1–H4 are pre-registered predictions, not findings. A commodity webcam tracker self-calibrates per session (WebGazer
fits a ridge regression from clicks), so two sessions of one person could match
on a shared *calibration geometry, screen, or lighting* rather than on their
individual eye movements. If that is not ruled out, the "biometric" is a
measurement artifact and every downstream result is spurious. This is a
methodological contribution, not an afterthought.

## Key facts

- **Calibration-swap / never-share-calibration.** Gallery and probe sessions of
  the same person must use **independent** calibrations (the
  [[capture-harness]] already clears the model on a fresh session). Add a
  deliberate control that enrolls and probes the same person under *different*
  calibration procedures and confirms re-ID survives — isolating person from
  [[covert-calibration|calibration]] geometry.
- **Cross-tracker generalization.** Enroll on [[webgazer]], identify on
  [[eyegestures]]; if re-ID works *only* within one tracker's idiosyncratic
  output, the signal is tracker-specific, not person-specific. (Distinct from
  [[ceiling-vs-commodity|RQ3]], which reports each tracker in isolation for
  fairness.)
- **Shuffled-label null.** Re-run the whole pipeline with subject labels
  permuted; rank-1 and EER must collapse to chance ([[reid-metrics]]). The
  cheapest credibility win — report it. (Pilot: WebGazer rank-1 ≈0.75 vs a
  shuffled null ≈0.50 — a thin margin over two identities; see
  [[pilot-empirical-status]].)
- **Rate-equalized negative control (added plan §9, 2026-07-12).** Commodity
  trackers **log** at the browser `requestAnimationFrame` cadence, not the true
  ~30 Hz camera rate, and that logged rate **varies by session/participant**
  (pilot: ~50 Hz P01 vs ~110 Hz P02) — so **capture rate is a confound correlated
  with identity**. Resample every session to a common cadence
  (`features.resample` / `reid-core.js resample`) and re-run; if re-ID collapses
  once rate is equalized, the "signal" was **cadence, not eyes**. `reid.py` prints
  this control by default. This is the decisive "is it real?" test alongside the
  shuffled-label null. See [[gaze-feature-extraction]], [[ceiling-vs-commodity]].
- **Appearance ablation** ([[survives-de-identification]]): dynamics-only vs
  dynamics+appearance, so "survives face removal" is clean and the reader sees
  how much signal is movement vs looks.
- **Lighting / time / device negative controls.** At least one session under
  changed lighting/seating (and a different webcam where possible); show the
  confusion is not driven by capture conditions rather than identity.
- **Within-session leakage bound.** Split one session into enroll/probe halves
  as an *upper bound*; always report the cross-session, cross-task cell
  separately so the easy case never masquerades as the threat.

## Related

- [[gaze-feature-extraction]] — dynamics-only, screen-normalized features are
  the first line of defense against these confounds.
- [[ceiling-vs-commodity]] — the RQ3 rig must also avoid IR-label contamination
  (a sibling confound; see [[simultaneous-capture-rig]]).
- [[unclearability]] — the wipe-state demo must clear the calibration model, or
  it re-identifies model persistence, not the person.
- [[reid-research-plan]] — Appendix A.3 (the control battery), A.2 (why it is
  decisive).

- [[pilot-empirical-status]] — why RQ0 is unanswered today (N=2, rate confound
  unresolved) and what a real cohort must clear.

## Mentions in sources

- Plan Appendix A.2–A.3; §8 (RQ0 as the gate); §19a (why RQ0 is unanswered);
  §20 step 7 (run the confound-control pilot **first**); §9 (rate-equalized
  control); §12 (dynamics-only control).
