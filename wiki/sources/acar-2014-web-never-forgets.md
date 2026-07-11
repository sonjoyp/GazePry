---
type: source
tags: [paper, web-tracking, fingerprinting, evercookie, baseline]
aliases: [Acar et al. 2014, The Web Never Forgets, canvas fingerprinting in the wild]
sources: [acar-2014-web-never-forgets]
reviewed: false
updated: 2026-07-11
---

Acar, Eubank, Englehardt, Juarez, Narayanan, Diaz (KU Leuven / Princeton) —
*The Web Never Forgets: Persistent Tracking Mechanisms in the Wild*, **ACM CCS
2014** — bibliography **[44]**. The reference for "persistent tracking
mechanisms" and the **rhetorical anchor** for GazePry's title framing
("unclearable"). Defines the *clearable* fingerprint baseline gaze is argued to
beat. (`raw/The Web Never Forgets...-2014.pdf`)

## Key facts

- First large-scale measurement of **canvas fingerprinting** (>5% of the top
  100,000 sites), **evercookies / respawning** (new IndexedDB vector), and
  **cookie syncing** amplifying tracking reach.
- These are **stateful or device-bound** mechanisms — powerful but ultimately
  clearable or resettable (clear storage, new device, anti-FP browser). That is
  the bar GazePry claims a **person-bound** gaze identifier clears: it survives
  the clear.
- Supplies the "clearable cookie" comparison used as a baseline in
  [[reid-metrics]] (canvas/UA fingerprint as the *resettable* control).

## Related

- [[person-bound-fingerprint]] — the contrast: gaze is person-bound, these are
  device-bound.
- [[vastel-2018-fp-stalker]], [[zimmeck-2017-cross-device]] — the other
  stateless-tracking baselines.
- [[unclearability]] — the property gaze has that these lack.
- [[weinberg-2011-history-sniffing]] — the history side channel it pairs with.

## Mentions in sources

- Plan §6 (contribution 1, vs device-bound FP), §14 (clearable baseline),
  §18.5 [44]; protocol §15.5 [44].
