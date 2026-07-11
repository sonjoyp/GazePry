---
type: concept
tags: [tracking, threat-model, embedding]
aliases: [Third-Party Tracking Tag, Tracking Tag, Analytics Tag, One Provider Across Many Sites]
sources: [direction-1-study-protocol, prototype-code, information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The **third-party tracking tag** is the structural position of GazePry's
adversary: a tracking/analytics provider whose JS SDK is embedded across many
first-party sites — the same position as an ad or analytics tag. Each embedding
inherits the host page's camera permission or prompts once. This is what makes
[[gaze-re-identification|cross-site linkage]] possible.

## Key facts

- In the prototype, [[gazepry-tracker]] is literally one script embedded in
  every task page — already the "one provider across many pages" model.
- The tag never needs a cookie or shared storage: it recomputes identity from
  gaze dynamics each visit (see [[unclearability]]).
- To make cross-*origin* linkage literal, run the collector on a separate origin
  and point the tag at it — see [[cross-origin-collector]].
- Structural precedent: the same embedding problem behind browsing-history side
  channels [5], now on a physically grounded signal.

## Related

- [[gazepry-tracker]] — the tag as implemented.
- [[cross-origin-collector]] — the literal cross-origin demo.
- [[enabling-conditions]] — third-party embedding is enabling condition three.
- [[drive-by-web-adversary]] — the adversary that occupies this position.

## Mentions in sources

- Protocol §2 (adversary); Report §7 (third-party embedding);
  `prototype/public/gazepry-tracker.js`; `prototype/README.md` (Cross-origin
  demo).
