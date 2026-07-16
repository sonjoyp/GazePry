---
type: concept
tags: [mouse-cursor, tracking, gaze-proxy, permission-free, d2]
aliases: [Cursor Tracking, Mouse Tracking, Mouse-Cursor Tracking, Cursor as Gaze Proxy, Permission-Free Channel]
sources: [d2-reading-search-intent-direction]
reviewed: false
updated: 2026-07-16
---

**Cursor tracking** is the mouse-movement modality the project adds alongside
[[gaze-estimation|webcam gaze]]. Its defining property for privacy: it needs **no
camera permission and shows no indicator**, yet mouse-cursor position is a proven
**Web-scale proxy for gaze** on search-results pages. It is the permission-free
**floor** of the [[reading-search-intent-leakage|D2 direction]] (webcam gaze is the
camera-gated ceiling), and the reason the project's brief pairs *eye-tracking and
mouse-tracking*.

## Key facts

- **Cursor ≈ gaze on SERPs.** During active mouse motion the cursor sits close to
  gaze; correlation is **strongest on SERPs** (Huang, White & Buscher 2012,
  [[huang-2012-gaze-cursor-alignment]]); gaze is predictable from cursor (Guo &
  Agichtein 2010, [[guo-2010-gaze-from-cursor]]); and cursor reveals examination
  **at Web scale where eye tracking is impractical** (Huang, White & Dumais 2011,
  [[huang-2011-no-clicks-no-problem]]).
- **Features (permission-free):** per-AOI hover time and cursor dwell, cursor path
  length/curvature, cursor-to-AOI proximity over time, scroll depth/reversals, and
  **clicks** (the baseline the D2 surplus is measured over).
- **Honest bounds:** not every user moves the cursor where they look; alignment
  holds during active motion. Report the *distribution* of cursor-floor recovery;
  the gaze ceiling covers low-cursor users.
- **Distinct from [[covert-calibration]].** In the WebGazer lineage the mouse is
  merely a *calibration* input that trains the gaze regression (clicks valid ≤200
  ms). D2 promotes it to a **first-class examination channel** — a harness delta:
  log **move/hover/scroll/dwell**, not only clicks, and add a cursor-feature
  extractor beside [[gaze-feature-extraction]].
- **Public data:** the Attentive Cursor dataset ([[leiva-2020-attentive-cursor]])
  and a 2025 simultaneous mouse+eye SERP dataset
  ([[latifzadeh-2025-serp-mouse-eye]], preprint) let the floor be prototyped before
  fresh capture.
- **Non-biometric use here.** Cursor dynamics *can* be a behavioral biometric, but
  in D2 the cursor is used to recover **content/intent**, not identity — consistent
  with the "non-gaze-biometric leakage" brief.

## Related

- [[reading-search-intent-leakage]] — the direction this channel enables.
- [[covert-calibration]] — the older, calibration-only role of mouse clicks.
- [[gaze-feature-extraction]] — the gaze twin the cursor extractor sits beside.
- [[ceiling-vs-commodity]] — the floor-vs-ceiling framing D2 borrows from D4.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` §1–§4, §6, §7, §12.
