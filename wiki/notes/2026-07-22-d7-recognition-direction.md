---
type: note
tags: [note, d7, recognition, direction, literature, non-biometric]
date: 2026-07-22
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

# 2026-07-22 — D7 chosen as the non-biometric direction; the ocular CIT is the instrument

Session goal: pick a **non-biometric** gaze-leakage direction for the webcam
harness that is practical at the project's real scale and publishable. Outcome:
a new vector, **D7 recognition & concealed-knowledge leakage**
([[recognition-knowledge-leakage]]), drafted as
`GazePry_D7_Recognition_Knowledge_Direction.md`
([[d7-recognition-knowledge-direction]]), plus ten new source pages.

## What was decided, and why the alternatives lost

Four non-biometric options were weighed against the existing taxonomy
([[leakage-vectors-d1-d6]]):

| Option | Outcome |
|---|---|
| **D1** PIN/keypad inference on desktop webcam | **Ruled out.** Needs sub-degree pointing on packed AOIs — [[thilderkvist-2024-limitations]] is the direct counterexample, and [[eyetell]] / [[gazerevealer]] already own the framing. |
| **D3** cognitive/affective state | **Ruled out.** [[hutt-2024-mind-wandering]] [22] already did webcam mind-wandering; the privacy reframe alone is thin for a security venue. |
| **D5** demographics on desktop | **Ruled out.** Derivative of [[alsakar-2025-handheld-privacy]] [10] and needs the large N the project does not have. |
| **D7** recognition / prior exposure | **Chosen.** Empty cell, coarse-AOI tolerant, works at N ≈ 40 in one session. |

Note this is *in addition to* the existing [[reading-search-intent-leakage]] (D2)
direction, which was already drafted 2026-07-16 and is not superseded. D2 and D7
are different tenses of the same content-dependent regime: D2 leaks what the
visitor is examining **now**, D7 leaks what they knew **before arriving**.

## The load-bearing reason D7 was picked over pressing on with D4

D7 **structurally cancels the confound that gates D4**. The D4 plan's RQ0 asks
"the person, or the apparatus?" ([[reid-confound-controls]]), and
[[pilot-empirical-status]] records N=2 with no true cross-session separation and
a capture-rate confound correlated with identity. The D7 effect is a
**within-participant, within-trial contrast between AOIs on the same screen**, so
calibration geometry, lighting, seating, tracker identity, and logging cadence are
*constant across the units being compared* and cannot manufacture the effect. With
item-level counterbalancing (each item familiar for half the participants),
saliency and position are orthogonal to the contrast by construction. Consequence:
**N ≈ 40, one session** instead of N ≥ 50 with ≥1-week separation.

## Evidence gathered (all verified by publisher metadata / PMC full text on 2026-07-22)

The mechanism ([[eye-movement-memory-effect]]) and the instrument
([[ocular-concealed-information-test]]) are both mature; only the *attack framing*
is missing.

- [[althoff-1999-eye-movement-memory-effect]] — prior exposure changes sampling,
  **within the first five fixations**. Short observation window is viable.
- [[hannula-2010-worth-a-glance]] — the effect **does not require conscious
  recollection**. This is the "leak, not disclosure" claim.
- [[schwedes-2012-revealing-glance]] — six-face arrays; fixation duration revealed
  memory **regardless of intent to conceal**; 65% of relevant trials.
- [[nahari-2019-concealed-familiarity]] — n=61, **four-face parallel arrays**;
  task demands decide suppressibility; memory-dependent tasks resist
  countermeasures. Source of D7's cover-task manipulation.
- [[millen-2019-concealed-face-recognition]] — **AUC 0.67–0.87**; under
  countermeasures the fine spatial signal collapsed (d 1.40 → −0.12) while mean
  fixation duration **strengthened** (d 0.66 → 0.91). Source of the
  temporal-vs-spatial feature split and of RQ4/RQ5.
- [[zangrossi-2024-aiat-eye-movements]] — 75% from the eye measure alone on
  **week-old** memories.
- [[rosenzweig-2020-mock-terror]] — 88% / AUC 0.84, but via **microsaccades at
  RSVP rates**. Filed explicitly as an **IR ceiling that a ~30 Hz webcam cannot
  reach**, so it is never mistaken for a design template.

**The feasibility keystone** is a paper the wiki already had but had not been read
for this purpose: [[van-der-cruyssen-2024-validation]] replicated the **novelty
preference** — i.e. the recognition effect itself — online with WebGazer.js
(n=45), effect sizes shrinking **20–27%**, with a working stimulus geometry of
**472 × 331 px images 295 px apart**. That page has been deepened with the full
verified citation (*Behavior Research Methods* 56(5), 4836–4849, 2024,
doi 10.3758/s13428-023-02221-2) and now anchors D7 §6.2.

## The reframe, and the inversion that makes it a security paper

Browsers killed `:visited` history sniffing at the rendering layer
([[weinberg-2011-history-sniffing]] [5]). D7 reinstates the capability one layer
below, **where the side channel is the user rather than the renderer**.

The inversion worth keeping: the entire countermeasure literature that bounds the
forensic CIT assumes a subject who **knows they are being tested**. A drive-by web
visitor ([[drive-by-web-adversary]]) does not. **The covert setting is strictly
easier than the interrogation room** — and D7's RQ4 is designed to put a number on
that advantage.

## Risks recorded (do not lose these)

1. **Scoop risk, high.** Van der Cruyssen, Ben-Shakhar, Pertzov & Verschuere hold
   *both* the CIT expertise ([[nahari-2019-concealed-familiarity]]) *and* the
   webcam validation ([[van-der-cruyssen-2024-validation]]). They are one
   reframing away. Their venues are psychology/forensic, not security. Move on the
   E1 pilot rather than waiting for a large N.
2. **E2 is weaker than E1.** Lab-installed familiarity is a strong manipulation;
   "has an account on this site" cannot be *assigned*, so E2's counterbalancing is
   statistical rather than structural. This is the honest gap in the direction.
3. **Sign instability.** Familiarity yields *preference* in some paradigms and
   *avoidance* in others ([[nahari-2019-concealed-familiarity]] reports avoidance),
   and early vs late windows can differ. Pre-register per-window directional
   predictions; averaging across the reversal can null a real effect.
4. **Three citations remain unverified** — Lancry-Dayan 2018 [C6], Van der
   Cruyssen 2024 CIT-leakage [C7], and [[et-privacy-decade-review-2025]] [P1]
   (ACM DL returned 403; **author list unknown**). The D7 §3 gap claim must not
   rest on [P1] until the PDF is read.

## Immediate consequence for the code

D7 needs four new pieces on top of [[capture-harness]] / [[analysis-pipeline]]:
a probe-array task page ([[task-suite]] gains a sixth page), an **I-DT
dispersion-threshold** fixation detector (the existing I-VT is too coarse at
webcam rates and fixation *duration* is the load-bearing feature — this is the
second half of what [[thilderkvist-2024-limitations]] contributes), a
soft-assignment AOI feature extractor, and a per-trial/per-user classifier. The
[[simultaneous-capture-rig]] and every tracker adapter carry over unchanged.

**Next action:** verify the four outstanding citations, deep-read [C1]–[C5], then
run E1 at N ≈ 12 with the single question *does RQ0 clear?*
