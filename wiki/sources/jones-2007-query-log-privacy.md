---
type: source
tags: [paper, privacy, query-logs, web-search, re-identification]
aliases: [Jones 2007, I Know What You Did Last Summer, query logs and user privacy]
sources: [jones-2007-query-log-privacy]
reviewed: false
updated: 2026-07-16
---

Jones, Kumar, Pang & Tomkins — *"I Know What You Did Last Summer": Query Logs and
User Privacy*, **CIKM '07**, pp. 909–914, doi:10.1145/1321440.1321573. The
reference **query-log privacy** attack: subtle identity cues in a user's sequence
of **queries and clicks** enable a trace attack. The [[reading-search-intent-leakage|D2 direction]]
**extends this threat model** from queries+clicks to the previously-unlogged
**examination layer** (what was looked at / considered / read
without clicking). Cited **author-year** (not in plan §21). *(Grounding: retrieved
abstract/metadata, web search 2026-07-16 — not a full-PDF read.)*

## Key facts

- Introduces the **trace attack**: from a privacy-enhanced sequence of a user's
  searches, recover information about the user.
- Uses anonymized Yahoo! query logs + user profiles (age, zip, gender) — leakage
  is from **queries and clicks**, the layer D2 argues is now *incomplete*.
- The D2 gap: query-log privacy has **never incorporated the gaze/cursor
  examination signal**, which is strictly more revealing (zero-click,
  considered-but-unclicked).

## Related

- [[gervais-2014-web-search-privacy]] — a later *quantification* of web-search
  privacy (CCS), the top-venue precedent D2 cites.
- [[weinberg-2011-history-sniffing]] — the "recover what you looked at" side-channel
  analogue already in the project bibliography [5].
- [[reading-search-intent-leakage]] — the direction that extends this.

## Mentions in sources

- `GazePry_D2_Reading_Search_Intent_Direction.md` §3, §9, §11 [Q1].
