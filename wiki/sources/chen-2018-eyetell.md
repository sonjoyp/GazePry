---
type: source
tags: [paper, attack, content-dependent, keystroke-inference, mobile]
aliases: [Chen et al. 2018, EyeTell paper]
sources: [chen-2018-eyetell]
reviewed: false
updated: 2026-07-11
---

Chen, Li, Zhang, Zhang, Hedgpeth — *EyeTell: Video-Assisted Touchscreen
Keystroke Inference from Eye Movements*, **IEEE S&P 2018** — bibliography
**[27]**. The canonical content-*dependent* mobile gaze attack and the source
of the numbers the plan §21 corrected. Backs the [[eyetell]] entity.
(`raw/EyeTell...-2018.pdf`)

## Key facts

- Reconstructs touchscreen input from a **video of the victim's eyes** by
  mapping gaze onto a known soft-keyboard layout; iOS + Android; PIN,
  pattern-lock, and alphabetical keyboards.
- **Actual figures (from the paper's abstract):**
  - 4-digit **PIN**: top-5 **65%**, top-10 74%, top-50 **90%**.
  - Android **lock pattern**: top-5 **70.3%**, top-10 75.3%, top-50 85.1%.
  - **Words**: top-5 **38.43%**, top-10 63.19%, top-25 71.3%, top-50 72.45%.
- **Resolves two earlier misquotes (plan §21):** the "≈70%" figure is the
  **lock-pattern top-5** (70.3%), not a 6-digit PIN; and the old "4-digit PIN
  top-1 ≈39%" was a conflation of the **word top-5 (38.43%)** — there is no
  39% PIN-top-1 result. Quote PIN and pattern figures separately.
- Adversary model is **stronger** than GazePry's: a physically present camera
  filming the victim's face. It is the content-*dependent* contrast class the
  plan explicitly is *not* (identity, not secrets).

## Related

- [[eyetell]] — the attack entity.
- [[gazerevealer]] — sibling mobile password-inference attack.
- [[two-regimes-of-leakage]] — the content-dependent regime.
- [[leakage-vectors-d1-d6]] — vector D1.

## Mentions in sources

- Plan §3.1, §7 (delta table), §18.7, **§21 (corrections)** [27]; report §3.1,
  §6 [27].
