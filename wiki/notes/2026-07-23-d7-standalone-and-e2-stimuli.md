---
type: note
tags: [note, d7, recognition, stimuli, sourcing, methodology, gotchas, bibliography]
date: 2026-07-23
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-23
---

# 2026-07-23 — D7 made standalone, and E2 stimuli sourced for real

Follow-on to [[2026-07-22-d7-instrumentation-findings]]. Two jobs in one
session: make the D7 document independent of the other two direction plans, and
close the stimulus gap that note left open ("real E2/E3 assets are not
installed, so only E1 can currently be run").

**E2 is now collectable. E3 is still blocked, and the reason changed** — it is
no longer a sourcing problem, it is a construct problem (§5). That asymmetry is
the most consequential thing in this note. Still **no human D7 data**.

## 1. The D7 document is standalone, and its citation numbers are now local

[[d7-recognition-knowledge-direction]] previously opened as a "companion to"
[[reid-research-plan]] and [[d2-reading-search-intent-direction]], compared
itself to D2/D4 throughout, and drew its bracket citations from the shared
bibliography in plan §21. It now stands alone: apparatus, ethics, and
data-hygiene sections describe their own requirements instead of pointing
elsewhere, and §2 contrasts the vector against *classes* of gaze attack
(keystroke inference, intent profiling, gaze biometrics, trait inference)
rather than against sibling plans.

**The trap this creates.** The document now carries its own complete
bibliography, renumbered **[1]–[30], local to that file**. These numbers do
**not** match the shared project numbering. The collisions are live and
misleading rather than obviously wrong:

| Bracket | In `GazePry_ReID_Research_Plan.md` §21 | In the D7 document |
|---|---|---|
| [5] | Weinberg 2011, history sniffing | Nahari et al. 2019, concealed familiarity |
| [6] | Liebling & Preibusch 2014 | Millen & Hancock 2019 |
| [8] | Wang et al. 2020 | Zangrossi et al. 2024 |
| [16] | *(unrelated)* | Weinberg 2011, history sniffing |

This is the same shape of hazard [[SCHEMA]] already documents for
`raw/related-papers.txt`, so it has been recorded there in the same place.
Wiki pages continue to cite the **shared** numbering; a claim traced to the D7
document must be resolved by author-year, never by carrying its bracket number
across.

The doc-local `[M1]`/`[C1]`/`[W1]`/`[P1]` labels the prior draft used are gone
from both the document and the code comments that quoted them.

## 2. E2 is now 24 real items in three classes of eight

E2 measures familiarity the participant brought with them, so it needs the real
thing. It now ships:

| Class | 8 items | Why this class |
|---|---|---|
| `face` | Obama, Swift, Messi, Merkel, Ardern, Thunberg, Miyamoto, Strickland | The stimulus class the whole [[ocular-concealed-information-test]] literature uses; maximum visual detail |
| `bank` | Chase, Bank of America, Wells Fargo, Citi, HSBC, Barclays, Santander, Nordea | The closest analogue to the [[weinberg-2011-history-sniffing]] payload: *which financial services do you use* |
| `landmark` | Eiffel Tower, Statue of Liberty, Taj Mahal, Colosseum, Sydney Opera House, Pena Palace, Sigiriya, Dragon Bridge (Ljubljana) | High-detail photographs whose exposure varies by travel and background rather than by account ownership |

Each class deliberately spans universal to niche recognition (Obama vs
Strickland; Chase vs Nordea; Eiffel Tower vs Sigiriya). Without that spread the
"familiar" label is a cohort constant rather than an individual fact — see §7.

All 24 fetched and verified from Wikimedia Commons. The eight bank wordmarks
all came back **Public domain** (a plain wordmark is below the threshold of
originality); faces and landmarks are mostly CC BY-SA, two CC0, two public
domain.

## 3. Arrays must be class-homogeneous, and that is a protocol change

A trial mixing one face with three bank marks lets the probe be identified by
**category** rather than by familiarity, and injects category-driven saliency
variance into a contrast that is otherwise between four visually comparable
tiles. The published ocular-CIT arrays are all-faces for this reason.

The trial builder now draws irrelevants from the probe's own class when the set
declares `arrayGroupBy` (E2 does; E1 and E3 do not, being visually homogeneous
already). Changed in `public/probe-protocol.js` and `analysis/probe_protocol.py`
in the same commit, as the parity tests require.

**The invariant this exposed, which is not obvious.** The counterbalancing Latin
square runs over the **global** item index (`isFamiliar(i, g) = ((i+g) mod 4) <
2`). A class therefore has to be a **contiguous block whose size is a multiple
of `N_GROUPS`**, or some counterbalance group ends up with too few unfamiliar
items in that class to fill a 4-tile array. Eight contiguous items split exactly
4 familiar / 4 unfamiliar for every group, which is why the classes are eight.

The failure mode if violated is the bad kind: `buildTrials` throws **mid-session
for one participant in one group**, not at startup and not for the operator who
tested it. Now enforced by `make_stimuli.py --check` and pinned by a test on
each side that walks every group × class.

## 4. Two sourcing dead ends, and one gotcha

Recorded because each cost a cycle and each will re-appear the moment anyone
sources E3.

**Wikipedia lead images work for people and places; they do not work for
brands.** Resolving an article to its lead image via the `pageimages` API gave
free, usable portraits for 12/12 people tried and photographs for 14/14 places.
For banks it returns **headquarters buildings**: `Bank of America` → *Bank of
America Corporate Center*, `HSBC` → *8 Canada Square*, `Chase Bank` → a
*footprint map*, and `Citibank` has no lead image at all. Brand marks have to be
named as explicit Commons files.

**Commons free-text search does not find topic photographs.** Searching for E3
material returned digitised books, not images: "therapy counselling session two
people" → four PDFs of a drug-addiction therapy manual; "dermatologist skin
examination" → DjVu scans of 19th-century dermatology texts; "person sleeping
bed night" → two novels and a play. Targeted queries for *documents* did work
(IRS Form 1040, FDA nutrition label, sample ballots), which is the lead worth
following if E3 is ever sourced.

**MediaWiki snaps `iiurlwidth` to standard thumbnail buckets.** Requesting 720
px and 900 px both returned **960 px**. The letterbox compositor trusted the
requested width and every one of the eight logos failed with "does not fit a
900×675 canvas". The fix is to fit in code against what actually arrived rather
than against what was asked for. Any pipeline that assumes a requested
thumbnail width is honoured will break the same way.

## 5. E3 stays blocked, and the reason is now a construct problem

[[2026-07-22-d7-instrumentation-findings]] treated E2 and E3 symmetrically:
both "need real logos, screenshots, and topic cards". **They are not
symmetric**, and this note supersedes that framing.

E1 and E2 rest on the participant having seen *that stimulus*, which is what
the [[eye-movement-memory-effect]] actually predicts — a bank wordmark or a
famous face is something a familiar viewer has genuinely encountered many times.
A **topic card** is not. A card about mortgages that the participant has never
seen before carries no episodic trace no matter how familiar mortgages are to
them; what it can carry is *semantic* familiarity with the subject matter, which
is a different memory system from the one the whole direction rests on.

So E2's gap was closable by sourcing and E3's is not. E3 remains on placeholders
and the task page keeps refusing it. The bar a valid E3 asset has to clear is
recorded in `public/stimuli/README.md`: something a person plausibly
**encountered before** (standard government forms, public-information posters,
recognisable article-card formats), not merely something depicting a familiar
subject. The construct caveat belongs in the paper regardless of what is
sourced, and is now stated in the document rather than implied.

**Separately: E3 was shipping an item the document forbade.** `t_imm` ("Visa
paperwork") had been in the set since the pack was written, while both the plan
and the stimulus README say immigration status is out of scope as a protected
characteristic. The scoping test did not catch it because it asserts the
*category* vocabulary (health / finance / legal / civic) and `t_imm` was
categorised `legal`. Replaced with `t_claims` ("Small claims court"). The lesson
generalises: a test over a controlled vocabulary does not constrain what is put
into each bucket.

## 6. Provenance is machine-enforced, not a discipline

Three properties of `scripts/fetch_stimuli.py`, because "remember to record
where the image came from" does not survive contact with a deadline:

- **Licence gating.** Every asset is checked against a free-licence allow-list
  (public domain, CC0, CC BY, CC BY-SA, FAL) using the licence Commons itself
  reports; anything else is **refused and never downloaded**. A fair-use logo
  cannot enter a GPLv3 repo intended for release by accident.
- **A lock file.** `stimuli.lock.json` pins the resolved Commons file, its
  licence and author, and the **SHA-256 of every byte written**. Lead images
  change under you, so without this two cohorts collected months apart could
  have seen different stimuli with nothing to reveal it. `--verify` re-checks
  the hashes offline and is now a pre-collection step in the run sheet.
- **Generated attribution.** `ATTRIBUTION.md` is rebuilt from the lock on every
  fetch, so the CC BY / CC BY-SA credit list cannot drift from what is on disk.

`sources.json` (intent), the lock, the manifest, and the attribution are
committed; the `e2/`/`e3/` images are not. A clean checkout reproduces the pack
with two commands.

Wordmarks are composited onto a shared canvas at a common margin. This is a
methodological control, not cosmetics: aspect ratios vary from 322×53 to
302×302, so dropped raw into a 4:3 tile the browser would render each at a
different apparent size — item saliency dressed up as a stimulus, inside the one
contrast the design cannot afford to contaminate.

## 7. Cohort-level familiarity is now the top threat to the headline

Naming it because the E2 sourcing brought it into focus and the document now
carries it as a high-severity risk. If every participant is a US student, the
same bank marks are familiar to all of them, and what reads as *individual*
recognition is a cohort constant. The mitigations available are (a) item classes
spanning nationality, which is why the set holds Nordea and Barclays alongside
Chase, and regional landmarks alongside the Eiffel Tower, (b) recruiting for
demographic spread, and (c) reporting the per-class variance in the self-report
labels as evidence the contrast actually varies *within* the cohort. (c) costs
nothing and should be reported whatever the headline says.

## Verification state

- `npm test` — **162 pass, 0 fail** (74 JS + 88 Python), 2026-07-23. Up from
  147; the new tests cover class-homogeneous arrays, the group × class fill
  invariant, provenance fields on real items, the licence gate, the PNG
  round-trip, and lock tampering.
- `npm run d7:verify` — effect dataset PASSes RQ0, null dataset correctly FAILs.
  Unchanged by this session's work.
- `npm run d7:stimuli:check` — 3 sets, 64 items, all files present, 1 warning
  (E3 placeholders, expected).
- `npm run d7:stimuli:verify` — 24 locked assets present and unmodified.
- Served over HTTP and checked end to end: manifest, a fetched JPEG, a
  composited logo, the probe page, and the questionnaire.

## Open items this note does not resolve

- **Data hygiene, still blocking collection.** Still **44** real gaze sessions
  tracked in git. Unchanged from [[2026-07-22-d7-instrumentation-findings]];
  untracking is a git-index operation left to a human.
- **E3 unsourced**, deliberately (§5).
- The four unverified citations are still unverified — now numbered [9], [10],
  [15], [17] in the D7 document's local scheme (previously [C6], [C7], [W5],
  [P1]).
- Every D7 number remains synthetic. The E1 pilot (N ≈ 12) still asks one
  question: *does RQ0 clear on real eyes?*
- Outside D7's scope but noticed: `README.md`'s header points at
  `GazePry_Direction1_ReID_Study_Protocol.md` and
  `GazePry_Information_Leakage_Report.md`, which live in `raw/` and not at the
  repo root, so both links are dead.

## Related

- [[2026-07-22-d7-instrumentation-findings]] — the prior note; §5 here
  supersedes its "E2 and E3 both just need real assets" framing.
- [[2026-07-22-d7-recognition-direction]] — the direction decision both notes
  implement.
- [[recognition-knowledge-leakage]] — the concept page, updated with E2's status
  and the class-homogeneity control.
- [[ocular-concealed-information-test]] — the all-faces array convention §3
  follows.
- [[eye-movement-memory-effect]] — the episodic mechanism §5 argues a topic card
  cannot engage.
- [[SCHEMA]] — the citation-numbering trap §1 creates is recorded there.
