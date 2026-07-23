# D7 stimulus packs

Real image files for the recognition-probe task, described by `manifest.json`.

```bash
npm run d7:stimuli          # design the packs + generate E1 and any placeholders
npm run d7:stimuli:fetch    # install the real E2 assets from Wikimedia Commons
npm run d7:stimuli:check    # validate the manifest against what is on disk
npm run d7:stimuli:verify   # offline: hash-check installed assets against the lock
```

| Set | Items | Ships as | Ready to collect? |
|---|---|---|---|
| **E1** | 24 | Julia-set fractals, generated here | **Yes** |
| **E2** | 24 | 8 faces + 8 bank marks + 8 landmarks, fetched from Commons | **Yes, once fetched** |
| **E3** | 8 | Everyday documents (vaccination card, census form, jury summons…), fetched from Commons | **Yes, once fetched — with the construct caveat below** |

The task page **blocks** a set while any of its items is marked
`"placeholder": true`. That is deliberate rather than a warning: E2 and E3
measure familiarity the participant brought with them, so a cohort run against
stand-ins produces data that cannot be salvaged, and by the time anyone reads a
warning the participants have gone home.

---

## The two scripts, and why they are two

`scripts/make_stimuli.py` is the **design**: which items exist, what class and
expected-penetration tier each one has, and the counterbalancing invariants they
have to satisfy. It generates E1 in full and writes obvious placeholders for
E2/E3 so the harness runs and the tests pass from a clean checkout.

`scripts/fetch_stimuli.py` is the **sourcing**: it resolves each E2 item to a
freely-licensed Wikimedia Commons file, downloads it, and marks it real in the
manifest.

Run them in that order. Re-running `make_stimuli.py` **keeps** assets that
`fetch_stimuli.py` already installed (`--force-placeholders` overrides), and
sweeps images the item table no longer references.

---

## Why E1 is generated and E2 is not

E1's validity depends on the participant having **no prior exposure**, so that
familiarity is created only by the study phase and the ground truth is exact.
Photographs of real things fail that test — everyone has seen a beach, a dog, a
keyboard — and the "novel" items would carry uncontrolled pre-existing
familiarity that no counterbalancing can remove. Richly detailed *novel abstract*
images are the standard stimulus class for recognition-memory work for exactly
this reason.

The generator enforces two properties that a naive fractal dump does not have:

- **Detail.** Escape-time is histogram-equalised and the interior is coloured by
  an orbit trap, because the obvious mapping produces a dark image with a thin
  bright rim — low variance and little for a participant to actually recognise.
- **Mutual distinctiveness.** Every pair is checked in *colour* to differ by at
  least 22 mean absolute RGB levels, and candidates are resampled until that
  holds. If a "novel" tile looks like one the participant studied, the
  familiarity contrast is contaminated in a way counterbalancing cannot undo.
  The achieved minimum is recorded as `minPairDistance` in the manifest.

E2 measures *naturally acquired* familiarity, so it needs the real thing.

---

## E2: three classes, and why arrays never mix them

| Class | 8 items | Why it is in the set |
|---|---|---|
| `face` | Public figures, globally to professionally famous | The stimulus class the whole ocular-CIT literature uses; maximum visual detail |
| `bank` | Retail-bank and payment wordmarks | The closest analogue to the history-sniffing payload: *which financial services do you use* |
| `landmark` | Widely photographed places, universal to regional | High-detail photographs whose exposure varies by travel and background rather than by account ownership |

**Arrays are drawn within a class.** A trial showing one face among three bank
marks would let the probe be identified by *category* rather than by familiarity,
and would add category-driven saliency variance to a contrast that is otherwise
between four visually comparable tiles. This is what `"arrayGroupBy": "class"`
in the manifest means, and both the browser protocol and the Python port enforce
it.

Two invariants the checker will not let you break:

- **A class must be a contiguous block in the item table**, and its size must be
  a multiple of the four counterbalance groups. The Latin square runs over the
  global item index, so a block of eight splits exactly 4 familiar / 4 unfamiliar
  for *every* group, which is what guarantees each class can always fill a 4-tile
  array. Violate it and a trial fails to build mid-session rather than at startup.
- **Faces and marks carry no on-tile caption.** A caption would let the
  participant read the name instead of recognising the image, which is a
  different memory system from the one the effect rests on. The `name` field is
  for the questionnaire, the operator log, and the attribution file only.

Tiers (`high` / `medium` / `low`) record your *expectation* about the cohort and
drive the "high-salience items only" fallback analysis. They are a hypothesis,
not a label: the ground truth is always the post-hoc questionnaire.

---

## Sourcing, licensing, and provenance

`sources.json` says which person, brand, or place each item denotes.
`stimuli.lock.json` records what was actually resolved: the Commons file, its
licence and author, the SHA-256 of the bytes written, and the date.
`ATTRIBUTION.md` is regenerated from the lock on every fetch.

```bash
export GAZEPRY_CONTACT="skpaul@tamu.edu"   # Wikimedia requires a contactable UA
npm run d7:stimuli:fetch
```

**Only free licences.** Every asset is checked against an allow-list (public
domain, CC0, CC BY, CC BY-SA, FAL) using the licence Commons itself reports.
Anything else is refused and **not downloaded**. Most retail-bank wordmarks
qualify because a plain wordmark is below the threshold of originality for
copyright. If an item you want is not free, choose a different item — do not
relax the check.

