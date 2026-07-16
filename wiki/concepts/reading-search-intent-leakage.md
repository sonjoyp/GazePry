---
type: concept
tags: [d2, reading, search-intent, content-dependent, leakage, direction, core]
aliases: [D2, Reading Search Intent Leakage, Reading and Search Intent, No Clicks No Privacy, Examination Surveillance, Surveillance Surplus, Zero-Click Intent]
sources: [d2-reading-search-intent-direction, information-leakage-report]
reviewed: false
updated: 2026-07-16
---

**Reading & search-intent leakage** is vector **D2** in the
[[leakage-vectors-d1-d6]], developed into a full direction by
[[d2-reading-search-intent-direction]] (*"No Clicks, No Privacy"*). A first-party
analytics/search tag reconstructs a visitor's **latent information interest** — the
results, products, and passages they *considered, re-read, or answered their need
from without clicking or typing* — from commodity webcam [[gaze-estimation|gaze]]
fused with permission-free [[cursor-tracking|mouse-cursor tracking]]. It is
[[two-regimes-of-leakage|content-dependent]] (so it does **not**
[[same-origin-policy|survive SOP]] cross-site) but first-party and within-site.
The leaked payload is **content/intent, not a biometric** — the counterpart to
[[gaze-re-identification|D4]] (*who you are*); the two **compose**.

## Key facts

- **The reframe:** turns a decade of "cursor/gaze as an implicit-feedback *tool*
  for ranking" (Guo & Agichtein 2010, Huang/White/Dumais 2011
  [[huang-2011-no-clicks-no-problem]], Huang/White/Buscher 2012
  [[huang-2012-gaze-cursor-alignment]], Buscher [[buscher-2012-attentive-documents]])
  into a **privacy attack**, and quantifies the **surveillance surplus** of the
  examination channel over the click/query baseline.
- **Permission-free floor vs camera ceiling** — the D2 analogue of
  [[ceiling-vs-commodity]]: the cursor leaks a coarse version of examination with
  **no camera grant and no indicator**; webcam gaze is the finer, permission-gated
  ceiling. RQ3 measures the gap on the same users/pages.
- **Zero-click / considered-but-unclicked** intent is the headline (RQ2): the
  clickstream *by construction* cannot contain it (Li 2009
  [[li-2009-good-abandonment]], Williams 2016 [[williams-2016-good-abandonment]]),
  but gaze/cursor recover it.
- **Extends query-log privacy** ([[jones-2007-query-log-privacy]],
  [[gervais-2014-web-search-privacy]]) from queries+clicks to the **examination
  layer** — strictly more revealing.
- **Scoped honestly:** does not claim cross-site content peeking (blocked by
  [[same-origin-policy]]); operates at **coarse AOI granularity** (SERP rows,
  paragraphs, topics), because webcam gaze cannot resolve fine AOIs
  ([[thilderkvist-2024-limitations]] [45]) — which is exactly where the sensitive
  inference lives.
- **RQ0 is the gate:** the attack must beat a **saliency/position prior** (everyone
  looks at the top result / first paragraph — [[rayner-1998-reading-eye-movements]])
  and collapse under a shuffled-label null — the D2 analogue of
  [[reid-confound-controls]].
- **Headline surface:** SERP scanning ([[task-suite]] SERP task, the
  [[searchgazer]] AOI lineage), where cursor–gaze alignment is strongest
  [[huang-2012-gaze-cursor-alignment]]; reading passages are the second surface.
- **Features are AOI-/content-anchored**, unlike D4's content-*independent*
  [[gaze-feature-extraction|16-D dynamics]] — a different pipeline, plus a new
  cursor-feature extractor ([[cursor-tracking]]).
- **Status:** proposal only — no D2 result yet; H0–H5 are pre-registered
  predictions ([[pilot-empirical-status]]).

## Related

- [[cursor-tracking]] — the permission-free modality that makes the floor.
- [[gaze-re-identification]] — the D4 sibling; D2 (interest) + D4 (identity)
  compose into an interest profile bound to a persistent pseudonymous ID.
- [[two-regimes-of-leakage]] — D2 is the content-dependent regime, here shown to
  host a real threat despite SOP.
- [[papoutsaki-2017-searchgazer]] — the tool-framed ancestor D2 weaponizes.
- [[gaze-perturbation-defense]] — the RQ5 defense, traded against reading
  relevance-feedback utility ([[buscher-2012-attentive-documents]]).
- [[target-venues]] — PETS/PoPETs primary, SOUPS companion.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` (all sections); Report §3.1, §4
  (D2, content-dependent regime); plan §4 (D2 set aside for D4 — the constraint
  this direction works within).

## Open questions

- Ground truth for *intent* (self-report) is softer than for *examination* (IR
  fixations); the direction leads with examination recovery and treats intent as
  the interpretation layer — verify this holds once real data exists.
