---
type: concept
tags: [browser-security, scope, threat-model]
aliases: [Same-Origin Policy, SOP, Site Isolation, Cross-Tab Peeking]
sources: [information-leakage-report, direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

The **same-origin policy** (and browser site isolation) is the constraint that
*shapes* GazePry's contribution. It blocks a script in one tab/origin from
reading the gaze stream on another — so cross-tab **content peeking is not
feasible** — which redirects the cross-site threat toward content-independent
[[gaze-re-identification|re-identification]].

## Key facts

- Rules out the most alarming scenario (a background page silently reading what
  you look at on your bank's site). This is a *tightening* of the threat model
  and should be presented as such.
- The realistic cross-site risk is therefore behavioral-biometric re-ID [20],
  [29], not reading another site's content.
- **Turns the limitation into the thesis:** re-ID is content-independent, so SOP
  does not touch it — two first-party sites embedding the same tag link the same
  visitor by gaze. This is exactly why the [[prototype-readme|prototype]] does
  not attempt content peeking.

## Related

- [[two-regimes-of-leakage]] — SOP blocks content-dependent cross-site leakage,
  not content-independent.
- [[gaze-re-identification]] — the SOP-proof cross-site channel.
- [[drive-by-web-adversary]] — SOP defines this adversary's out-of-scope line.

## Mentions in sources

- Report §1, §8 (What Tightens the Threat Model); Protocol §1, §2;
  `prototype/README.md` (Two regimes on purpose).
