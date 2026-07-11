---
type: concept
tags: [defense, rq5, privacy, mitigation]
aliases: [Gaze Perturbation Defense, Defense, RQ5, Privacy-Utility Curve, D6 Defense]
sources: [reid-research-plan, information-leakage-report]
reviewed: false
updated: 2026-07-11
---

The optional **defense** direction (RQ5 / vector D6): an in-browser layer that
perturbs the client-side gaze stream to raise attacker EER at bounded utility
cost. Because gaze is a [[hardware-grounded-fingerprint]], the defense must
perturb the *signal*, not spoof reported values. Deliverable: a **privacy–utility
tradeoff curve**.

## Key facts

- Perturbations to evaluate: temporal/Gaussian noise, down-sampling, spatial
  differential privacy ([[david-john-2021-streaming-privacy|David-John et al.]]
  [24]), streaming-DP + VR robustness/UX ([[wilson-2024-vr-gaze-streaming]]
  [13]); foundational feature-level gaze-DP is [[steil-2019-gaze-dp|Steil et
  al.]] [47]; [[li-2021-kaleido|Kalεido]] [48] is a real-time gaze-DP *system*
  with formal guarantees; [[david-john-2022-for-your-eyes-only|"For Your Eyes
  Only"]] [49] applies k-anonymity/plausible deniability specifically against
  eye-movement re-ID (the closest-matching threat model). Black-box mobile
  face-obfuscation ([[du-2024-privategaze|PrivateGaze]] [23]) targets the
  [[gazecloud]]-style cloud-upload threat.
- **Scope caveat:** partial, uncoordinated protections can be undone when a
  second signal is left unprotected ([[aziz-2025-uncoordinated-protections]]
  [41]) — scope the defense against all channels.
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

- Plan §6 (contribution 3), §8 (RQ5), §16 (Defense), §18.6 [13], [23], [24],
  [47]–[49], [41]; report §4 (D6), §7 [13], [23], [24].
