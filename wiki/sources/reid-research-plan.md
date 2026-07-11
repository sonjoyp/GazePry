---
type: source
tags: [research-plan, threat-model, re-identification, study-design]
aliases: [ReID Research Plan, Research Plan, GazePry_ReID_Research_Plan, Cross-Site Gaze Re-Identification Research Plan]
sources: [reid-research-plan]
reviewed: false
updated: 2026-07-11
---

The consolidated blueprint for the [[gazepry]] paper: *Cross-Site Gaze
Re-Identification as an Unclearable Web Tracking Vector*
(`GazePry_ReID_Research_Plan.md`, added 2026-07-11). It **merges** the
[[information-leakage-report]] (now Part I, motivation) and the
[[direction-1-study-protocol]] (now Parts II–III, the plan proper) into one
self-contained document; both predecessors are frozen in `raw/`. This is now the
**living planning document** and holds the project's canonical bibliography
(§21, entries [1]–[49]) together with per-citation verification status.

**Reviewer-hardening pass (2026-07-11).** After the full literature ingest the
plan gained **Appendix A** (reviewer-facing novelty defense + threats to
validity) and three surgical corrections to previously shaky claims — see the
new-material summary below.

## Key facts

- **Thesis (§6):** webcam gaze dynamics are a *stateless, person-bound*
  re-identifier that survives cookie/cache clearing, incognito, device switch
  ([[unclearability]]) and face removal ([[survives-de-identification]]) —
  vector D4 of [[leakage-vectors-d1-d6]], chosen because it is the only
  content-independent vector the [[same-origin-policy]] does not neutralize.
- **Three contributions:** the new tracking channel ([[person-bound-fingerprint]]
  vs device-bound fingerprints [44]–[46]); [[ceiling-vs-commodity]] measured on
  the same subjects; an optional [[gaze-perturbation-defense]] (privacy–utility
  curve).
- **Five tracker arms (§9):** [[gazepoint]] GP3 (IR ceiling), [[webgazer]]
  (deployed reality), [[webeyetrack]] (near-future on-device ceiling),
  [[eyegestures]] (open-source second commodity arm), [[gazecloud]] (cloud
  contrast — reported separately). Considered and set aside: RealEye.io,
  TurkerGaze/[[searchgazer]], iTracker/GazeCapture, L2CS-Net.
- **Design (§10–§13):** N = 40–60; ≥2–3 sessions ≥1 week apart (mirroring
  JuDo1000 [38] and GazeBase [36]); five [[task-suite|task "sites"]]; features
  route (a) hand-crafted + classifier ([[gaze-feature-extraction]], lineage
  [31]) and route (b) end-to-end deep ceiling ([20], [33], [34]); the
  [[conditions-matrix]] headline cell is **cross-task, cross-session,
  dynamics-only, webcam**.
- **Metrics (§14, [[reid-metrics]]):** rank-1/rank-5 + CMC, EER + ROC; two key
  curves — accuracy vs **observation window** (EKYT: EER ≈0.58% at 60 s rising
  to ≈3.66% at 5 s [20] — always state the window) and accuracy vs **gallery
  size**; baseline = a *clearable* canvas/UA fingerprint [44]–[46].
- **Related-work map (§18):** eight groups, 18.1 biometrics foundations
  [30]–[35] · 18.2 task-independence [32] · 18.3 datasets [36]–[38] · 18.4
  unclearable-at-scale analogues [39]–[43] · 18.5 stateless web tracking
  [44]–[46] · 18.6 defenses [47]–[49], [13], [23], [24] · 18.7 the
  content-dependent contrast class [5], [8], [12], [14], [15], [19], [27] ·
  18.8 the gap (no prior work at the webcam × desktop × cross-site × re-ID
  intersection).
- **Venues & timeline (§19, [[target-venues]]):** PETS/PoPETs primary, USENIX
  Security/CCS/NDSS reach, WPES hedge, SOUPS companion; ≈6–8 months; aim
  **PoPETs H1 2027** or **USENIX Security 2027**.