This is a **copyright** test only. Displaying a mark to identify the service it
denotes is normally nominative use, but that is a judgement for you and your
institution, not something this README or that script settles.

**Reproducibility.** A later fetch reuses the file pinned in the lock, so a
Wikipedia lead image changing under you does not silently change the stimulus
set. `--relock` re-resolves deliberately. `--verify` re-checks the hashes
offline, and is part of the pre-collection checklist: two cohorts collected
months apart provably saw the same stimuli, or you find out.

**Presentation uniformity.** Wordmarks have wildly different aspect ratios;
dropped straight into a 4:3 tile the browser would scale each to a different
apparent size, which is an item-saliency difference dressed up as a stimulus.
Marks are composited at the same margin onto the same canvas, so the only thing
varying across a bank array is which bank it is. Photographs are installed at
their own aspect and the tile is held at 4:3 by `ProbeProtocol.layout()`, so the
stimulus **fills the whole tile** (`object-fit: cover`) — the largest the sensor
geometry allows.

The catch is the face photos: they are portrait, so a *centred* cover crop of a
960 × 1440 portrait keeps the middle band — a collar — and throws the face away,
which looks like data and is not. The crop is therefore anchored per item by the
manifest **`focus`** field (a CSS `object-position`). `make_stimuli.py` sets
`focus: "50% 0%"` on every `face` so the crop is taken from the top edge, where
the head is; banks and landmarks carry no `focus` and stay centred. This is
class-level because "top" is safe for any head-and-shoulders portrait. Server-side
cropping is not an option here — the faces are JPEGs and the decoder in these
scripts is PNG-only — so the crop happens in the browser.

The consequence for sourcing: **prefer head-and-shoulders framing over a
full-length shot**, so the face is a large share of the frame the top crop keeps.
A distant or off-centre face will be small or clipped; the fix is a better source
file. If one portrait genuinely needs a different anchor, change it in
`make_stimuli.py` (the design owns `focus`, and re-running the generator restamps
it) rather than editing the manifest by hand, which the next regenerate would
overwrite.

**Requirements for any asset:** at least 600 × 450 px (below that it is upscaled
into the tile and loses the detail recognition depends on). The fetcher enforces
this and refuses rather than installing something too small.

---

## What gets committed

`.gitignore` excludes the `e2/` and `e3/` image files. They are third-party
material, and while the licences permit redistribution, keeping them out of a
GPLv3 repo avoids muddling the licensing of the code with the licensing of the
stimuli.

| | Committed? |
|---|---|
| `manifest.json`, `sources.json`, `stimuli.lock.json`, `ATTRIBUTION.md` | **yes** — your design and its provenance |
| `e1/` images | **yes** — generated here, reproducible from recorded seeds, no third-party rights |
| `e2/`, `e3/` images | **no** — fetch them with `npm run d7:stimuli:fetch` |

A clean checkout therefore reproduces the whole pack with two commands and no
manual asset hunting.

---

## E3: sourced, but read this before treating it like E1/E2

E3 now ships **8 real documents** and is collectable once fetched, but its
construct is deliberately kept at arm's length from E1/E2 and the material was
chosen against a stricter bar than "depicts a familiar topic."

**The construct is weaker than E1/E2's, in kind and not only in degree.** E1 and
E2 rely on the participant having seen *that stimulus*, which is what the
eye-movement memory effect actually predicts. A topic card the participant has
never seen before cannot carry an episodic trace no matter how familiar the topic
is; what it can carry is *semantic* familiarity with the subject matter. That is
a real result if reported as one, and a misleading one if folded in with E1/E2 —
so **report E3 separately, with the episodic-versus-semantic caveat stated, and
do not let an E3 number support the mechanism claim.**

**What a valid E3 asset is, and what the eight are.** Something a person
plausibly **handled**, not merely something that depicts a familiar subject. The
shipped set is a COVID-19 vaccination card, an FDA nutrition-facts label, a CDC
"wash your hands" poster (health); a 2020 US Census form, an "I Voted" sticker, a
recycling poster (civic); a jury summons (legal); and a payslip (finance).

**Why 8 and not 16, and why the lopsided split (3 health / 3 civic / 1 legal /
1 finance).** A valid E3 asset has to be freely licensed *and* on Wikimedia
Commons, since that is all the fetcher will pull. Commons has canonical free
versions of the health and civic documents but **not** of the modern US finance
and legal forms — a current IRS 1040, a W-2, a Miranda card are all public-domain
federal works that simply have not been uploaded there. Finance and legal are
therefore present but **too thin (n=1) to carry a per-category claim**; treat
them as illustrative, not as a category comparison. Closing that gap means either
uploading those PD forms to Commons first, or extending the fetcher to accept
direct `.gov` sources.

**Scope.** Keep to health, finance, legal, and civic. **Do not add protected
characteristics** (sexual orientation, religion, immigration status): the method
would apply, the demonstration does not need them, and including them turns a
privacy paper into an ethics problem. A JS test and a Python test both assert the
shipped E3 categories, so adding one will fail the suite.

To change the E3 set, edit its items in `scripts/make_stimuli.py` (design) and
the `E3` block of `sources.json` (sourcing) together, then re-run the generator
and the fetcher — the same two-step flow as E2.
