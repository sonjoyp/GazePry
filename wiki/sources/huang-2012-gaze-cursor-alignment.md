---
type: source
tags: [paper, mouse-cursor, gaze, web-search, serp, abandonment]
aliases: [Huang White Buscher 2012, User See User Point, Gaze and Cursor Alignment in Web Search]
sources: [huang-2012-gaze-cursor-alignment]
reviewed: false
updated: 2026-07-16
---

Huang, White & Buscher — *User See, User Point: Gaze and Cursor Alignment in Web
Search*, **CHI '12**, pp. 1341–1350, doi:10.1145/2207676.2208591. Characterizes
**how closely the cursor tracks gaze** and, critically, that the correlation is
**strongest on SERPs** — which is why the [[reading-search-intent-leakage|D2
direction]] makes SERP scanning its headline surface. Also links cursor activity
to **result relevance** and **good-vs-bad abandonment**. Cited **author-year**
(not in plan §21). *(Grounding: retrieved abstract/metadata, web search
2026-07-16 — not a full-PDF read.)*

## Key facts

- When a user **moves or clicks** the mouse, the cursor is relatively close to
  gaze; cursor–gaze correlation is **stronger on SERPs than other pages** — the
  fusion signal D2 leans on ([[cursor-tracking]]).
- Analyzes cursor activity types — hyperlink clicks, non-link clicks, **hover** —
  and uses them to **estimate result relevance** and **differentiate good vs bad
  abandonment** (the zero-click intent D2 recovers).
- Bounds the cursor floor honestly: alignment holds *during active mouse motion*;
  not every user moves the cursor where they look — the gaze ceiling covers
  low-cursor users.

## Related

- [[cursor-tracking]] — alignment is the mechanism of the cursor-as-gaze-proxy.
- [[huang-2011-no-clicks-no-problem]] — the Web-scale companion.
- [[li-2009-good-abandonment]], [[williams-2016-good-abandonment]] — the
  abandonment behavior this links to cursor activity.
- [[reading-search-intent-leakage]] — why SERPs are the D2 headline surface.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` §3, §6, §7, §9, §10, §11 [G3].
