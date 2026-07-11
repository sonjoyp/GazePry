---
type: source
tags: [paper, attack, side-channel, browsing-history, web]
aliases: [Weinberg et al. 2011, I Still Know What You Visited Last Summer, history sniffing]
sources: [weinberg-2011-history-sniffing]
reviewed: false
updated: 2026-07-11
---

Weinberg, Chen, Jayaraman, Jackson — *I Still Know What You Visited Last
Summer: Leaking Browsing History via User Interaction and Side Channel
Attacks*, **IEEE S&P 2011** — bibliography **[5]**. A classic web
history-leak side channel; GazePry cites it as the "clearable cookie"-adjacent
rhetorical anchor that pairs with the fingerprinting baseline.
(`raw/I Still Know What You Visited Last Summer...-2011.pdf`)

## Key facts

- Recovers a user's **browsing history** via interaction-based and side-channel
  techniques even after CSS `:visited` sniffing was mitigated.
- The paper's framing — "history leaks despite defenses" — parallels GazePry's
  argument that gaze re-ID leaks despite state-clearing defenses; the title
  echoes [[acar-2014-web-never-forgets|"The Web Never Forgets"]].
- A *stateful/side-channel* web-privacy attack, distinct from the stateless,
  person-bound gaze channel; used for rhetorical positioning, not method.

## Related

- [[acar-2014-web-never-forgets]] — the persistent-tracking companion it pairs
  with (§18.7).
- [[unclearability]] — the "leaks despite defenses" theme.
- [[same-origin-policy]] — history sniffing is another SOP-boundary side channel.

## Mentions in sources

- Plan §18.7 (pairs with [44]–[46] as the clearable-cookie history side
  channel) [5]; report references [5].
