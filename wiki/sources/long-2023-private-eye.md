---
type: source
tags: [paper, attack, content-dependent, screen-peeking, eyeglass-reflection]
aliases: [Long et al. 2023, Private Eye, eyeglass reflections screen peeking]
sources: [long-2023-private-eye]
reviewed: false
updated: 2026-07-11
---

Long, Yan, Xiao, Prasad, Xu, Fu (Michigan / Zhejiang) — *Private Eye: On the
Limits of Textual Screen Peeking via Eyeglass Reflections in Video
Conferencing*, **IEEE S&P 2023** — bibliography **[19]**. Recovers on-screen
text from **eyeglass reflections** captured by a webcam during video calls — a
content-*dependent* optical side channel, cited to delimit GazePry's scope.
(`raw/Private Eye...-2023.pdf`)

## Key facts

- Uses multi-frame super-resolution + optical modeling to reconstruct
  reflected screen content from a conferencing webcam; characterizes the
  recognizability thresholds as webcam resolution improves.
- A *screen-peeking* attack (reads what is on screen), the exact scenario the
  [[same-origin-policy]] blocks a web script from doing cross-origin — the plan
  uses it to argue the realistic web risk is re-ID, not content peeking.
- Adversary stronger/different (a video-call peer with a clear glasses
  reflection), not a drive-by web script.

## Related

- [[same-origin-policy]] — why content peeking is out of scope on the web.
- [[two-regimes-of-leakage]] — content-dependent regime.
- [[drive-by-web-adversary]] — contrast: GazePry's weaker web adversary can't
  do this.

## Mentions in sources

- Plan §2 (adversary contrast: eyeglass reflections), §18.7 [19]; protocol §15.7
  [19].
