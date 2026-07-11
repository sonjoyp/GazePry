# GazePry Wiki — Index

An LLM-maintained knowledge base for [[gazepry]], following Karpathy's LLM-wiki
pattern. Raw sources are immutable; these pages are the compiled, cross-linked
layer over them. Conventions and workflows live in [[SCHEMA]].

**Start here:** [[gazepry]] · [[gaze-re-identification]] ·
[[reid-research-plan]] · [[readme]]

---

## Sources (`sources/`)

**Project documents & code**
- [[reid-research-plan]] — the living blueprint (motivation + study plan +
  positioning); canonical bibliography [1]–[49] in §21.
- [[readme]] — repo front door **and** harness manual: quick start, pluggable
  trackers, tests, rig/cross-origin recipes.
- [[information-leakage-report]] — threat-model survey (frozen in `raw/`; now
  Part I of the plan); two regimes, D1–D6, form factors, evidence, [1]–[29].
- [[direction-1-study-protocol]] — the Direction-1 protocol (frozen in `raw/`;
  now Parts II–III of the plan); [30]–[49].
- [[prototype-readme]] — superseded pointer (the prototype README was merged
  into the root README).
- [[prototype-code]] — the harness source (server, orchestrator + adapters,
  features, analysis, tests).

### Ingested papers (`sources/`, by role)

*Cite by the plan §21 bracket number where given; author-year otherwise
(see [[SCHEMA]]). Full digests on each page.*

**Webcam-tracker lineage & validation** — [[papoutsaki-2016-webgazer]],
[[papoutsaki-2017-searchgazer]] [4], [[papoutsaki-2018-eye-of-typer]] [7],
[[davalos-2025-webeyetrack]] [25], [[hutt-2024-mind-wandering]] [22],
[[semmelmann-2018-online-webcam-et]], [[yang-2021-webcam-behavioral]],
[[van-der-cruyssen-2024-validation]], [[kaduk-2024-webcam-vs-eyelink]],
[[thilderkvist-2024-limitations]], [[falch-2024-webcam-gaze-estimation]],
[[molina-cantero-2024-review]], [[zhu-2025-gazefollower]], [[park-2021-gazel]],
[[razuman-2025-browser-extension]], [[pygaze-site]].

**Eye-movement biometrics & datasets** —
[[holland-2011-scanpath-biometrics]] [30], [[kinnunen-2010-task-independent]]
[32], [[george-2016-score-fusion]] [31], [[jager-2019-deep-eyedentification]]
[33], [[makowski-2021-deepeyedentification-live]] [34],
[[lohr-2022-eye-know-you-too]] [20], [[al-zaidawi-2022-multi-dataset]] [35],
[[aziz-2026-gaze-offset-fusion]] [29], [[griffith-2021-gazebase]] [36],
[[lohr-2023-gazebasevr]] [37].

**Content-dependent gaze attacks** — [[chen-2018-eyetell]] [27],
[[wang-2020-gazerevealer]] [8], [[wang-2024-gazeploit]] [14],
[[slocum-2023-arvr-keylogging]] [15], [[long-2023-private-eye]] [19],
[[weinberg-2011-history-sniffing]] [5].

**VR/XR identification & anonymity** — [[nair-2023-vr-50k]] [39],
[[miller-2020-vr-identifiability]] [40],
[[aziz-2025-uncoordinated-protections]] [41],
[[patergianakis-2026-xr-anonymity]] [42].

**Gaze privacy defenses** — [[steil-2019-gaze-dp]] [47], [[li-2021-kaleido]]
[48], [[david-john-2022-for-your-eyes-only]] [49],
[[david-john-2021-streaming-privacy]] [24], [[du-2024-privategaze]] [23],
[[wilson-2024-vr-gaze-streaming]] [13].

**Stateless web tracking & keystroke biometrics** —
[[acar-2014-web-never-forgets]] [44], [[vastel-2018-fp-stalker]] [45],
[[zimmeck-2017-cross-device]] [46], [[acien-2022-typenet]] [43].

**Privacy attitudes, HCI surveys & gaze-AI** —
[[katsini-2020-gaze-security-survey]] [3], [[kroger-2020-gaze-privacy]] [21],
[[liebling-2014-pervasive-privacy]] [6], [[alsakar-2025-handheld-privacy]] [10],
[[bozkir-2025-privacy-concerns]] [28], [[abdrabou-2025-gaze-to-data]] [9],
[[bukhari-2025-privacy-indicators]] [17], [[yang-2025-gazellm]] [11],
[[pham-2026-gazeqwen]] [16], [[mathew-2026-gazevlm]] [18],
[[danry-2026-gaze-to-guidance]] [26], [[dmello-2012-gaze-tutor]] [1],
[[dmello-2012-autotutor]] [2].

## Entities (`entities/`)

**Trackers** *(five arms — see [[ceiling-vs-commodity]])*
- [[webgazer]] — commodity in-browser webcam tracker (v3.5.3); the deployed
  reality arm.
- [[webeyetrack]] — head-pose-aware in-browser tracker (~2.32 cm); near-future
  commodity ceiling.
- [[eyegestures]] — open-source on-device commodity arm (NativeSensors,
  Rust/WASM web build).
- [[gazecloud]] — hosted high-accuracy cloud contrast (GazeRecorder; frames
  leave the machine).
- [[gazepoint]] — research-grade IR tracker (GP3); the ground-truth ceiling.
- [[searchgazer]] — the deprecated 2016/2017 ancestor (dead SERP selectors;
  archived in `legacy-searchgazer/`).

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
- [[webcam-tracking-validation]] — the "accuracy objection is weakening"
  argument (webcam gaze approaching lab standards).
- [[gaze-conditioned-ai]] — gaze fed to LLMs/VLMs; why gaze collection is
  proliferating.
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
