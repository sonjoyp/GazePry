---
type: source
tags: [paper, web-tracking, cross-device, linkage, baseline]
aliases: [Zimmeck et al. 2017, A Privacy Analysis of Cross-device Tracking]
sources: [zimmeck-2017-cross-device]
reviewed: false
updated: 2026-07-11
---

Zimmeck, Li, Kim, Bellovin, Jebara (CMU / Columbia) — *A Privacy Analysis of
Cross-device Tracking*, **USENIX Security 2017** — bibliography **[46]**. The
prior model for linking one **person** across devices/contexts — which gaze does
*without* the shared-network / deterministic-identifier assumptions this work
relies on. (`raw/A Privacy Analysis of Cross-device Tracking...-2017.pdf`)

## Key facts

- Documents the shift from browser/device tracking to **people-tracking** as
  users move across phones, laptops, tablets; analyzes the signals (shared IPs,
  deterministic identifiers, behavioral correlation) used to link devices to one
  person.
- GazePry's cross-device claim is stronger in kind: gaze links a person **across
  a fresh device** with no shared network, cookie, or account — the biometric
  rides with the body, not the device fleet.

## Related

- [[person-bound-fingerprint]] — cross-device linkage without device signals.
- [[unclearability]] — RQ4 cross-device survival.
- [[acar-2014-web-never-forgets]], [[vastel-2018-fp-stalker]] — the stateless
  web-tracking baseline group.

## Mentions in sources

- Plan §6 (contribution 1, cross-device without shared-network assumptions),
  §18.5 [46]; protocol §15.5 [46].
