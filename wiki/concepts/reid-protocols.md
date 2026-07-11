---
type: concept
tags: [evaluation, methodology, protocols]
aliases: [Re-ID Protocols, Four Protocols, cross_task_cross_session, Evaluation Protocols]
sources: [prototype-code, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

The **four evaluation protocols** in `reid.py` that separate the "easy" re-ID
case from the real tracking threat. They differ by whether the gallery may share
the probe's task and/or session.

## Key facts

| Protocol | Gallery eligibility | Meaning |
|---|---|---|
| `all` | any other session | loosest |
| `same_task_cross_session` | same content, different visit | test–retest robustness (RQ1) |
| `cross_task` | different content | the [[cross-task-generalization|generalisation]] that makes it tracking (RQ2) |
| **`cross_task_cross_session`** | different content **and** different visit | **headline** — the real-world tracking threat |

- Matching within a protocol: nearest gallery session **per participant** in
  standardized ([[gaze-feature-extraction|z-scored]]) feature space.
- Headline claim: rank-1 ≫ chance and EER well below 0.5 under
  `cross_task_cross_session` ⇒ gaze links users across content and visits.
- Maps to the study's [[conditions-matrix]] (task-pairing × session axes).

## Related

- [[reid-metrics]] — rank-1/rank-5/EER computed per protocol.
- [[cross-task-generalization]] — the axis the cross_task protocols isolate.
- [[synthetic-data-results]] — these protocols run on synthetic data.
- [[conditions-matrix]] — the full experimental grid.

## Mentions in sources

- `prototype/analysis/reid.py` (eligible, evaluate); `prototype/README.md`
  (Offline evaluation); Protocol §8.
