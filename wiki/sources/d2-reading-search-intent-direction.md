---
type: source
tags: [project-document, d2, reading, search-intent, mouse-tracking, direction]
aliases: [D2 Direction, Reading Search Intent Direction, D2 Plan, No Clicks No Privacy]
sources: [d2-reading-search-intent-direction]
reviewed: false
updated: 2026-07-16
---

`GazePry_D2_Reading_Search_Intent_Direction.md` — the **D2** direction blueprint
(*"No Clicks, No Privacy"*): reconstructing a visitor's **latent reading and
search intent** from commodity webcam gaze **and permission-free mouse-cursor
tracking**, framed as a first-party privacy attack. Companion to the D4
[[reid-research-plan]]; D2 leaks *what you are doing/thinking about*
([[reading-search-intent-leakage]]), D4 leaks *who you are*
([[gaze-re-identification]]). This is the concept vector D2 in
[[leakage-vectors-d1-d6]], now developed into a full plan. The mouse channel is
the new [[cursor-tracking]] modality the project adds.

## Key facts

- **Thesis:** a first-party analytics/search tag reconstructs *considered-but-
  unclicked*, *re-read*, and *zero-click/good-abandonment* interest at coarse-AOI
  granularity — the **examination layer**, previously private because it left no
  click trail. Contribution = reframing "cursor/gaze as an implicit-feedback tool
  for ranking" as an **attack**, and quantifying the **surveillance surplus** of
  the examination channel over the click/query baseline.
- **Eye + mouse fusion.** Separates a **permission-free cursor floor** (no camera
  grant, no indicator — Guo & Agichtein 2010, Huang/White/Dumais 2011,
  Huang/White/Buscher 2012) from a **camera-gated gaze ceiling** — the D2 analogue
  of [[ceiling-vs-commodity]]. Satisfies the brief: leaked payload is
  content/intent, **non-biometric**.
- **Confronts the same-origin objection head-on:** D2 is content-dependent, so
  cross-site content peeking stays blocked ([[same-origin-policy]]). The threat is
  **first-party / within-site**, needs no SOP defeat, and is alarming via
  zero-click intent + the permission-free cursor. Does **not** claim cross-site
  reading.
- **Confronts webcam coarseness** (Thilderkvist [45]): scoped to coarse AOIs (SERP
  rows, paragraphs, topics), which is where the sensitive inference lives.
- **RQs:** RQ0 (beat a saliency/position prior — the gate), RQ1 (per-channel
  examination recovery), RQ2 (latent-intent surplus — headline), RQ3 (cursor floor
  vs gaze ceiling), RQ4 (topic/sensitivity), RQ5 (defense).
- **Harness delta:** promote mouse **move/hover/scroll/dwell** to a first-class
  recorded stream (today only calibration clicks are logged) + a cursor-feature
  extractor beside [[gaze-feature-extraction]] + IR-fixation-on-AOI ground truth.
- **New bibliography** (groups G/B/A/Q/R in the doc §11) fills the mouse/
  search-behavior gap the project bibliography lacked — see [[cursor-tracking]] and
  the source pages below. These are **doc-local labels**, not the shared plan §21
  numbering; wiki cites them **author-year** until merged into §21 (doc §12 next
  step).
- **Venues:** PETS/PoPETs primary (Gervais 2014 CCS precedent for search privacy),
  SOUPS companion (consent/awareness gap), CHIIR/WWW/SIGIR adjacent.
- **Status:** proposal only — no D2 empirical result yet; all H0–H5 are
  pre-registered predictions with RQ0 as the gate ([[pilot-empirical-status]]).

## Related

- [[reading-search-intent-leakage]] — the concept page for this direction.
- [[cursor-tracking]] — the permission-free mouse channel it introduces.
- [[reid-research-plan]] — the D4 companion; shares the harness, the
  [[simultaneous-capture-rig]], and the confound discipline; the two **compose**.
- [[papoutsaki-2017-searchgazer]] / [[searchgazer]] — the SERP AOI lineage this
  weaponizes; [[task-suite]] — the SERP task is the headline surface.
- [[thilderkvist-2024-limitations]] — the coarse-granularity bound.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` (repo root), all sections.
