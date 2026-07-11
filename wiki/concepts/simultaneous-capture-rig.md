---
type: concept
tags: [apparatus, methodology, ground-truth]
aliases: [Simultaneous Capture Rig, Gazepoint Rig, Ground-Truth Rig, Simultaneous Capture]
sources: [reid-research-plan, readme]
reviewed: false
updated: 2026-07-11
---

The **simultaneous-capture rig** records the webcam video *while*
[[gazepoint]] tracks, so every webcam frame carries an IR ground-truth gaze
label. This is the cleanest way to answer [[ceiling-vs-commodity|RQ3]]: it
yields both an **independent accuracy reference** for the webcam estimate and
matched per-subject data across both channels in one session.

> **Critical control (plan §9, hardened 2026-07-11):** the commodity webcam
> trackers must be evaluated *as an attacker deploys them* — running their own
> native self-calibration — and their gaze output must **never be retrained,
> corrected, or label-supervised using the Gazepoint signal**. IR-label
> supervision would leak the ceiling into the commodity arm and inflate both
> the RQ3 gap and the headline re-ID result. Here Gazepoint is a **measurement
> instrument, not part of the attack pipeline**. This is a sibling of the
> [[reid-confound-controls|calibration-artifact confound]].

## Key facts

1. Run Gazepoint (GP3 / GP3 HD) with its own capture, logging gaze at 60/150 Hz
   with system timestamps.
2. Run the [[capture-harness]] in the browser at the same time; the
   [[webgazer]] stream carries `t` (ms). Align the two clocks with a shared
   event (keypress or on-screen flash at task start).
3. Down-sample Gazepoint to the webcam rate (~30 Hz) for the fair-comparison
   arm — note 30 Hz limits saccade-velocity features.
4. Feed each channel's stream through the same
   [[gaze-feature-extraction|features.py]]; the `tracker` field distinguishes
   them.

## Related

- [[gazepoint]] — the IR ground-truth device.
- [[ceiling-vs-commodity]] — the RQ3 payoff this rig enables.
- [[capture-harness]] — the browser side of the simultaneous recording.
- [[reid-confound-controls]] — the IR-label-contamination control here is a
  sibling of the calibration-artifact controls.

## Mentions in sources

- Plan §9 (Apparatus — recommended rig + critical control); `README.md`
  (Gazepoint ground-truth rig).
