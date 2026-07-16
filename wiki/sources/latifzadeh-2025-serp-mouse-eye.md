---
type: source
tags: [paper, preprint, dataset, mouse-cursor, eye-tracking, serp]
aliases: [Latifzadeh 2025, Versatile Dataset Mouse Eye SERP, SERP mouse and eye dataset]
sources: [latifzadeh-2025-serp-mouse-eye]
reviewed: false
updated: 2026-07-16
---

Latifzadeh, Gwizdka & Leiva — *A Versatile Dataset of Mouse and Eye Movements on
Search Engine Results Pages*, 2025, **arXiv:2508… — preprint (arXiv:2507.08003)**.
A public dataset with **simultaneous mouse cursor and eye-tracking** on Google
SERPs — the closest existing resource to the [[reading-search-intent-leakage|D2
direction]]'s own capture, usable for a large-N feasibility ceiling. **Flag as
preprint**; verify license before use. Cited **author-year** (not in plan §21).
*(Grounding: arXiv abstract fetched 2026-07-16 — not a full read.)*

## Key facts

- **47 participants**, **2,776 transactional queries** on Google SERPs.
- Contains **both eye-tracking and mouse-movement** recordings, plus HTML source,
  screenshots, and **advertisement bounding boxes** — enough to correlate visual
  attention with cursor behavior at the AOI level.
- For D2: lets the **cursor-floor vs gaze-ceiling** gap and gaze–cursor alignment
  be prototyped on real SERPs before fresh simultaneous capture.

## Related

- [[leiva-2020-attentive-cursor]] — cursor-only predecessor dataset.
- [[cursor-tracking]] — the channel; [[simultaneous-capture-rig]] — the D2 capture
  this dataset stands in for.
- [[reading-search-intent-leakage]] — the direction that reuses it.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` §6, §11, §12 [G5].

## Open questions

- Confirm the exact arXiv ID (2507.08003) and license/terms before ingesting the
  data.
