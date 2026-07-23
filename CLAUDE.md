# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

GazePry is a security/privacy research project on information leakage from
webcam eye tracking. It is research-grade code, but reproducibility is a
requirement: see [`wiki/entities/gazepry.md`](wiki/entities/gazepry.md).

## Commands

```bash
node server.js                 # harness on http://localhost:8080 (npm start too)
node server.js --port 9000 --data ./data --labels ./labels

npm test                       # JS (node:test) + Python (unittest) — keep green
npm run test:js
npm run test:py

node --test test/idt.test.js                              # one JS file
node --test --test-name-pattern "counterbalance" test/*.test.js
node scripts/run-python.js analysis/test_analysis.py TestStimulusPack   # one Python class

npm run d7:verify              # D7 end-to-end: effect dataset PASSes RQ0, null refuses
npm run d7:stimuli             # design the packs; regenerate E1 + placeholders
npm run d7:stimuli:fetch       # install real E2 assets from Wikimedia Commons
npm run d7:stimuli:check       # validate the stimulus manifest against disk
npm run d7:stimuli:verify      # offline: assets still match their lock hashes
```

There is no build step and no lint config. Offline analysis:
`cd analysis && pip install -r requirements.txt && python reid.py --data ../data`
(D4) or `python recognition.py --data ../data --experiment E1` (D7).

**Use `scripts/run-python.js`, not a bare `python3`**, in anything committed —
it resolves `python3`/`python`/`py` across platforms and propagates the exit
code unchanged so a failure is never masked.

## Architecture

### Two research directions share one harness

- **D4, cross-site re-identification** — `reid-core.js` + `analysis/reid.py`.
  Unit of analysis is the *session pair*; leaks identity.
- **D7, recognition & concealed-knowledge probe** — `public/probe-protocol.js` +
  `analysis/recognition.py`. Unit of analysis is the *AOI within a trial*; leaks
  what the visitor has seen before. See
  [`GazePry_D7_Recognition_Knowledge_Direction.md`](GazePry_D7_Recognition_Knowledge_Direction.md)
  and [`D7_COLLECTION_RUNSHEET.md`](D7_COLLECTION_RUNSHEET.md).

They coexist in `data/` and are told apart by `session.schema`
(`gazepry.probe.v1` marks a D7 session). `server.js` deliberately excludes probe
sessions from the re-ID gallery — do not remove that guard.

### Every algorithm exists twice, in JS and Python

`reid-core.js` ↔ `analysis/features.py`, and `public/probe-protocol.js` ↔
`analysis/probe_protocol.py`. The browser needs the live demo; the analysis
needs the offline numbers. **Three parity tests** hold them together: the JS
side is exposed through thin CLIs (`test/features-cli.js`, `test/idt-cli.js`,
`test/probe-plan-cli.js`) that `analysis/test_analysis.py` shells out to and
compares against the Python result.

If you touch a feature, a threshold, or the trial protocol, change **both
sides in the same commit** — the parity tests will fail otherwise, and that is
the point. The PRNG is reproduced bit-identically in Python via explicit uint32
masking, so arithmetic changes there are especially load-bearing.

### Pluggable tracker adapters

`public/gazepry-tracker.js` is a tracker-agnostic orchestrator (identity,
calibration overlay, capture, watchdog, submit). Each tracker is a
self-registering adapter under `public/trackers/` calling
`GazePry.registerTracker({...})`; heavy libraries in `public/lib/` are lazily
loaded only for the selected tracker. The contract is documented in
[`public/trackers/README-adapter.md`](public/trackers/README-adapter.md) and
enforced by `test/registry.test.js`, which loads the browser code in a `vm`
sandbox. Sessions never match across tracker families — analysis and the
`/identify` endpoint both partition by family.

### D7 stimuli are manifest-driven, and design is split from sourcing

`public/stimuli/manifest.json` (schema `gazepry.stimuli.v1`) is the single item
table read by both the browser task page and the Python analysis, so the two
cannot drift. Two scripts write it, in order:

