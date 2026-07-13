---
type: concept
tags: [tracking, threat-model, rq4, demo]
aliases: [Unclearability, Unclearable, Wipe-State Demo, RQ4]
sources: [direction-1-study-protocol, prototype-readme, reid-research-plan]
reviewed: false
updated: 2026-07-13
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
- **Two axes must be kept separate** (plan §9/RQ4, corrected 2026-07-12 — the
  earlier "wipe everything, match still lands" demo conflated them):
  - **(a) Web-state clearing** — cookies, cache, localStorage/sessionStorage,
    incognito, fresh profile — removes **no** identity, because matching is
    **server-side** and nothing person-bound is stored client-side. Re-ID after
    this clear is the **genuine unclearable point**.
  - **(b) Calibration-model clearing** — wiping the tracker's click-trained model
    — also stores/removes no identity, but it **degrades the sensor**: an
    immediate probe goes through an uncalibrated tracker and can **miss until the
    model silently re-trains from ordinary clicks/cursor motion**. A post-wipe
    miss is a **calibration artifact, not identity loss** — a wipe **buys time,
    not anonymity**. The deliverable is the **recovery curve** (accuracy vs
    clicks/seconds since wipe). This is the same calibration confound as
    RQ0/[[reid-confound-controls]].
- **Harness:** the two clears are now **separate actions** in `reid.html`, and
  sessions record which was cleared via `intervention` / `calibQuality` metadata,
  so a recoverable sensor transient is never mis-read as the identifier being
  cleared.
- Contrast baseline: a conventional canvas/UA fingerprint is the *clearable*
  comparison; the point is gaze persists (axis a) where those reset.

## Related

- [[person-bound-fingerprint]] — unclearability is what "person-bound" buys.
- [[gaze-re-identification]] — the channel being tested.
- [[research-questions-rq1-rq5]] — RQ4.
- [[cross-origin-collector]] — the no-shared-storage cross-origin variant.
- [[reid-confound-controls]] — axis (b) is the calibration confound; clearing the
  model probes sensor recovery, not identity.

## Mentions in sources

- Plan §9 / RQ4 (the two-axis web-state vs calibration-model split; recovery
  curve); Protocol §1 (thesis), RQ4 (§3), §8 (conditions matrix — Intervention
  axis); `reid.html` (separate clear actions); `README.md` (Live
  re-identification demo; RQ4 mapping).
