---
type: concept
tags: [threat-model, enabling-conditions, intervention-points]
aliases: [Enabling Conditions, Camera-Consent Gap, Third-Party Embedding]
sources: [information-leakage-report, reid-research-plan]
reviewed: false
updated: 2026-07-11
---

Three conditions make [[drive-by-web-adversary|drive-by]] gaze leakage
practical. Each is also a potential intervention point (vector D6). The camera
grant is a real *friction* the paper must confront rather than assume (plan
Appendix A.4): the argument is not that the grant is silent, but that the
contexts that legitimately request it are **proliferating**.

## Key facts

- **The camera-consent gap.** Browser camera permission is coarse and binary: a
  user who grants the camera for a legitimate purpose grants the raw video
  stream, with no separate, gaze-specific consent and no indication that
  eye-movement analysis is occurring [28]. Liebling & Preibusch [6] make the
  key point: webcam privacy loss is *obvious* to users, but **gaze extraction is
  opaque** — a consented camera feed does not signal that oculomotor *identity*
  is being harvested ([[liebling-2014-pervasive-privacy]]).
- **Why the grant is increasingly available (argue it, don't assume it).**
  Legitimate, growing contexts that already request the webcam and could host
  such a tag: accessibility gaze navigation
  ([[razuman-2025-browser-extension]]), online proctoring, attention/UX
  analytics (WebGazer's own pitch), look-to-scroll/gaze UI, WebXR, and the surge
  of gaze-conditioned AI ([[gaze-conditioned-ai]]: [9], [11], [16], [18], [26]).
  This normalization of gaze capture *is* the enabling condition.
- **[[covert-calibration]].** WebGazer-class trackers self-calibrate from
  ordinary cursor clicks ([[papoutsaki-2016-webgazer]], [4], [7]), so a page
  builds a usable gaze model through normal interaction **with no explicit
  calibration step** — capture is genuinely drive-by. Foreground this as a
  novelty point.
- **First-party script embedding.** The tracker is a few lines of client-side
  JS, embedded as a [[third-party-tracking-tag]] running **first-party** on a
  page the user already trusts, using that origin's camera grant (linkage is
  server-side; permission is *not* silently shared across origins — see the tag
  page). The same structural problem behind earlier browsing-history side
  channels ([[weinberg-2011-history-sniffing]] [5]), now on a physically
  grounded signal.

## Related

- [[covert-calibration]] — condition two, its own page.
- [[third-party-tracking-tag]] — condition three, the embedding model.
- [[gaze-perturbation-defense]] — D6 interventions against these conditions.

## Mentions in sources

- Report §7 (Enabling Conditions); plan §5, Appendix A.4 (consent realism;
  proliferating gaze-grant contexts; covert calibration as drive-by).
