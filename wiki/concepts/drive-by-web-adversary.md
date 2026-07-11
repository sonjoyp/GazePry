---
type: concept
tags: [threat-model, adversary, core]
aliases: [Drive-by Web Adversary, Drive-by Desktop Web Adversary, Web Adversary]
sources: [information-leakage-report, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

The **drive-by web adversary** is GazePry's threat model: a first-party page or
an embedded third-party script that obtains camera access and runs
[[gaze-estimation]] client-side. This is deliberately *weaker* than the
adversaries assumed in most adjacent work (a physically present attacker filming
the victim, a VR/MR avatar feed, eyeglass reflections in a video call) — and
that weakness is the point: the commodity, consent-light, in-browser desktop
case is the gap in the literature.

## Key facts

- Capability: client-side JS only; in-browser gaze estimation; features
  computable client-side, so the adversary never needs to store the raw face.
- Structural position (Direction 1): a tracking/analytics provider whose JS SDK
  is embedded across many first-party sites — the same position as an ad or
  analytics tag ([[third-party-tracking-tag]]).
- **Out of scope (stated as such):** reading another origin's content (blocked
  by [[same-origin-policy]]), physically-present cameras, VR/MR headsets.
- Enabled by the [[enabling-conditions]]: the camera-consent gap,
  [[covert-calibration]], and third-party script embedding.

## Related

- [[gazepry]] — this model is what distinguishes the project.
- [[same-origin-policy]] — what bounds the adversary (no content peeking).
- [[gaze-re-identification]] — what the adversary *can* do across sites.

## Mentions in sources

- Report §2 (Scope and Definitions), §7 (Enabling Conditions); Protocol §2
  (Threat model).
