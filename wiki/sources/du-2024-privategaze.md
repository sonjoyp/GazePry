---
type: source
tags: [paper, defense, mobile, black-box, obfuscation, preprint]
aliases: [Du et al. 2024, PrivateGaze]
sources: [du-2024-privategaze]
reviewed: false
updated: 2026-07-11
---

Du, Jia, Zhang, Lan (TU Delft / Penn State) — *PrivateGaze: Preserving User
Privacy in Black-box Mobile Gaze Tracking Services*, arXiv:2408.00950, 2024 —
bibliography **[23]** (**preprint-flagged** in plan §21). Defends the *cloud
gaze service* threat directly relevant to the [[gazecloud]] arm: obfuscate the
uploaded face so identity/gender can't be recovered, without hurting gaze
accuracy. (`raw/PrivateGaze...-2024.pdf`)

## Key facts

- Motivating threat is exactly [[gazecloud]]'s: mobile gaze services require the
  user to upload **full-face images** to a black-box estimator, which a
  malicious provider could mine for **identity, gender**, and other attributes.
- Trains a **privacy preserver** that converts full-face images into obfuscated
  counterparts — still usable for gaze estimation, but stripped of private
  attributes. Evaluated on four datasets; comparable tracking accuracy.
- The natural defense to cite alongside GazePry's finding that the most
  accurate drop-in tracker ([[gazecloud]]) is the one that exfiltrates the face.

## Related

- [[gazecloud]] — the cloud-upload threat PrivateGaze targets.
- [[gaze-perturbation-defense]] — the RQ5 defense landscape (image-level here,
  vs GazePry's stream-level perturbation).
- [[enabling-conditions]] — the camera-grant / face-upload exposure.

## Mentions in sources

- Plan §16 (black-box mobile gaze defense), §18.6, §21 (preprint flag) [23];
  report §7 [23].
