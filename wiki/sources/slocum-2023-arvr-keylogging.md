---
type: source
tags: [paper, attack, content-dependent, keylogging, vr, head-motion]
aliases: [Slocum et al. 2023, Going through the motions, AR/VR keylogging]
sources: [slocum-2023-arvr-keylogging]
reviewed: false
updated: 2026-07-11
---

Slocum, Zhang, Abu-Ghazaleh, Chen (UC Riverside) — *Going through the motions:
AR/VR keylogging from user head motions*, **USENIX Security 2023** —
bibliography **[15]**. Recovers text typed on a VR virtual keyboard from
**head-motion** telemetry — a content-*dependent* side channel, cited only to
delimit GazePry's scope. (`raw/Going through the motions...-2023.pdf`)

## Key facts

- Threat: AR/VR apps let users enter private text (passwords) on virtual
  keyboards; head motion while typing correlates with key positions and leaks
  the input.
- Motion-based (not gaze), VR-specific, and keyboard-layout-dependent — a
  sibling to [[wang-2024-gazeploit]] (gaze) and to the VR head/hand-motion
  identification line ([[nair-2023-vr-50k]]).
- In GazePry's framing it belongs to the content-dependent contrast class the
  re-ID thesis is explicitly *not*.

## Related

- [[wang-2024-gazeploit]] — VR keystroke inference via gaze rather than head
  motion.
- [[nair-2023-vr-50k]] — VR motion as an *identification* signal (content-
  independent), the closer analogue to GazePry's thesis.
- [[leakage-vectors-d1-d6]] — content-dependent input inference.

## Mentions in sources

- Plan §18.7 (content-dependent contrast class) [15]; protocol §15.7 [15].
