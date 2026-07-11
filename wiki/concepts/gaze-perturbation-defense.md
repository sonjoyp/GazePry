---
type: concept
tags: [defense, rq5, privacy, mitigation]
aliases: [Gaze Perturbation Defense, Defense, RQ5, Privacy-Utility Curve, D6 Defense]
sources: [direction-1-study-protocol, information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The optional **defense** direction (RQ5 / vector D6): an in-browser layer that
perturbs the client-side gaze stream to raise attacker EER at bounded utility
cost. Because gaze is a [[hardware-grounded-fingerprint]], the defense must
perturb the *signal*, not spoof reported values. Deliverable: a **privacy–utility
tradeoff curve**.

## Key facts

- Perturbations to evaluate: temporal/Gaussian noise, down-sampling, spatial
  differential privacy (David-John et al. [24]), streaming-DP [13]; foundational
  feature-level gaze-DP is Steil et al. [47]; Kalεido [48] is a real-time
  gaze-DP *system* with formal guarantees; "For Your Eyes Only" [49] applies
  k-anonymity/plausible deniability specifically against eye-movement re-ID.
- Utility task: reading-AOI detection or an accessibility metric must stay
  acceptable while attacker EER rises.
- Implementation hook: perturb the stream in [[gazepry-tracker]] before it POSTs
  to the [[reid-server]].
- Pairing an attack with a defense "reviews better."

## Related

- [[unclearability]] / [[gaze-re-identification]] — the attack a defense must
  raise EER against.
- [[gazepry-tracker]] — where perturbation is applied.
- [[hardware-grounded-fingerprint]] — why signal-level perturbation is required.

## Mentions in sources

- Protocol §1 (contribution 3), §3 (RQ5), §11 (Defense), §15.6 [47]–[49];
  Report §4 (D6), §7 [13], [23], [24].
