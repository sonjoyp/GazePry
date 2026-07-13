---
type: concept
tags: [related-work, literature, positioning]
aliases: [Related Work, Related Work Direction 1, The Gap, Prior Work]
sources: [reid-research-plan]
reviewed: false
updated: 2026-07-13
---

How the [[reid-research-plan]] is positioned against prior work (plan §18,
eight groups 18.1–18.8). There *is* a large adjacent literature, but **no
published work occupies the exact cell this plan targets**: commodity
in-browser webcam gaze, on a desktop, used for cross-task / cross-site
[[gaze-re-identification|re-identification]] framed as an unclearable
web-tracking vector. Every close analogue differs on at least one of {hardware,
setting, task-transfer, framing}.

## Key facts

- **Eye-movement biometrics — the signal exists** ([[eye-movement-biometrics]],
  RQ1/§7): Holland & Komogortsev [30], George & Routray [31], Deep
  Eyedentification [33], DeepEyedentificationLive [34], cross-dataset +
  template-aging [35]. Research-grade IR ceilings, not the webcam threat.
- **The cross-task problem** ([[cross-task-generalization]], RQ2): Kinnunen et
  al. [32] — the canonical task-independent authentication paper; the closest
  prior *framing*, under-studied. Two stronger data points (added to plan §21 on
  2026-07-13): **Eberz et al. 2016 [50]** ([[eberz-2016-looks-like-eve]]) is the
  **closest prior art overall** — cross-task authentication
  (reading/writing/browsing) that still works at **50 Hz** — and **Liao et al.
  2022 [51]** ([[liao-2022-wayfinding]]) shows stimulus-independent ID in
  real-world wayfinding (leave-one-route-out). Both strengthen "cross-task
  recognition exists"; neither closes the gap (see below). Plan §18.1 adds Rigas
  [52], Li [53], and the Galdi survey [54] to the foundations.
- **Longitudinal / large-N datasets** ([[gazebase]]): GazeBase [36], GazeBaseVR
  [37], JuDo1000 [38].
- **Behavioral biometrics as an unclearable, scalable identifier** (the
  [[person-bound-fingerprint]] framing): VR 50,000+ users from head/hand motion
  [39], cross-device 360° VR re-ID [40], eye-tracking-undoes-motion-privacy
  [41], XR "loss of anonymity" [42], TypeNet keystroke biometrics at 100k [43].
  Supporting analogies in other modalities, not the same setting.
- **Stateless web tracking — the "clearable cookie" baseline**: canvas
  fingerprinting [44], FP-STALKER evolving-fingerprint linkage [45],
  cross-device tracking [46]. Device-bound and resettable — the bar gaze clears.
- **Defenses** ([[gaze-perturbation-defense]], RQ5, §18.6): Steil et al.
  gaze-DP [47], Kalεido real-time gaze-DP system [48], "For Your Eyes Only"
  k-anonymity [49], plus streaming-DP and VR-gaze protections [13], [23], [24].
- **The content-dependent contrast class** (§18.7 — what the plan is *not*):
  [[eyetell|EyeTell]] [27] and GAZEploit [14] in the delta table, plus
  [[gazerevealer|GazeRevealer]] [8], gaze graphical passwords [12], AR/VR
  head-motion keylogging [15], eyeglass-reflection screen peeking [19]; the
  history side channel "I Still Know What You Visited Last Summer" [5] pairs
  with the fingerprinting baseline [44]–[46]. Privacy-framing / consent-angle
  sources: [3], [6], [9], [21], [28].

## The gap

Eye-movement biometrics is proven on **IR hardware** ([20], [30]–[37]);
behavioral-biometric tracking at **scale/cross-device** is proven in **VR**
([39], [40]); stateless web tracking is proven for **device-bound fingerprints**
([44]–[46]). No one has shown commodity webcam gaze, on the open desktop web,
re-identifying users cross-task and cross-site as an unclearable channel, and
quantified its gap to the IR ceiling on the same subjects
([[ceiling-vs-commodity]], RQ3). That intersection is the contribution.

**Rebut "just biometrics on a worse sensor" (plan Appendix A.1).** The
contribution is not a new biometric model; it is (i) the first characterization
of the *commodity webcam* channel for re-ID, (ii) the first *cross-task /
cross-site* transfer measured as a tracking threat, (iii) the first
*ceiling-vs-commodity* gap on the same subjects, and (iv) the reframing as a
stateless, [[person-bound-fingerprint|person-bound]], [[unclearability|
unclearable]] web identifier. Any one axis alone is not publishable; the stack
is. The reusable one-paragraph novelty statement lives in plan Appendix A.9.

**Handling the closest prior art — Eberz et al. 2016 [50]**
([[eberz-2016-looks-like-eve]]). A reviewer *will* cite it: cross-task, 50 Hz,
2-week stable. Pre-empt it with three distinctions the paper itself grants —
(1) it **downsamples clean 500 Hz IR** to 50 Hz, not a natively ~30 Hz noisy
self-calibrating webcam (the [[ceiling-vs-commodity]] gap); (2) it **authenticates
a cooperating, enrolled** user (1:1 defense) rather than covertly
**re-identifying** an unconsented one (1:N attack); (3) it lives on a
**workstation**, with no browser, [[same-origin-policy]], or
[[unclearability|unclearable]] cross-site framing. It establishes feasibility of
two ingredients; it does not occupy the cell.

## Related

- [[person-bound-fingerprint]], [[cross-task-generalization]],
  [[eye-movement-biometrics]], [[ceiling-vs-commodity]] — the axes the gap
  stacks.
- [[reid-research-plan]] — §18 is the full related-work discussion (the frozen
  protocol's §15 is its predecessor).

## Mentions in sources

- Plan §18 (Related work, groups 18.1–18.8), §21 (references + citation
  status); Protocol §15–§16 (frozen original).
