---
type: source
tags: [study-protocol, re-identification, tracking]
aliases: [Direction 1 Study Protocol, ReID Study Protocol, Study Protocol, GazePry_Direction1_ReID_Study_Protocol]
sources: [direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

The study protocol for the project's lead research direction:
**[[gaze-re-identification|cross-site gaze re-identification]] as an unclearable
web tracking vector**. It is a companion to the [[information-leakage-report]]
and is written to stand alone as a publication plan. Adds bibliography entries
**[30]–[49]** and reproduces the carried-over [1]–[29] subset.

## Key facts

- **Thesis:** eye-movement dynamics from a commodity in-browser webcam tracker
  form a *stateless, person-bound* re-ID signal that browser privacy controls
  (cookie/cache clear, incognito, storage partitioning, new device) do not
  remove, and that [[survives-de-identification|survives face removal]] because
  it is carried by movement dynamics, not appearance.
- **Why this contribution:** [[same-origin-policy]] blocks content peeking but
  not content-independent re-ID — two sites embedding the same tag link the
  same visitor by gaze. The report's limitation becomes the paper's thesis.
- **Three contributions:** (1) a new tracking channel — gaze as a cookieless,
  cache-proof, cross-device [[person-bound-fingerprint]] vs device-bound
  canvas/font fingerprints; (2) [[ceiling-vs-commodity]] — the gap between
  [[gazepoint]] IR and [[webgazer]]/[[webeyetrack]] on the *same* subjects;
  (3) optional [[gaze-perturbation-defense|defense]].
- **Research questions** [[research-questions-rq1-rq5]]: RQ1 same-task baseline,
  RQ2 cross-task tracking (headline), RQ3 ceiling vs commodity, RQ4
  [[unclearability]], RQ5 defense.
- **Apparatus:** [[simultaneous-capture-rig]] — record webcam *while*
  [[gazepoint]] tracks, giving per-frame IR ground truth. Three tracker arms:
  [[gazepoint]] (ceiling), [[webgazer]] (deployed reality), [[webeyetrack]]
  (near-future commodity ceiling).
- **Participants:** target N = 40–60; ≥2–3 sessions per participant separated
  by ≥1 week (cross-session is the real "returning visitor" test); **TAMU IRB**
  is the critical-path gate. Public datasets ([[gazebase]], GazeBaseVR,
  JuDo1000) back the large-N ceiling.
- **Stimuli:** five tasks stand in for five "sites" — [[task-suite|reading,
  SERP, images, video, form]].
- **Metrics** [[reid-metrics]]: rank-1/rank-5, CMC, EER, ROC/AUC; two headline
  curves (accuracy vs observation window, accuracy vs gallery size).
- **Venues:** primary PETS/PoPETs; reach USENIX Security / CCS / NDSS; hedge
  WPES; companion SOUPS. Rough path ≈ 6–8 months, gated by IRB + session
  separation.

## Related

- [[information-leakage-report]] — the companion survey; shares the
  bibliography and the [[drive-by-web-adversary]] model.
- [[prototype-readme]] — implements this protocol's Direction 1.
- [[conditions-matrix]], [[research-questions-rq1-rq5]], [[reid-metrics]],
  [[related-work-direction-1]] — concept pages from this protocol.

## Mentions in sources

- `GazePry_Direction1_ReID_Study_Protocol.md` §1 Thesis; §2 Threat model +
  delta table; §3 RQs; §4 Apparatus; §5 Participants; §6 Stimuli; §7
  Features/models; §8 Conditions matrix; §9 Metrics; §10 Analysis; §11 Defense;
  §12 Risks; §13 Venues; §14 Next steps; §15 Related work; §16 References.
