---
type: entity
subtype: dataset
tags: [dataset, biometrics, longitudinal, public-data]
aliases: [GazeBase, GazeBaseVR, JuDo1000, Public Datasets]
sources: [direction-1-study-protocol, reid-research-plan]
reviewed: false
updated: 2026-07-11
---

Public eye-movement datasets used to back the **large-N / deep-model feasibility
ceiling** — as opposed to the *fresh simultaneous capture* that supports the
webcam threat claim. GazeBase is the reference longitudinal set.

## Key facts

- **GazeBase** [36] ([[griffith-2021-gazebase]]) — 322 subjects, 12,334
  monocular recordings, EyeLink 1000 @ 1000 Hz, 7 tasks × 2 sessions, **9
  rounds over 37 months**; the reference for test–retest
  ([[unclearability|cross-session stability]]) and the [[lohr-2022-eye-know-you-too|EKYT]] ceiling model.
- **GazeBaseVR** [37] ([[lohr-2023-gazebasevr]]) — 407 subjects, 5,020 binocular
  recordings, VR headset @ 250 Hz, up to 6 sessions over 26 months; the
  gallery-size scaling curve and VR contrast point. DOI
  **10.1038/s41597-023-02075-5** (plan §21's "…02073-7" is a typo).
- **JuDo1000** [38] — Makowski et al. 2020 (OSF, doi 10.17605/OSF.IO/5ZPVK):
  150 subjects, 4 sessions **≥1 week apart**, EyeLink Portable Duo at 1000 Hz.
  No longer a reserved placeholder — the plan cites it as the direct model for
  the cross-session, time-separated design (plan §10).
- Used for the deep-model / route (b) ceiling and large-population feasibility,
  **not** for the commodity-webcam claim.

## Related

- [[eye-movement-biometrics]] — the research-grade signal these datasets
  establish.
- [[ceiling-vs-commodity]] — public data backs the ceiling side.
- [[research-questions-rq1-rq5]] — RQ1/RQ3 feasibility.

## Mentions in sources

- Protocol §5 (Participants / public datasets), §15.3; plan §10, §17, §18.3,
  §21 [36], [37], [38].

## Open questions

- GazeBaseVR DOI discrepancy **resolved at PDF ingest**: the paper's own DOI is
  **10.1038/s41597-023-02075-5**; the plan §21 [37] value "…02073-7" is a typo.
  A human should fix it in `GazePry_ReID_Research_Plan.md` §21 (the wiki cannot
  edit sources).
