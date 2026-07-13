---
type: concept
tags: [study-design, research-questions]
aliases: [Research Questions, RQ0, RQ1, RQ2, RQ3, RQ4, RQ5, RQs]
sources: [reid-research-plan, readme]
reviewed: false
updated: 2026-07-13
---

The research questions of the [[reid-research-plan]] (§8), and where each is
exercised in the harness ([[readme]], RQ→code mapping table). The plan now leads
with **RQ0**, a precondition that gates the rest.

## Key facts

- **RQ0 (the gate — person or apparatus?):** the [[reid-confound-controls|confound
  battery]] (calibration-swap, cross-tracker, shuffled-label null,
  rate-equalized) must pass **before** any headline number is quoted; until it
  runs on a real cohort, RQ1–RQ4 answers are pre-registered predictions, not
  findings ([[pilot-empirical-status]]). → `reid.py` `confound_battery`,
  `shuffle_null`, `rate_control`.
- **RQ1 (baseline):** same-task, cross-session re-ID (test–retest across days).
  → `reid.py` protocol `same_task_cross_session`.
- **RQ2 (the tracking threat, headline):** how much re-ID degrades
  [[cross-task-generalization|cross-task]] — enroll on site A, identify on site
  B. → `reid.py` protocols `cross_task*`.
- **RQ3 ([[ceiling-vs-commodity|ceiling vs commodity]]):** EER/rank-1 gap
  between the [[gazepoint]] IR ceiling and the commodity trackers —
  [[webgazer]], [[webeyetrack]], [[eyegestures]], plus the cloud option
  [[gazecloud]] (reported separately) — on the same subjects. →
  [[simultaneous-capture-rig]] + the pluggable adapters; `reid.py` reports per
  tracker and never matches across trackers.
- **RQ4 ([[unclearability]]):** does re-ID survive cookie/cache clear,
  incognito, new profile, new day/lighting, new device webcam, and face
  de-identification? **Now two distinct axes (plan §9):** *(a) web-state
  clearing* — the genuine unclearable point (server-side matching, nothing
  person-bound stored client-side); *(b) calibration-model clearing* — degrades
  the sensor and silently re-trains, so the deliverable is the **recovery curve**
  ("a wipe buys time, not anonymity"), not a survival claim. → `reid.html`
  separate clear actions (`intervention`/`calibQuality` metadata) +
  [[cross-origin-collector]].
- **RQ5 ([[gaze-perturbation-defense|defense]], optional):** what perturbation
  of the gaze stream defeats re-ID at acceptable utility cost? → perturb the
  stream in [[gazepry-tracker]] before submit.

## Related

- [[conditions-matrix]] — the experimental grid that answers these RQs.
- [[reid-protocols]] — the code protocols mapped to RQ1/RQ2.
- [[reid-confound-controls]] — RQ0, the gate on all the others.
- [[pilot-empirical-status]] — why RQ0 is currently unanswered (N=2 pilot).
- [[target-venues]] — where the answers are submitted.

## Mentions in sources

- Plan §8 (Research questions incl. RQ0), §9 (RQ4 two-axis split), §19a
  (RQ0 as the gate); `README.md` (Mapping to the study protocol).
