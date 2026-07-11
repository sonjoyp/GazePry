---
type: concept
tags: [study-design, research-questions]
aliases: [Research Questions, RQ1, RQ2, RQ3, RQ4, RQ5, RQs]
sources: [direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

The five research questions of [[direction-1-study-protocol|Direction 1]], and
where each is exercised in the [[prototype-readme|prototype]].

## Key facts

- **RQ1 (baseline):** same-task, cross-session re-ID (test–retest across days).
  → `reid.py` protocol `same_task_cross_session`.
- **RQ2 (the tracking threat, headline):** how much re-ID degrades
  [[cross-task-generalization|cross-task]] — enroll on site A, identify on site
  B. → `reid.py` protocols `cross_task*`.
- **RQ3 ([[ceiling-vs-commodity|ceiling vs commodity]]):** EER/rank-1 gap
  between [[gazepoint]], [[webgazer]], [[webeyetrack]] on the same subjects. →
  [[simultaneous-capture-rig]] + `tracker` field.
- **RQ4 ([[unclearability]]):** does re-ID survive cookie/cache clear,
  incognito, new profile, new day/lighting, new device webcam, and face
  de-identification? → `reid.html` wipe-state demo + [[cross-origin-collector]].
- **RQ5 ([[gaze-perturbation-defense|defense]], optional):** what perturbation
  of the gaze stream defeats re-ID at acceptable utility cost? → perturb the
  stream in [[gazepry-tracker]] before submit.

## Related

- [[conditions-matrix]] — the experimental grid that answers these RQs.
- [[reid-protocols]] — the code protocols mapped to RQ1/RQ2.
- [[target-venues]] — where the answers are submitted.

## Mentions in sources

- Protocol §3 (Research questions); `prototype/README.md` (Mapping to the study
  protocol).
