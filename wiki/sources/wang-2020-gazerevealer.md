---
type: source
tags: [paper, attack, content-dependent, password-inference, mobile]
aliases: [Wang et al. 2020, GazeRevealer paper, Your Eyes Reveal Your Secrets]
sources: [wang-2020-gazerevealer]
reviewed: false
updated: 2026-07-11
---

Wang, Cai, Gu, Shao — *Your Eyes Reveal Your Secrets: An Eye Movement Based
Password Inference on Smartphone*, **IEEE TMC 2020** — bibliography **[8]**.
The [[gazerevealer]] attack: smartphone PIN/password inference from the **front
camera alone**. Content-*dependent*, and a best-evidenced mobile attack for
[[form-factor-analysis]]. (`raw/Your Eyes Reveal Your Secrets...-2020.pdf`)

## Key facts

- Uses only the phone's **front camera** (no external filming, unlike
  [[eyetell]]) to map eye movements onto a known keypad and recover the entered
  digits/password.
- Reported accuracy: single digit ≈**77.5–77.9%**; full 6-digit password
  ≈**84.4%** under ideal conditions [8].
- Reinforces the report's finding that on mobile, the **camera-permission grant
  itself** becomes the dominant leakage vector (once a page holds the video
  stream, pointing accuracy matters less).

## Related

- [[gazerevealer]] — the attack entity.
- [[eyetell]] — sibling attack (needs an external camera; GazeRevealer needs
  only the front camera).
- [[leakage-vectors-d1-d6]] — vector D1.
- [[form-factor-analysis]] — smartphone as best-evidenced surface.

## Mentions in sources

- Plan §3.1 (≈77.9% / 84.4%), §18.7 [8]; report §3.1, §5.2, §6 [8].
