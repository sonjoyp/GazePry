# D7 collection run sheet

Operator protocol for the recognition-probe study
([`GazePry_D7_Recognition_Knowledge_Direction.md`](GazePry_D7_Recognition_Knowledge_Direction.md)).
This is the document you keep open while running a participant.

**Status: no D7 data has been collected yet.** The first thing to run is the E1
mechanism pilot (§4 below). Its only question is *does RQ0 clear* — not "is the
effect big". If RQ0 does not clear, nothing downstream is worth collecting.

---

## 1. Before you start (once, not per participant)

### 1.1 Stop committing participant data — do this first

The repo currently tracks **44 real gaze sessions** in git, and the `.gitignore`
rules were commented out. They are now re-enabled, but **`.gitignore` only
governs untracked paths** — files already in the index keep being committed
until they are explicitly removed from it.

```bash
git rm --cached data/*.json          # stop tracking; files stay on disk
git status                           # confirm: deletions staged, disk untouched
git commit -m "chore: untrack participant gaze data before D7 collection"
```

This is not a history scrub. The sessions remain in past commits, so **before
any public artifact release** you still need `git filter-repo` (or BFG) and a
force-push. That is a separate, destructive decision — do not fold it into
collection prep.

Verify the guard works before trusting it:

```bash
git check-ignore -v data/anything.json labels/anything.json    # both must match
```

### 1.2 Environment check

```bash
npm test                 # JS + Python, must be green
npm run d7:verify        # effect dataset PASSes RQ0, null dataset correctly refuses
```

### 1.3 Stimuli

The task shows **real image files** from `public/stimuli/`, described by
`manifest.json`. From a clean checkout:

```bash
npm run d7:stimuli                          # design the packs; generate E1
export GAZEPRY_CONTACT="skpaul@tamu.edu"    # Wikimedia needs a contactable UA
npm run d7:stimuli:fetch                    # install the real E2 assets
npm run d7:stimuli:check                    # every file present and large enough
npm run d7:stimuli:verify                   # every file matches the lock hash
```

| Set | Ships as | Ready? |
|---|---|---|
| **E1** | 24 Julia-set fractals, mutually distinguishable by construction | **yes** |
| **E2** | 8 faces + 8 bank marks + 8 landmarks from Wikimedia Commons | **yes, once fetched** |
| **E3** | 8 everyday documents (vaccination card, census form, jury summons…) from Wikimedia Commons | **yes, once fetched — report separately, see caveat** |

E1 is deliberately abstract: its validity depends on the participant having **no
prior exposure**, so photographs of real things would smuggle in uncontrolled
familiarity that no counterbalancing removes.

**E2 is the opposite** — it measures familiarity the participant brought with
them, so it uses real faces, bank marks, and places. Arrays are drawn *within* a
class, never across, so a trial is four faces or four bank marks and the probe
cannot be picked out by category.

The task page **disables Begin** for a set that still contains placeholders. Do
not work around it: a cohort collected against stand-ins cannot be salvaged.

**Run `npm run d7:stimuli:verify` before the first participant of every session
block.** It is the only thing that catches a stimulus that changed between
cohorts, which would otherwise be invisible and unfixable in analysis.

**E3 is collectable but its construct is weaker in kind, not just degree** — its
cards probe topic exposure (semantic), not exposure to a specific image
(episodic), so report it separately with that caveat and never let an E3 number
support the mechanism claim. Free-licensing also left finance and legal at one
item each; treat them as illustrative, not a category comparison. See
[`public/stimuli/README.md`](public/stimuli/README.md), "E3: sourced, but read
this before treating it like E1/E2".

### 1.4 Consent and debrief copy

**D7 uses mild deception**: the cover task conceals that recognition is being
measured. That is standard in the CIT literature and necessary here (telling
participants converts every session into the RQ4 countermeasure condition), but
it obliges you to debrief. The study runs under the existing TAMU IRB-exempt
determination; the copy below is the operational implementation, not a new
protocol filing.

**Consent script (before the session)**

> This study looks at how people's eyes move while they browse ordinary web
> pages. Your webcam will be used to estimate where on the screen you are
> looking. **No video is recorded or transmitted** — only the coordinates of
> your estimated gaze point, plus your answers to a short questionnaire.
>
> You will look at a series of image panels and answer a simple question about
> each. It takes about 20 minutes. You can stop at any point, and you can ask me
> to delete your data afterwards without giving a reason.
>
> To keep the task natural, I will explain the specific research question at the
> end rather than now. Nothing you do can be right or wrong.

