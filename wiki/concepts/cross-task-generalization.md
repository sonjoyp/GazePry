---
type: concept
tags: [re-identification, methodology, rq2, headline]
aliases: [Cross-Task Generalization, Cross-Task, Cross-Stimulus, RQ2, Task Transfer]
sources: [direction-1-study-protocol, prototype-code]
reviewed: false
updated: 2026-07-10
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
- In the [[reid-protocols|protocols]], this is `cross_task` and (with time
  separation) the `cross_task_cross_session` headline.

## Related

- [[reid-protocols]] — the four protocols that isolate this case.
- [[gaze-re-identification]] — the mechanism cross-task tests.
- [[task-suite]] — the five "sites."
- [[research-questions-rq1-rq5]] — RQ2.

## Mentions in sources

- Protocol §3 (RQ2), §6 (stimuli), §15.2 [32]; `prototype/analysis/reid.py`
  (protocol `cross_task`).
