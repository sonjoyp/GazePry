---
type: concept
tags: [fingerprinting, threat-model, premise]
aliases: [Hardware-Grounded Fingerprint, Physically Grounded Signal, Bypasses Script-Layer Defenses]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The **premise** underlying the whole leakage assessment: because gaze
coordinates derive from *physical* (largely involuntary) eye behavior rather
than from JavaScript-reported values, they behave as a hardware-grounded signal
that ordinary software-level privacy defenses do not touch.

## Key facts

- Defenses it bypasses: anti-fingerprinting countermeasures, sandboxing, value
  spoofing — all operate at the script layer, whereas gaze is produced below it
  by the camera + the user's oculomotor system.
- This is why gaze leakage "is not incidental" and why the
  [[person-bound-fingerprint]] framing works.
- The same property means a defense must perturb the *signal*
  ([[gaze-perturbation-defense]]), not merely spoof reported values.

## Related

- [[person-bound-fingerprint]] — the tracking framing that builds on this.
- [[gaze-perturbation-defense]] — the defense class the premise forces.

## Mentions in sources

- Report §1 (Executive Summary — central premise).