- `scripts/make_stimuli.py` is the **design** — which items exist, their class
  and tier, and the counterbalancing invariants. Generates E1's 24 fractals
  (abstract *on purpose*: E1's validity requires no prior exposure) and writes
  obvious placeholders for E2/E3. Re-running **keeps** already-fetched real
  assets and sweeps images the item table no longer references.
- `scripts/fetch_stimuli.py` is the **sourcing** — resolves E2's 24 items
  (8 faces / 8 bank marks / 8 landmarks) to freely-licensed Wikimedia Commons
  files. It **refuses** any licence outside its free allow-list, pins every
  resolution and file hash in `stimuli.lock.json`, and regenerates
  `ATTRIBUTION.md`. `sources.json`, the lock, and the attribution are committed;
  the `e2/`/`e3/` images are not.

**E2 arrays are class-homogeneous** (`arrayGroupBy: "class"`): a face is never
shown alongside bank marks, or the probe could be picked out by category rather
than familiarity. A class must be a **contiguous block whose size is a multiple
of `N_GROUPS`**, because the Latin square runs over the global item index — the
checker and tests on both sides enforce this.

E3 is sourced (8 everyday documents) but its construct is weaker in kind, not
just in degree, so it is reported separately with an episodic-versus-semantic
caveat and never supports the mechanism claim; free-licensing left finance and
legal at one item each — see `public/stimuli/README.md`. The task page still
**disables Begin** while any set contains placeholders (the guard is generic; no
shipped set trips it now).

## Constraints that are not negotiable

- **Zero runtime dependencies.** `server.js` is stdlib Node, tests use
  `node:test` and stdlib `unittest`, analysis uses numpy only (matplotlib for
  `--plot`). `scripts/make_stimuli.py` writes PNGs with stdlib `zlib`/`struct`.
  Do not add a package to solve a problem the stdlib can solve.
- **Never commit participant data.** `data/*.json` (gaze) and `labels/`
  (questionnaire responses, the most sensitive thing the study holds) are
  gitignored and live in separate directories on purpose. Never copy either
  into `wiki/`. Note `.gitignore` only governs *untracked* paths — see
  `D7_COLLECTION_RUNSHEET.md` §1.1 for the outstanding untracking task.
- **No silent zero.** A trial that cannot be scored returns `None`/`null`, not a
  zero-filled row; a metric with a missing class returns `nan`, not 0.5. Zeros
  masquerade as data and score as chance, which reads as a negative result
  rather than a bug. Two regression tests pin failure modes of exactly this
  shape (see the notes below).
- **The RQ0 gate.** No D7 result counts unless the shuffled-label null and the
  saliency-only baseline both sit at ≈0.500. Report AUC intervals bootstrapped
  over *participants*, never point estimates or row-level resampling.
- `legacy-searchgazer/` is the archived 2016/2017 SearchGazer demo with dead
  SERP selectors. Deprecated — do not build on it.
- License is GPLv3, which is why third-party logos/screenshots for E2/E3 are
  gitignored rather than vendored.

## The wiki

[`wiki/`](wiki/) is an LLM-maintained wiki on Karpathy's pattern: raw sources
are immutable, the wiki is the compiled cross-linked layer over them, and
[`wiki/SCHEMA.md`](wiki/SCHEMA.md) is the constitution that governs it.

**Read [`wiki/SCHEMA.md`](wiki/SCHEMA.md) before touching the wiki.** It defines
the page format (frontmatter, `[[wiki-links]]`, aliases, `reviewed:`
protection), the shared numbered bibliography, and three workflows:

- **Ingest** — new/changed source (or files dropped in [`raw/`](raw/)): read it,
  write/update its `sources/` page, extract entities and concepts (update, don't
  duplicate), update [`wiki/index.md`](wiki/index.md), append to
  [`wiki/log.md`](wiki/log.md).
- **Query** — answer from the wiki first (start at `index.md`), fall back to raw
  sources, file durable answers back as pages.
- **Lint** — sweep for dead links, orphans, contradictions, stale claims,
  missing aliases; log the pass.

Entry points: [`wiki/index.md`](wiki/index.md) (catalog),
[`wiki/log.md`](wiki/log.md) (history), and `wiki/notes/` (dated session
findings — read `2026-07-22-d7-instrumentation-findings` before changing the
I-DT thresholds or the RQ0 controls).

Ask to **"ingest"**, **"query: <question>"**, or **"lint the wiki"**.

**Caveat:** the bundled `check_wiki.py` from the `wiki-ingest` skill reports
hundreds of false-positive dead links because it does not resolve `[[links]]`
across subfolders, contradicting SCHEMA's Obsidian basename rule. Resolve links
by basename before believing a failure.
