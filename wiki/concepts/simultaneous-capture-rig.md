---
type: concept
tags: [apparatus, methodology, ground-truth]
aliases: [Simultaneous Capture Rig, Gazepoint Rig, Ground-Truth Rig, Simultaneous Capture]
sources: [direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

The **simultaneous-capture rig** records the webcam video *while*
[[gazepoint]] tracks, so every webcam frame carries an IR ground-truth gaze
label. This is the cleanest way to answer [[ceiling-vs-commodity|RQ3]]: it
yields both clean labels to train/validate the webcam estimate and matched
per-subject data across both channels in one session.

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

## Mentions in sources

- Protocol §4 (Apparatus — recommended rig); `prototype/README.md` (Gazepoint
  ground-truth rig).
