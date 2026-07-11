---
type: entity
subtype: tool
tags: [eye-tracking, hardware, ground-truth, infrared]
aliases: [Gazepoint, Gazepoint GP3, GP3 HD, Gazepoint rig]
sources: [direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

**Gazepoint** (GP3 / GP3 HD) is the research-grade infrared eye tracker used as
the **ground-truth ceiling** in the [[ceiling-vs-commodity]] comparison. Its IR
gaze gives a per-frame label for every webcam frame in the
[[simultaneous-capture-rig]], which is how the protocol answers RQ3 (the gap
between research hardware and the webcam channel on the *same* subjects).

## Key facts

- Sampling rate 60 / 150 Hz IR — well above the ≈30 Hz webcam rate.
- Down-sampled to the webcam rate for the *fair-comparison* arm; note that
  30 Hz limits saccade-velocity features (report which features survive).
- Clock alignment with the browser stream via a shared event (keypress or
  on-screen flash at task start).
- Distinguished from webcam channels in analysis by the `tracker` field.

## Related

- [[simultaneous-capture-rig]] — how Gazepoint and webcam are recorded together.
- [[webgazer]], [[webeyetrack]] — the commodity arms it sets the ceiling for.
- [[ceiling-vs-commodity]] — RQ3.

## Mentions in sources

- Protocol §4 (apparatus), §8 (tracker arms); `prototype/README.md` (Gazepoint
  ground-truth rig).
