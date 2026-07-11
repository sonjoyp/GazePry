---
type: concept
tags: [tracking, threat-model, rq4, demo]
aliases: [Unclearability, Unclearable, Wipe-State Demo, RQ4]
sources: [direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

**Unclearability** is the property that makes gaze re-ID a genuinely new
tracking channel: it survives the actions a user takes to *stop* being tracked.
It is research question **RQ4** and the point of the prototype's wipe-state demo.

## Key facts

- Survives: cookie/cache clear, incognito, a fresh browser profile, a different
  day/lighting, a **different device webcam**, and
  [[survives-de-identification|face de-identification]].
- **Why:** identity was never stored in the browser — it is carried by the
  person's [[eye-movement-biometrics|movement dynamics]], recomputed on each
  visit. There is no client-side token to clear.
- **Demo** (`reid.html`): *Wipe all browser state* clears cookies +
  localStorage + sessionStorage + the WebGazer model, then identifies again —
  the match still lands.
- Contrast baseline: a conventional canvas/UA fingerprint is the *clearable*
  comparison; the point is gaze persists where those reset.

## Related

- [[person-bound-fingerprint]] — unclearability is what "person-bound" buys.
- [[gaze-re-identification]] — the channel being tested.
- [[research-questions-rq1-rq5]] — RQ4.
- [[cross-origin-collector]] — the no-shared-storage cross-origin variant.

## Mentions in sources

- Protocol §1 (thesis), RQ4 (§3), §8 (conditions matrix — Intervention axis);
  `prototype/README.md` (Live re-identification demo; RQ4 mapping).
