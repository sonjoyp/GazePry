---
type: source
tags: [paper, mouse-cursor, web-search, gaze-proxy, extended-abstract]
aliases: [Guo Agichtein 2010, Towards predicting web searcher gaze position from mouse movements]
sources: [guo-2010-gaze-from-cursor]
reviewed: false
updated: 2026-07-16
---

Guo & Agichtein — *Towards Predicting Web Searcher Gaze Position from Mouse
Movements*, **CHI '10 Extended Abstracts**, pp. 3601–3606,
doi:10.1145/1753846.1754025. Early evidence that **mouse cursor position is a
usable proxy for gaze** during web search — a foundation for the permission-free
[[cursor-tracking]] floor in the [[reading-search-intent-leakage|D2 direction]].
Cited **author-year** (not in plan §21). *(Grounding: retrieved
abstract/metadata, web search 2026-07-16 — not a full-PDF read.)*

## Key facts

- 10 subjects × 20 search tasks; eye + mouse recorded on navigational and
  informational tasks.
- Reported ~**77% accuracy** predicting *when* gaze and cursor are strongly
  aligned, using cursor features.
- Cursor–gaze distances longer along the **x-axis** than the y-axis.
- **Extended abstract / poster** — note the venue type when citing; the fuller
  treatment of cursor-as-gaze-proxy is Huang/White/Dumais 2011 and
  Huang/White/Buscher 2012.

## Related

- [[cursor-tracking]] — the permission-free channel this grounds.
- [[huang-2011-no-clicks-no-problem]], [[huang-2012-gaze-cursor-alignment]] — the
  Web-scale and alignment follow-ups.
- [[reading-search-intent-leakage]] — the D2 attack that reframes this as leakage.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` §3, §7, §11 [G1].

## Open questions

- Deepen from the full PDF: exact cursor feature set and the alignment-detection
  method behind the 77% figure.
