---
type: source
tags: [threat-model, survey, leakage]
aliases: [Information Leakage Report, Leakage Assessment, Threat-Model Report, GazePry_Information_Leakage_Report]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The project's threat-model assessment: *Information Leakage in Webcam-Based Eye
Tracking on Laptops, Smartphones, and Tablets*. It argues that a
[[gaze-estimation|webcam eye tracker]] leaks substantial sensitive information
across all three device classes, and it establishes the vocabulary the rest of
the project uses: the [[two-regimes-of-leakage]], the six [[leakage-vectors-d1-d6]],
and the [[drive-by-web-adversary]] threat model. Holds the shared bibliography
entries **[1]–[29]**.

## Key facts

- **Central premise:** gaze derives from physical, largely involuntary eye
  behavior, so it behaves as a [[hardware-grounded-fingerprint]] that bypasses
  script-layer defenses (anti-fingerprinting, sandboxing, value spoofing).
- Three classes of leaked information from the literature: (i) on-screen
  secrets (PINs, passwords, reading/search content); (ii) cognitive/affective
  state; (iii) stable personal attributes (identity, gender, age, origin).
- **Two regimes** ([[two-regimes-of-leakage]]): content-dependent (needs known
  layout; attacker-controlled page) vs content-independent (movement dynamics;
  survives not knowing the screen).
- **Leakage vectors** [[leakage-vectors-d1-d6]]: D1 keypad/PIN, D2 reading/search,
  D3 cognitive/affective state, D4 [[gaze-re-identification|re-ID & tracking]],
  D5 attribute/demographic, D6 defenses.
- **Form-factor split** ([[form-factor-analysis]]): laptop/desktop is the
  *primary novel surface* (favorable head pose, large screen, least studied);
  smartphone is *best evidenced* ([[eyetell]], [[gazerevealer]]); tablet is
  *least studied* (interpolated).
- Two model-tightening facts: cross-tab content peeking is blocked by
  [[same-origin-policy]] (so the cross-site risk is re-ID, not reading another
  site); the eye-movement biometric [[survives-de-identification|survives face removal]].
- Key evidence numbers live in [[evidence-summary]]; enabling conditions
  (camera-consent gap, [[covert-calibration]], third-party embedding) in
  [[enabling-conditions]].

## Related

- [[direction-1-study-protocol]] — turns this report's §8 limitation (SOP
  blocks content peeking) into a thesis about re-identification.
- [[two-regimes-of-leakage]], [[leakage-vectors-d1-d6]], [[form-factor-analysis]],
  [[evidence-summary]] — the concept pages distilled from this report.

## Mentions in sources

- `GazePry_Information_Leakage_Report.md` §1 Executive Summary; §3 Two Regimes;
  §4 Vectors D1–D6; §5 Form-Factor Analysis; §6 Evidence; §7 Enabling
  Conditions; §8 What Tightens/Loosens; §9 Conclusion; References [1]–[29].
