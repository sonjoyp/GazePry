---
type: concept
tags: [tracking, threat-model, embedding]
aliases: [Third-Party Tracking Tag, Tracking Tag, Analytics Tag, One Provider Across Many Sites]
sources: [reid-research-plan, prototype-code, information-leakage-report]
reviewed: false
updated: 2026-07-11
---

The **third-party tracking tag** is the structural position of GazePry's
adversary: a tracking/analytics provider whose JavaScript is embedded across
many sites — the same position as an ad or analytics tag. This is what makes
[[gaze-re-identification|cross-site linkage]] possible.

## Key facts

- **Correct web-platform mechanism (plan §7, hardened 2026-07-11):** the
  provider's script runs **first-party** — included via `<script src>` and
  executing in each host site's *own* origin — so it uses *that site's* camera
  permission, and the provider links visitors **server-side** across every site
  it appears on. Camera permission is granted **per top-level origin and is not
  silently shared across origins**: a cross-origin tracker *iframe* would need
  explicit `Permissions-Policy` camera delegation from each top frame plus its
  own per-origin grant. So the realistic (and still-alarming) model is the
  first-party-included script, **not** a third-party iframe silently inheriting
  the camera. State this precisely — a security reviewer checks it.
- In the harness, [[gazepry-tracker]] is literally one script embedded in every
  task page — already the "one provider across many pages" model.
- The tag never needs a cookie or shared storage: it recomputes identity from
  gaze dynamics each visit (see [[unclearability]]).
- To make cross-*origin* linkage literal, run the collector on a separate origin
  and point the tag at it — see [[cross-origin-collector]].
- Structural precedent: the same embedding problem behind browsing-history side
  channels ([[weinberg-2011-history-sniffing]] [5]), now on a physically
  grounded signal.

## Related

- [[gazepry-tracker]] — the tag as implemented.
- [[cross-origin-collector]] — the literal cross-origin demo.
- [[enabling-conditions]] — third-party embedding is enabling condition three.
- [[drive-by-web-adversary]] — the adversary that occupies this position.

## Mentions in sources

- Plan §7 (adversary + corrected permission mechanism), Appendix A.4; Report §7
  (third-party embedding); `public/gazepry-tracker.js`; `README.md`
  (Cross-origin demonstration).