**Debrief script (after the session, mandatory)**

> Thanks. Here is what the study was actually measuring. When you look at
> something you have seen before, your eyes treat it differently from something
> new — you tend to look at it for a different length of time, and your
> individual fixations tend to be longer. That happens automatically and you
> cannot really control it.
>
> We were testing whether an ordinary web page, using nothing but a standard
> webcam, could work out **which of those images you had seen or used before** —
> without ever asking you. The point of the research is that this is a privacy
> problem: a website could learn what you recognise, and therefore something
> about your history, with no cookie and no click.
>
> I did not tell you this beforehand because knowing about it changes how people
> look at things, which is itself one of the conditions we test.
>
> Your data is a stream of gaze coordinates and your questionnaire answers,
> stored under your participant code with no name attached. **If you would
> rather we did not use it, tell me now or email later and I will delete it —
> no reason needed.** Any questions about what we found?

Record the debrief as delivered on the participant log. Note any withdrawal
request immediately and delete both the `data/` session and the `labels/` record.

### 1.5 Recruitment note

Recruit for demographic spread where you can. A narrow lab cohort makes it
harder to argue the effect is individual recognition rather than a shared
cohort-level familiarity with the same services — which matters most in E2.

---

## 2. Per-participant setup

Assign IDs **sequentially**: `P01`, `P02`, `P03`, … This is not cosmetic.
Counterbalance group is derived from the participant number, so sequential IDs
spread the cohort evenly across the four groups. Random or non-numeric IDs fall
back to a hash, group sizes drift apart, and item identity starts leaking into
familiarity — the exact thing the RQ0 saliency control exists to catch.

**Room setup**
- Maximise the browser window. The probe page refuses to run below 400×300 px
  tiles with 250 px gaps, which is the geometry the published webcam replication
  actually used. If Begin is disabled, the window is too small.
- Consistent, non-backlit lighting; no window behind the participant.
- Seat them at a normal viewing distance (~60 cm) and leave it there for the
  whole session.
- Record seating/lighting in the condition fields on the hub — you cannot
  reconstruct them later.

---

## 3. Session flow

```bash
node server.js
```

Open **http://localhost:8080** on the participant machine and
**http://localhost:8080/collect.html** on your own screen.

| # | Step | Notes |
|---|---|---|
| 1 | Consent script + questions | §1.4 |
| 2 | Hub: enter `P0n`, session `S1`, pick tracker, consent box | tracker = `webgazer` for the pilot |
| 3 | **Save & calibrate** | 9-point grid; redo if the participant reports drift |
| 4 | Rate calibration quality on the hub | feeds the confound controls |
| 5 | **Recognition probe** → set the design cell → Begin | see §4 for pilot settings |
| 6 | Check the completion card | `Clock anchored: yes`, trial count correct |
| 7 | **E2/E3 only:** open `questionnaire.html`, complete it | never before step 5 |
| 8 | Check the participant's row in `collect.html` | §5 — do this before they leave |
| 9 | Debrief script | §1.4, mandatory |

**Step 6 is a gate, not a formality.** If the card says `Clock anchored: NO`, no
gaze reached the recorder and the session is unscorable. Re-run it now.

---

## 4. The E1 mechanism pilot — run this first

Target **N ≈ 12**, one session each, ~20 minutes per participant.

| Setting | Value | Why |
|---|---|---|
| Experiment | `E1` | familiarity is installed in the lab, so ground truth is perfect |
| Array size | `2` | highest-signal condition; establish the effect before making it realistic |
| Cover task | `memory-adjacent` | the task demand reported as countermeasure-resistant |
| Awareness | `naive` | the covert setting the threat model assumes |
| Delay | `immediate` | runs the familiarisation phase in-session |
| Trials | `40` | ~6 minutes of array time |

Then score it:

```bash
cd analysis
python recognition.py --data ../data --experiment E1
```

**The pilot's decision rule.** RQ0 must clear: shuffled-label null ≈ 0.500,
saliency-only baseline ≈ 0.500, and the per-AOI AUC CI lower bound above 0.500.

