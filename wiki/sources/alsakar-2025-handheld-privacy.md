---
type: source
tags: [paper, privacy, mobile, attribute-inference, handheld]
aliases: [Alsakar et al. 2025, Privacy Implications of Eye Tracking on Handheld Mobile Devices]
sources: [alsakar-2025-handheld-privacy]
reviewed: false
updated: 2026-07-11
---

Alsakar, Alotaibi, Khamis, Stumpf (Glasgow / Taif) — *Assessing and Mitigating
the Privacy Implications of Eye Tracking on Handheld Mobile Devices*, **ACM
TOPS 2025** — bibliography **[10]**. The best-evidenced **handheld attribute
inference** result and a key delta point: mobile gaze leaks *attributes* on a
*single site*, whereas GazePry is desktop, cross-site, and about *identity*.
(`raw/Assessing and Mitigating the Privacy Implications...-2025.pdf`)

## Key facts

- On the SmartEyePhone dataset, front-camera gaze leaks on average **≈65.5% of
  private attributes** (age, gender, nationality, plus task/state signals);
  differential-privacy mitigation cuts leakage (report cites ≈10–28%).
- Attacker model: a black-box mobile gaze service or an interceptor of the gaze
  stream/model transfer infers sensitive attributes — the same cloud-service
  exposure [[du-2024-privategaze|PrivateGaze]] defends and [[gazecloud]]
  embodies.
- The plan's Related-Work **delta**: Alsakar is *mobile, attribute inference,
  single site*; GazePry is *desktop, cross-site linkage, identity* — same
  literature, orthogonal cell.

## Related

- [[form-factor-analysis]] — smartphone as the best-evidenced surface.
- [[leakage-vectors-d1-d6]] — vector D5 (attributes/demographics).
- [[evidence-summary]] — the ≈65.5% figure lives in the evidence table.
- [[related-work-direction-1]] — the handheld-vs-desktop delta.

## Mentions in sources

- Plan §2 (delta table), §4 (D5 evidence), §18.4 [10]; report §5.2, §6
  (≈65.5%, DP cuts 10–28%) [10].
