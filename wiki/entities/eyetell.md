---
type: entity
subtype: attack
tags: [attack, mobile, content-dependent, keystroke-inference]
aliases: [EyeTell, EyeTell [27]]
sources: [information-leakage-report, reid-research-plan, chen-2018-eyetell]
reviewed: false
updated: 2026-07-11
---

**EyeTell** [27] is a content-dependent keystroke-inference attack: it
reconstructs touchscreen soft-keyboard input (PINs, passwords) from a *video of
the user's eyes*. It is one of the best-evidenced mobile gaze attacks and, in
GazePry's framing, a member of the **content-dependent** contrast class that
Direction 1 is explicitly *not* (identity, not secrets).

## Key facts

- Reported accuracy (verified against the paper, [[chen-2018-eyetell]]): 4-digit
  PIN **top-5 65%**, top-10 74%, **top-50 90%**; Android lock-pattern **top-5
  70.3%**, top-50 85.1%; words top-5 38.43%, top-50 72.45% [27].
- The **≈70%** figure is the **lock-pattern top-5**, not a 6-digit PIN; the old
  "PIN top-1 ≈39%" was a misread of the **word top-5 (38.43%)** (plan §21).
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

- Report §3.1, §6 [27]; Protocol §2 (delta table); plan §3.1, §7 (delta
  table), §18.7, §21 (correction) [27]; [[chen-2018-eyetell]] (paper).