- **Clears** → proceed to the full E1 (delay conditions, 4-tile arrays, the
  countermeasure arm), then E2.
- **Does not clear, saliency baseline high** → counterbalancing broke. Check IDs
  are sequential and groups are even before blaming the effect.
- **Does not clear, everything at chance** → the effect is not recoverable
  through this sensor at this geometry. Stop and reconsider the direction rather
  than collecting 40 participants of it.

Do not skip to E2. E2 is the headline but it is also the weakest link: real
familiarity cannot be assigned, so its counterbalancing is statistical rather
than structural, and it leans on E1 having already established the mechanism.

---

## 5. Quality gates

`collect.html` flags these automatically. Act on them **while the participant is
still present**.

| Flag | Meaning | Action |
|---|---|---|
| `no clock anchor` | no gaze samples reached the recorder | re-run now; check camera permission |
| `no trials recorded` | sequence aborted | re-run |
| `very few samples per trial` (<60) | tracker starved or window lost focus | re-calibrate and re-run |
| `over 40% gaps` | face repeatedly lost | fix lighting/seating, re-run |
| `needs questionnaire` | E2/E3 session with no labels filed | run `questionnaire.html` before they leave |

Sanity-check the first participant's mechanics before running the rest:

```bash
cd analysis
python -c "
import sys,json,glob; sys.path.insert(0,'.')
from aoi_features import extract_session
s=json.load(open(sorted(glob.glob('../data/*probe*.json'))[-1]))
rows=extract_session(s)
print('scorable AOI rows:', len(rows), 'of', s['nTrials']*s['arrayN'])
fam=[r['features']['dwell_prop'] for r in rows if r['familiar']]
unf=[r['features']['dwell_prop'] for r in rows if not r['familiar']]
print('mean dwell  familiar %.3f  unfamiliar %.3f' % (sum(fam)/max(1,len(fam)), sum(unf)/max(1,len(unf))))
"
```

If scorable rows are far below the total, trials are being dropped for too few
samples — that is a tracker problem, not an analysis problem.

**Watch `fixations per trial` in every `recognition.py` run.** Below 1.0 the
fixation-duration channel has collapsed and every fixation feature silently
reports AUC 0.500. The tool warns, but only if you read the line. If it fires on
real data, the I-DT dispersion threshold needs raising for your sensor before
any per-feature number means anything.

---

## 6. Data handling

| What | Where | Committed? |
|---|---|---|
| Gaze streams | `data/*.json` | **never** (gitignored) |
| Questionnaire labels | `labels/*.json` | **never** (gitignored, separate dir) |
| Participant log (code ↔ consent/debrief) | **paper or offline file** | never in this repo |

Labels live outside `data/` deliberately: service usage and topic exposure are
exactly the information the D7 attack claims to extract, so they are the most
sensitive thing the study holds. Keeping them in a separate directory means a
careless `git add data/` cannot sweep them in.

Never put a participant's name, email, or the code↔identity mapping in the repo.

---

## 7. Analysis after collection

```bash
cd analysis

# E1 — ground truth is the counterbalance assignment
python recognition.py --data ../data --experiment E1 --plot e1_k.png

# E2/E3 — ground truth is the questionnaire; the tool REFUSES without it
python recognition.py --data ../data --experiment E2 --labels ../labels --plot e2_k.png

# E2 per-class contrast: faces vs bank marks vs landmarks.
# The classes differ in visual detail and in how many times a familiar viewer
# has seen them, so the ordering is a result, and it is what tells an attacker
# which content types make a usable probe. It is also the fallback if the
# pooled E2 number underwhelms.
python recognition.py --data ../data --experiment E2 --labels ../labels --item-class face
python recognition.py --data ../data --experiment E2 --labels ../labels --item-class bank
python recognition.py --data ../data --experiment E2 --labels ../labels --item-class landmark

# RQ4: what an informed participant recovers
python recognition.py --data ../data --experiment E1 --awareness naive
python recognition.py --data ../data --experiment E1 --awareness countermeasure

# §7.1 contrast: does the effect survive hard AOI assignment?
python recognition.py --data ../data --experiment E1 --hard-aoi
```

Report the AUC **interval**, never the point estimate. The CI is bootstrapped
over participants, which is the correct unit — resampling rows would treat 40
trials from one person as 40 independent observations and produce an interval
far too tight to believe.
