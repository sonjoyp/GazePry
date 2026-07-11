---
type: source
tags: [paper, eye-movement-biometrics, task-independent, authentication]
aliases: [Kinnunen et al. 2010, task-independent person authentication eye movement]
sources: [kinnunen-2010-task-independent]
reviewed: false
updated: 2026-07-11
---

Kinnunen, Sedlak, Bednarik (University of Eastern Finland) — *Towards
Task-Independent Person Authentication Using Eye Movement Signals*, **ETRA
2010** — bibliography **[32]**. The canonical **task-independent**
eye-movement authentication paper and the closest prior framing to GazePry's
RQ2 ([[cross-task-generalization]]): train and test on *arbitrary, unmatched*
tasks. (`raw/Towards task-independent person authentication...-2010.pdf`)

## Key facts

- Models short-term gaze-direction feature vectors with a **GMM-UBM** (Gaussian
  mixture / universal background model, the speaker-verification recipe);
  user models adapted from the UBM, scores UBM-normalized.
- Finding: there **are person-specific eye-movement features that survive
  task independence** — enrollment and verification need not share a stimulus.
  This is exactly the "enroll on site A, identify on site B" premise.
- Honest failure modes (small subject pool, high error rates) motivate the
  plan's longer observation windows and distributional features (plan §17,
  §18.2).
- The only prior work occupying the task-transfer cell — but on lab hardware,
  for *authentication*, not adversarial cross-site *tracking*.

## Related

- [[cross-task-generalization]] — RQ2, whose closest precedent this is.
- [[eye-movement-biometrics]] — the signal it authenticates on.
- [[research-questions-rq1-rq5]] — anchors RQ2's honest discussion.
- [[related-work-direction-1]] — §18.2, the differentiator group.

## Mentions in sources

- Plan §8 (RQ2 closest framing), §17 (failure-mode mitigation), §18.2 [32];
  protocol §3, §15.2.
