---
type: source
tags: [paper, attack, content-dependent, keystroke-inference, vr, avatar]
aliases: [Wang et al. 2024, GAZEploit]
sources: [wang-2024-gazeploit]
reviewed: false
updated: 2026-07-11
---

Wang, Zhan, Shan, Dai, Panoff, Wang — *GAZEploit: Remote Keystroke Inference
Attack by Gaze Estimation from Avatar Views in VR/MR Devices*, **ACM CCS 2024**
— bibliography **[14]**. A content-*dependent* keystroke-inference attack in
VR/MR: it recovers typed text from the **gaze of a user's virtual avatar**, not
from a physical camera. In the plan's delta table it is the VR sibling of
[[eyetell]]. (`raw/GAZEploit...-2024.pdf`)

## Key facts

- Estimates gaze from **avatar eye renderings** (as broadcast in VR/MR social
  apps) and maps it onto the virtual keyboard to infer keystrokes — remote, no
  device compromise.
- Reported: click-candidate identification ≈85.9% precision / 96.8% recall;
  **top-5 keystroke inference ≈92.1% for messages**; over 80% top-5 precision;
  character inference 34.6% top-1 / 77.0% top-5; >80% overall with 30
  participants.
- Adversary is remote but relies on a **known virtual keyboard layout**
  (content-dependent) — again the contrast class GazePry is not.

## Related

- [[eyetell]] — the touchscreen sibling in the plan's content-dependent delta
  table.
- [[two-regimes-of-leakage]] — content-dependent regime.
- [[slocum-2023-arvr-keylogging]] — sibling VR keylogging via head motion.
- [[leakage-vectors-d1-d6]] — D1-type inference in a VR setting.

## Mentions in sources

- Plan §7 (delta table: GAZEploit content-dependent vs content-independent),
  §18.7 [14]; protocol §2, §16 [14].
