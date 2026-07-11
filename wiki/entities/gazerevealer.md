---
type: entity
subtype: attack
tags: [attack, mobile, content-dependent, password-inference]
aliases: [GazeRevealer, GazeRevealer [8]]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

**GazeRevealer** [8] infers smartphone PINs/passwords from the **front camera
alone**, mapping eye movements onto a known on-screen keypad. Like
[[eyetell]], it is a content-dependent mobile attack — the contrast class to
GazePry's content-independent [[gaze-re-identification|re-identification]] thesis.

## Key facts

- Reported accuracy: single digit ≈77.9%; full 6-digit password ≈84.4% under
  ideal conditions [8].
- Wang et al., *Your Eyes Reveal Your Secrets: An Eye Movement Based Password
  Inference on Smartphone*, IEEE TMC 2020 [8].
- Evidence for form-factor analysis: the smartphone is the best-evidenced
  surface for concrete attacks.

## Related

- [[eyetell]] — sibling mobile keystroke-inference attack.
- [[leakage-vectors-d1-d6]] — vector D1.
- [[form-factor-analysis]] — smartphone as best-evidenced surface.

## Mentions in sources

- Report §3.1, §5.2, §6 [8]; Protocol §16 [8].
