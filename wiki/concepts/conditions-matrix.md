---
type: concept
tags: [study-design, methodology, experiment]
aliases: [Conditions Matrix, Experimental Cells, Conditions]
sources: [reid-research-plan]
reviewed: false
updated: 2026-07-11
---

The **conditions matrix** is the experimental grid — each cell run across the
five [[ceiling-vs-commodity|tracker arms]] (the [[gazepoint]] IR ceiling plus
[[webgazer]], [[webeyetrack]], [[eyegestures]], and the cloud contrast
[[gazecloud]]).

## Key facts

| Axis | Levels |
|---|---|
| Task pairing | same-task / cross-task |
| Session | same-session / cross-session (≥1 wk) |
| Observation window | 5 s / 15 s / 30 s / 60 s / full |
| Gallery size | 10 / 25 / 50 / full |
| Intervention | none / cookie-cache clear / incognito / new profile / new device / face-blur |
| Features | dynamics-only / dynamics+appearance |

- **Headline cell:** cross-task, cross-session, dynamics-only, webcam — the
  real-world tracking threat.
- The Intervention axis operationalizes [[unclearability]]; the Features axis
  operationalizes [[survives-de-identification]] (dynamics-only is primary,
  dynamics+appearance is an upper bound).
- Observation-window and gallery-size axes feed the two headline
  [[reid-metrics|curves]].
- Pre-register the matrix + metrics to keep the cross-task/cross-session claim
  honest.

## Related

- [[reid-protocols]] — the task-pairing × session axes as implemented.
- [[reid-metrics]] — what each cell reports.
- [[research-questions-rq1-rq5]] — the RQs the axes answer.

## Mentions in sources

- Plan §13 (Conditions matrix), §20 (pre-register, step 5).
