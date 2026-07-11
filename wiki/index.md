# GazePry Wiki — Index

An LLM-maintained knowledge base for [[gazepry]], following Karpathy's LLM-wiki
pattern. Raw sources are immutable; these pages are the compiled, cross-linked
layer over them. Conventions and workflows live in [[SCHEMA]].

**Start here:** [[gazepry]] · [[gaze-re-identification]] ·
[[direction-1-study-protocol]] · [[information-leakage-report]]

---

## Sources (`sources/`)

- [[readme]] — repo front door: project framing, quick start, license.
- [[information-leakage-report]] — threat-model survey; the two regimes, D1–D6,
  form factors, evidence, bibliography [1]–[29].
- [[direction-1-study-protocol]] — the lead research plan: cross-site gaze
  re-ID as an unclearable tracking vector; adds [30]–[49].
- [[prototype-readme]] — how to run the Direction 1 prototype.
- [[prototype-code]] — the prototype's actual source (server, tracker,
  features, analysis).

## Entities (`entities/`)

**Trackers**
- [[webgazer]] — commodity in-browser webcam tracker (v3.5.3); the deployed
  reality arm.
- [[webeyetrack]] — head-pose-aware in-browser tracker (~2.32 cm); near-future
  commodity ceiling.
- [[gazepoint]] — research-grade IR tracker (GP3); the ground-truth ceiling.
- [[searchgazer]] — the deprecated 2016/2017 ancestor (dead SERP selectors).

**Prototype components**
- [[reid-server]] — zero-dependency Node collection + live re-ID server.
- [[gazepry-tracker]] — the client-side "third-party analytics tag."
- [[capture-harness]] — the browser front-end (hub + five task pages + demo).
- [[analysis-pipeline]] — the authoritative Python evaluation.
- [[gaze-feature-extraction]] — the 16-feature content-independent vector
  (reid-core.js / features.py).
- [[task-suite]] — the five task "sites" (reading, SERP, images, video, form).

**Attacks & data**
- [[eyetell]] — mobile keystroke inference from eye video (content-dependent).
- [[gazerevealer]] — smartphone password inference from the front camera.
- [[gazebase]] — public longitudinal datasets (GazeBase / GazeBaseVR /
  JuDo1000).

**Publishing**
- [[target-venues]] — PETS/PoPETs, USENIX Security, SOUPS; timeline.

## Concepts (`concepts/`)

**Threat model & framing**
- [[drive-by-web-adversary]] — the weak-but-realistic in-browser adversary.
- [[two-regimes-of-leakage]] — content-dependent vs content-independent.
- [[leakage-vectors-d1-d6]] — the six vectors, mapped to the two regimes.
- [[same-origin-policy]] — why the cross-site threat is re-ID, not peeking.
- [[hardware-grounded-fingerprint]] — why gaze bypasses script-layer defenses.
- [[enabling-conditions]] — camera-consent gap, covert calibration, embedding.
- [[form-factor-analysis]] — laptop/desktop vs smartphone vs tablet.
- [[evidence-summary]] — the consolidated quantitative findings table.

**The re-ID thesis (Direction 1)**
- [[gaze-re-identification]] — linking visitors by gaze dynamics (vector D4).
- [[person-bound-fingerprint]] — gaze as a person-bound, cross-device identifier.
- [[unclearability]] — survives cookie clear, incognito, new device (RQ4).
- [[survives-de-identification]] — survives face removal; dynamics not appearance.
- [[cross-task-generalization]] — enroll on site A, identify on site B (RQ2).
- [[eye-movement-biometrics]] — the research-grade signal being weaponized.
- [[covert-calibration]] — building a gaze model from ordinary clicks.
- [[third-party-tracking-tag]] — one provider embedded across many sites.
- [[gaze-estimation]] — webcam-only "where are you looking" software.

**Method, evaluation & defense**
- [[research-questions-rq1-rq5]] — the five RQs and where each is exercised.
- [[ceiling-vs-commodity]] — the IR-vs-webcam gap on the same subjects (RQ3).
- [[simultaneous-capture-rig]] — webcam + Gazepoint recorded together.
- [[conditions-matrix]] — the full experimental grid.
- [[reid-protocols]] — the four evaluation protocols (headline
  cross_task_cross_session).
- [[reid-metrics]] — rank-1/rank-5, CMC, EER, ROC; the two headline curves.
- [[synthetic-data-results]] — verify-without-a-webcam sanity numbers.
- [[cross-origin-collector]] — the literal cross-origin linkage demo.
- [[gaze-perturbation-defense]] — the optional RQ5 defense.
- [[related-work-direction-1]] — positioning and the gap being filled.

---

*Maintenance: see [[log]] for the operation history and [[SCHEMA]] for the
ingest / query / lint workflows.*
