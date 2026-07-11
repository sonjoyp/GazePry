---
type: concept
tags: [tracking, fingerprinting, thesis, core]
aliases: [Person-Bound Fingerprint, Hardware-Grounded Fingerprint, Unclearable Identifier]
sources: [direction-1-study-protocol, information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The project's central framing: gaze is a **person-bound**, physically grounded
identifier — unlike canvas/font/device fingerprints, which are *device-bound*
and reset on a new device or defeated by anti-fingerprinting browsers. Because
gaze coordinates derive from involuntary physical eye behavior rather than
JavaScript-reported values, they behave as a [[hardware-grounded-fingerprint]]
that bypasses script-layer defenses.

## Key facts

- **Contribution 1** of Direction 1: gaze as a cookieless, cache-proof,
  incognito-surviving, cross-device re-identifier.
- Distinction from conventional fingerprints (the "clearable cookie" baseline):
  canvas fingerprinting [44], evolving-fingerprint linkage FP-STALKER [45], and
  cross-device tracking [46] are *stateless but device-bound* and can be reset;
  gaze is person-bound and survives a fresh device + [[survives-de-identification|
  face removal]].
- Nearest external analogues are behavioral biometrics that scale to huge
  galleries in VR (50,000+ users from head/hand motion [39]; cross-device 360°
  VR re-ID [40]) — supporting analogies, not the same setting.

## Related

- [[gaze-re-identification]] — the mechanism that realizes this fingerprint.
- [[hardware-grounded-fingerprint]] — the "bypasses script-layer defenses"
  property.
- [[unclearability]] — the empirical test (RQ4) of the "unclearable" claim.

## Mentions in sources

- Protocol §1 (contributions), §2 (delta table); Report §1 (central premise).
