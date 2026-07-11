---
type: source
tags: [paper, eye-movement-biometrics, score-fusion, gaze-offset, preprint]
aliases: [Aziz et al. 2026, Continuous Gaze Offset Score Fusion, Enhancing Eye Movement Biometrics]
sources: [aziz-2026-gaze-offset-fusion]
reviewed: false
updated: 2026-07-11
---

Aziz, Raju, Komogortsev (Texas State) — *Enhancing Eye Movement Biometrics for
User Authentication via Continuous Gaze Offset Score Fusion*, arXiv:2605.06810,
2026 — bibliography **[29]** (**preprint-flagged** in plan §21). Adds
**continuous gaze offset** as an auxiliary biometric feature fused with existing
EMB systems — of interest to GazePry because it explicitly helps under
*degraded/noisy* eye tracking (i.e. the webcam regime). (`raw/Enhancing Eye
Movement Biometrics...-2026.pdf`)

## Key facts

- Fuses continuous gaze-offset information with deep-EMB features via linear and
  nonlinear score fusion; **nonlinear fusion** gives the larger benefit.
- Evaluated on two public datasets (a lab-grade tracker and a **VR headset**),
  across multiple tasks and observation durations.
- **Multi-task fusion** further improves authentication — supports GazePry's
  cross-task enrollment intuition ([[cross-task-generalization]]).
- Key relevance: gaze offset is "useful auxiliary information under degraded or
  noisy eye tracking" — precisely the commodity-webcam condition where the plan
  expects EER to be a lower bound ([[ceiling-vs-commodity]]).

## Related

- [[eye-movement-biometrics]] — an incremental score-fusion enhancement.
- [[george-2016-score-fusion]] — the score-fusion lineage.
- [[cross-task-generalization]] — multi-task fusion evidence.

## Mentions in sources

- Plan §18.1/§18.2, §21 (preprint flag; re-check before submission) [29];
  report §6 [29].
