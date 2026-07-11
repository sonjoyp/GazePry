---
type: source
tags: [paper, defense, k-anonymity, re-identification, dataset-privacy]
aliases: [David-John et al. 2022, For Your Eyes Only, privacy-preserving eye-tracking datasets]
sources: [david-john-2022-for-your-eyes-only]
reviewed: false
updated: 2026-07-11
---

David-John, Butler, Jain (University of Florida) — *For Your Eyes Only:
Privacy-preserving eye-tracking datasets*, **ETRA 2022** — bibliography
**[49]**. The defense whose threat model **matches GazePry most exactly**:
k-anonymity / plausible deniability applied specifically to defeat eye-movement
**re-identification** on datasets. (`raw/For Your Eyes Only...-2022.pdf`)

## Key facts

- Eye-tracking datasets collected during ordinary VR tasks were shown to enable
  **unique identification**; this paper adapts **k-anonymity / plausible
  deniability** to suppress that re-ID while preserving downstream utility
  (activity/intent classification).
- Directly targets the *same attack* GazePry mounts (re-ID from gaze), so its
  privacy mechanism is the most on-point comparison for RQ5.

## Related

- [[gaze-perturbation-defense]] — RQ5; the closest-matching prior defense.
- [[gaze-re-identification]] — the attack it defends against.
- [[david-john-2021-streaming-privacy]] — the same group's streaming defense.
- [[steil-2019-gaze-dp]], [[li-2021-kaleido]] — the DP alternatives.

## Mentions in sources

- Plan §16 (k-anonymity/plausible deniability vs re-ID), §18.6 [49]; protocol
  §11, §15.6 [49].
