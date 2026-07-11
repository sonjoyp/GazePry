---
type: source
tags: [paper, defense, differential-privacy, gaze, foundations]
aliases: [Steil et al. 2019, Privacy-aware eye tracking differential privacy]
sources: [steil-2019-gaze-dp]
reviewed: false
updated: 2026-07-11
---

Steil, Hagestedt, Huang, Bulling (MPI / CISPA / Stuttgart) — *Privacy-Aware Eye
Tracking Using Differential Privacy*, **ETRA 2019** — bibliography **[47]**.
The **foundational feature-level differential-privacy-for-gaze** paper — the
natural first perturbation for GazePry's RQ5 [[gaze-perturbation-defense]].
(`raw/Privacy-aware eye tracking using differential privacy...-2019.pdf`)

## Key facts

- Applies **differential privacy to eye-movement feature data** so that
  privacy-sensitive attributes cannot be recovered while gaze utility is
  retained; motivated by eye tracking being integrated into VR/AR.
- The reference "feature-level gaze-DP" point in the plan's defense landscape;
  a mechanism to benchmark GazePry's in-browser perturbation against.

## Related

- [[gaze-perturbation-defense]] — RQ5; the first perturbation to evaluate.
- [[li-2021-kaleido]] — the real-time gaze-DP *system* successor.
- [[david-john-2022-for-your-eyes-only]] — re-ID-targeted defense.

## Mentions in sources

- Plan §16 (defense, feature-level DP), §18.6 [47]; protocol §11, §15.6 [47];
  report §4 (D6).
