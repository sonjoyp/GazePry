---
type: entity
subtype: attack
tags: [attack, mobile, content-dependent, keystroke-inference]
aliases: [EyeTell, EyeTell [27]]
sources: [information-leakage-report, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

**EyeTell** [27] is a content-dependent keystroke-inference attack: it
reconstructs touchscreen soft-keyboard input (PINs, passwords) from a *video of
the user's eyes*. It is one of the best-evidenced mobile gaze attacks and, in
GazePry's framing, a member of the **content-dependent** contrast class that
Direction 1 is explicitly *not* (identity, not secrets).

## Key facts

- Reported accuracy: 4-digit PIN top-1 ≈39%, top-5 ≈65%, top-50 ≈90%; 6-digit
  PIN top-5 ≈70% [27].
- Assumes a physically-present camera filming the victim — a *stronger* adversary
  than GazePry's [[drive-by-web-adversary]].
- Chen et al., *EyeTell: Video-Assisted Touchscreen Keystroke Inference from Eye
  Movements*, IEEE S&P 2018 [27].
- Appears in the protocol's delta table as content-*dependent* keystroke
  inference, contrasted with content-*independent* identity.

## Related

- [[gazerevealer]] — sibling mobile password-inference attack.
- [[leakage-vectors-d1-d6]] — vector D1.
- [[two-regimes-of-leakage]] — the content-dependent regime.

## Mentions in sources

- Report §3.1, §6 [27]; Protocol §2 (delta table), §15.7 [27], §16 [27].
