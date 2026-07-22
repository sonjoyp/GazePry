---
type: concept
tags: [concealed-information-test, forensic, d7, paradigm, countermeasures]
aliases: [Ocular CIT, Concealed Information Test, eye-movement CIT, concealed familiarity detection, CIT]
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

The **ocular Concealed Information Test** is the forensic paradigm that turns the
[[eye-movement-memory-effect]] into a *test*: present a probe item among
irrelevant items and decide, from gaze, whether the viewer recognizes the probe.
It is the instrument [[recognition-knowledge-leakage]] (D7) repurposes as a covert
web attack. The paradigm's central preoccupation — **countermeasures** — is
precisely what the web setting removes.

## Key facts

- **Typical design:** a small array of items (four faces in
  [[nahari-2019-concealed-familiarity]], six in
  [[schwedes-2012-revealing-glance]]) or sequential single items
  ([[millen-2019-concealed-face-recognition]]), with dwell time, visit counts,
  fixation counts, and fixation durations as the measures. Coarse, well-separated
  AOIs — which is why the paradigm ports to a webcam at all.
- **Performance scale (research-grade IR):** per-item **AUC 0.67–0.87**
  [[millen-2019-concealed-face-recognition]]; concealed knowledge detected in
  **65% of relevant trials** [[schwedes-2012-revealing-glance]]; **75%** from the
  eye measure alone on week-old memories [[zangrossi-2024-aiat-eye-movements]].
  The high-water mark is **88% / AUC 0.84** [[rosenzweig-2020-mock-terror]] — but
  that rests on **microsaccades at RSVP rates**, needs 500–1000 Hz sampling, and
  is **categorically unreachable** on a ~30 Hz webcam.
- **Countermeasures are the paradigm's binding limitation.**
  [[nahari-2019-concealed-familiarity]]: in a *visual detection* task,
  countermeasure instructions succeeded; in a *short-term memory* task, avoidance
  of the familiar face persisted **even under explicit instruction to conceal**.
  Conclusion: tasks that encourage differential gaze behaviour resist
  countermeasures.
- **What survives concealment is temporal.** Fixation duration reveals memory
  regardless of intent [[schwedes-2012-revealing-glance]] and *strengthens* under
  a fixed-sequence countermeasure ([[millen-2019-concealed-face-recognition]],
  d = 0.66 → 0.91) while the fine spatial signal collapses (d = 1.40 → −0.12).
- **The D7 inversion:** every result above assumes a subject who **knows they are
  being tested**. A drive-by web visitor ([[drive-by-web-adversary]]) does not, so
  the attack operates in the naive regime where effects are largest. **The covert
  setting is strictly easier than the forensic one** — stated in
  [[d7-recognition-knowledge-direction]] §4 as the threat model's core point.
- **The community is already moving to the webcam.**
  [[van-der-cruyssen-2024-validation]] shares two authors with
  [[nahari-2019-concealed-familiarity]] and adds Verschuere; they have both the
  CIT expertise and the browser validation. This is the D7 scoop risk.

## Related

- [[eye-movement-memory-effect]] — the underlying phenomenon.
- [[recognition-knowledge-leakage]] — the D7 direction that weaponizes this.
- [[ceiling-vs-commodity]] — the IR-vs-webcam framing D4 uses for identity and D7
  reuses for recognition.
- [[gaze-perturbation-defense]] — must be tested against the *temporal* channel,
  not just spatial coarsening.
- [[eyetell]], [[gazerevealer]] — the contrast class: content-dependent attacks on
  a secret being **entered**, versus D7's attack on a memory already **held**.

## Mentions in sources

- `GazePry_D7_Recognition_Knowledge_Direction.md` §1, §3, §4, §9.2.

## Open questions

- All five anchor papers are summarized from PMC full text or publisher metadata,
  **not** full-PDF reads. Effect directions, exact scoring windows, and
  per-measure AUCs must be taken from the papers' own tables before D7
  pre-registration (D7 doc §12 step 2).
- Two further CIT citations remain **unverified**: Lancry-Dayan et al. 2018 [C6]
  and Van der Cruyssen et al. 2024 on mock-crime detail leakage [C7].