- **Threat-model correction (§7):** the adversary is a provider's script running
  **first-party** on many sites (each with its own camera grant), linked
  **server-side** — *not* a third-party iframe silently inheriting the camera.
  Camera permission is per-top-level-origin and not shared across origins; a
  cross-origin iframe needs explicit `Permissions-Policy` delegation. See
  [[third-party-tracking-tag]], [[cross-origin-collector]].
- **RQ3 anti-contamination control (§9):** the commodity webcam trackers are
  evaluated *as deployed* (native self-calibration) and must **never** be
  trained or corrected with the Gazepoint IR labels; Gazepoint is a
  measurement instrument only. See [[simultaneous-capture-rig]],
  [[ceiling-vs-commodity]].
- **Domain-gap caveat (§12):** IR public data (250–1000 Hz) does not transfer to
  the ~30 Hz webcam channel without domain adaptation; route (a) hand-crafted
  features is the safer webcam primary, route (b) deep model for the ceiling.
- **Appendix A (new, reviewer-facing):** A.1 novelty is the *intersection*
  (rebut "just biometrics on a worse sensor"); A.3 the
  [[reid-confound-controls|confound-control battery]] (the #1 reviewer trap —
  calibration/session artifact vs person); A.4 threat-model realism
  ([[enabling-conditions|camera-consent]] proliferation, covert calibration);
  A.5 defusing "webcam too noisy" (re-ID is distributional, not pointing); A.6
  ethics/IRB/disclosure/artifact; A.7 headline + fallback ladder; A.8
  [[target-venues|venue tuning]]; A.9 reusable novelty statement.
- **Next steps gained (§20):** step 7 run the confound-control pilot **first**;
  step 8 resolve the two blockers (IRB contradiction; untrack the 29 committed
  participant gaze files before release).
- **§21 corrections (supersede earlier drafts):** George & Routray [31] is
  **EER ≈2.59%** (BioEye 2015, random-stimulus) — the earlier "≈5.8%, 320
  subjects" did not check out; EyeTell [27] ≈70% top-5 is the **Android
  lock-pattern** result, not a 6-digit-PIN result; EKYT [20] EER must always be
  quoted with its window. Preprint-flagged (numbers indicative): [16], [18],
  [23], [25], [26], [29], [35], [41]; cite the published versions of [20]
  (IEEE TIFS) and [35] (Signal Processing: Image Communication).

## Related

- [[information-leakage-report]] / [[direction-1-study-protocol]] — the two
  frozen predecessors this plan merges; their wiki pages remain the detailed
  summaries of Parts I and II respectively.
- [[readme]] — the repo front door describing the harness that implements §9
  (status paragraph in §9 points back at the repo).
- [[research-questions-rq1-rq5]], [[conditions-matrix]], [[reid-metrics]],
  [[reid-protocols]], [[related-work-direction-1]] — concept pages that now
  track this document's sections.

## Mentions in sources

- `GazePry_ReID_Research_Plan.md` — Part I §§1–5 (background), Part II §§6–17
  (plan), Part III §§18–21 (positioning, venues, next steps, references),
  **Appendix A** (novelty defense, confound controls, threat-model realism,
  ethics, headline ladder, venue tuning).

## Open questions

- **IRB contradiction:** §10/§20 call filing the TAMU IRB protocol the
  critical-path gate, but the repo `README.md` Caveats claim "this project is
  IRB-exempt". One of the two is wrong; a human should resolve which.
- GazeBaseVR DOI: §21 [37] prints 10.1038/s41597-023-**02073-7**;
  `raw/related-papers.txt` and the journal record say …-**02075-5**. Verify at
  PDF ingest.
- Al Zaidawi DOI: §21 [35] prints 10.1016/j.image.2022.**116746**;
  `raw/related-papers.txt` says …**116804**. Verify at PDF ingest.
- [12] (Tiwari & Pal, gaze-based graphical password) is cited in §3.1/§18.7 but
  has no PDF in `raw/`.
