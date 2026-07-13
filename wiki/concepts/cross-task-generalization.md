---
type: concept
tags: [re-identification, methodology, rq2, headline]
aliases: [Cross-Task Generalization, Cross-Task, Cross-Stimulus, RQ2, Task Transfer]
sources: [direction-1-study-protocol, prototype-code]
reviewed: false
updated: 2026-07-13
---

**Cross-task generalization** is the differentiator of Direction 1: enroll a
user on site A's content and identify them on site B's *different* content.
Most eye-movement biometrics papers enroll and test on the *same* task; the
tracking threat needs task/stimulus transfer. It is research question **RQ2**
and the headline result.

## Key facts

- Different tasks elicit different gaze dynamics, so the five
  [[task-suite|tasks]] stand in for five different "sites."
- Same-task matching is an upper bound; cross-task is "the generalisation that
  makes it *tracking*."
- Prior framing: Kinnunen et al. [32] — the canonical *task-independent*
  eye-movement authentication paper (no shared train/test stimulus); anchors the
  cross-task discussion, including its honest failure modes (high FRR on 9
  subjects) that motivate longer windows + distributional features.
- **External evidence cross-task works** (added to plan §21 on 2026-07-13):
  **Eberz et al. 2016 [50]** ([[eberz-2016-looks-like-eve]]) authenticates across
  **reading, writing, and browsing** with error comparable to a fixed task set —
  the closest prior art to this RQ. **Liao et al. 2022 [51]**
  ([[liao-2022-wayfinding]]) achieves stimulus-independent ID in real-world
  wayfinding, with **leave-one-route-out** (64%, EER 12.1%) as a direct analogue
  of enroll-on-A / identify-on-B. Caveat: both are cooperative IR/mobile trackers
  at ≥50–60 Hz, not covert ~30 Hz webcam re-ID — the transfer is shown, the
  *commodity-webcam* transfer is still GazePry's to demonstrate.
- In the [[reid-protocols|protocols]], this is `cross_task` and (with time
  separation) the `cross_task_cross_session` headline.

## Related

- [[reid-protocols]] — the four protocols that isolate this case.
- [[gaze-re-identification]] — the mechanism cross-task tests.
- [[task-suite]] — the five "sites."
- [[research-questions-rq1-rq5]] — RQ2.
- [[eberz-2016-looks-like-eve]], [[liao-2022-wayfinding]] — external evidence that
  cross-task / stimulus-independent recognition is achievable.

## Mentions in sources

- Protocol §3 (RQ2), §6 (stimuli), §15.2 [32]; `prototype/analysis/reid.py`
  (protocol `cross_task`).
