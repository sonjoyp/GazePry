---
type: concept
tags: [threat-model, enabling-conditions, intervention-points]
aliases: [Enabling Conditions, Camera-Consent Gap, Third-Party Embedding]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

Three conditions make [[drive-by-web-adversary|drive-by]] gaze leakage
practical. Each is also a potential intervention point (vector D6).

## Key facts

- **The camera-consent gap.** Browser camera permission is coarse and binary: a
  user who grants the camera for a legitimate purpose grants the raw video
  stream, with no separate, gaze-specific consent and no indication that
  eye-movement analysis is occurring [28].
- **[[covert-calibration]].** WebGazer-class trackers self-calibrate from
  ordinary cursor clicks, so a page builds a usable gaze model through normal
  interaction without a visible calibration step [4].
- **Third-party script embedding.** The tracker is a few lines of client-side
  JS, so it can be embedded as a [[third-party-tracking-tag]] inside a
  first-party page the user already trusts, inheriting that page's camera
  permission — the same structural problem behind earlier browsing-history side
  channels [5], now on a physically grounded signal.

## Related

- [[covert-calibration]] — condition two, its own page.
- [[third-party-tracking-tag]] — condition three, the embedding model.
- [[gaze-perturbation-defense]] — D6 interventions against these conditions.

## Mentions in sources

- Report §7 (Enabling Conditions).
