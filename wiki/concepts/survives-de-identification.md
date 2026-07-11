---
type: concept
tags: [biometrics, threat-model, privacy]
aliases: [Survives De-Identification, Survives Face Removal, De-facing, Identity Survives De-facing]
sources: [information-leakage-report, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

The eye-movement biometric is carried by **movement dynamics, not appearance**,
so stripping facial identity from the video does *not* remove it. A defense or
consent notice premised on "we do not store your face" therefore does not, on
its own, prevent [[gaze-re-identification|re-identification]].

## Key facts

- A *loosening* of the threat model (it makes the adversary stronger): consent
  dialogs framed around "the camera cannot see your face" understate the actual
  exposure [20], [29].
- Enforced cleanly in the prototype: the primary [[gaze-feature-extraction|
  feature set]] **excludes** raw face/appearance features, so the
  "survives de-identification" claim is clean. An appearance-*including* arm is
  run only as an upper bound, to quantify dynamics-vs-appearance signal.

## Related

- [[gaze-re-identification]] — what survives.
- [[eye-movement-biometrics]] — the dynamics that carry identity.
- [[unclearability]] — a sibling "survives X" property.

## Mentions in sources

- Report §1, §8 (Identity survives de-facing); Protocol §1, §7 (critical
  control — exclude appearance).
