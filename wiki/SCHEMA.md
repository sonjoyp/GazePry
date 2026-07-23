# GazePry Wiki — Schema

This file is the constitution of the GazePry LLM wiki. Any agent (or human)
maintaining the wiki follows the conventions and workflows defined here.
The pattern is Karpathy's "LLM wiki": raw sources are immutable, the wiki is
LLM-owned and incrementally compiled, and this schema is what makes the
maintainer disciplined rather than improvisational.

## The three layers

1. **Raw sources** — the repo's documents and code, plus anything dropped into
   the `raw/` inbox (papers, web clips, meeting notes, reviews). Immutable from
   the wiki's point of view: the wiki never edits them, only reads them.
   Current sources: `README.md`, `GazePry_ReID_Research_Plan.md` (the living
   plan), the harness code at the repo root (`server.js`, `reid-core.js`,
   `public/` incl. `public/trackers/`, `analysis/`, `test/`, `scripts/`), and
   everything in `raw/` — including the frozen predecessor docs
   (`raw/GazePry_Information_Leakage_Report.md`,
   `raw/GazePry_Direction1_ReID_Study_Protocol.md`) and the ingested papers.
2. **The wiki** (`wiki/`) — generated markdown pages, organized by type
   (below). The LLM owns this layer entirely and updates it as sources change.
3. **The schema** — this file.

## Directory layout

```
raw/               inbox — drop new source files here (papers, clips, notes);
                   processed files stay put, the wiki records having read them
wiki/
  SCHEMA.md        this file — conventions and workflows
  index.md         catalog of every page, by category, with one-line summaries
  log.md           append-only operation log (ingests, queries, lint passes)
  sources/         one page per ingested source: summary + pointers
  entities/        named things: tools, systems, datasets, papers-as-artifacts,
                   organizations, venues
  concepts/        ideas: threat models, techniques, metrics, phenomena
```

The `wiki/` folder is a valid Obsidian vault subtree: links are Obsidian
`[[wiki-links]]`, resolved by filename regardless of subfolder.

## Page format

Every page starts with YAML frontmatter:

```yaml
---
type: source | entity | concept
subtype: (entities only: tool | system | dataset | model | attack | org | venue)
tags: [lowercase, kebab-case]
aliases: [Alternative Names, abbreviations]
sources: [slugs-of-source-pages-this-page-derives-from]
reviewed: false
updated: YYYY-MM-DD
---
```

- **Filenames** are kebab-case slugs (`gaze-re-identification.md`); the slug is
  the link target: `[[gaze-re-identification]]`.
- **Aliases** list every name variant a future ingest might use, so duplicate
  pages are caught before they are created.
- **`reviewed: true`** marks a page a human has verified; the LLM may append to
  such a page but must not rewrite or delete existing claims on it.
- **`updated`** is bumped on every substantive edit.

Body structure (sections optional except the lead):

1. A lead paragraph defining the thing, dense with `[[links]]`.
2. `## Key facts` — grounded, checkable bullets (numbers, paths, thresholds).
3. `## Related` — links whose relevance isn't obvious from the lead, with a
   phrase saying *why* each is related.
4. `## Mentions in sources` — pointers back into the raw sources (file +
   section), so every claim is traceable.
5. `## Open questions` — contradictions, gaps, or stale claims found while
   writing; these feed the lint workflow.

## Citation convention

The project keeps a shared numbered bibliography. Its canonical home is
**`GazePry_ReID_Research_Plan.md` §21** (entries [1]–[54], with per-citation
verification/preprint status). The frozen predecessors in `raw/` use the *same*
numbering ([1]–[29] originated in the report; [30]–[49] in the protocol §16) —
no renumbering happened at the merge; [50]–[54] were appended 2026-07-13 for five
eye-movement-biometrics papers (Eberz, Liao, Rigas, Li, Galdi) and exist only in
the plan, not the frozen docs. Wiki pages cite with the same bracket numbers,
e.g. "EER ≈0.58% at a 60 s window [20]". Do not renumber; do not invent new
numbers — a genuinely new reference is added to the source documents first, then
the wiki reflects it (as happened for [50]–[54]).

**Trap 1:** `raw/related-papers.txt` is a reference-collection export with its
own independent numbering ([1]–[67]) that does **not** match the project
numbering — never cite its bracket numbers (e.g. the five 2026-07-13 papers are
[63]–[67] there but [50]–[54] in the plan). Papers in `raw/` that are not in
plan §21 are cited by author-year (their `sources/` page), not by number.

**Trap 2 (added 2026-07-23):** `GazePry_D7_Recognition_Knowledge_Direction.md`
was made standalone and now carries its **own** complete bibliography,
renumbered **[1]–[30] local to that file**, which does not match the project
numbering. The collisions are silent rather than obviously wrong — [5] is
Weinberg (history sniffing) in the shared scheme but Nahari et al. 2019 in the
D7 document, [6] is Liebling & Preibusch there and Millen & Hancock here, and
Weinberg is [16] in D7. Wiki pages keep citing the **shared** numbering;
resolve anything traced to the D7 document by author-year and never carry its
bracket number across. See [[d7-recognition-knowledge-direction]].

## Workflows

### Ingest (new or changed source)

Triggered by "ingest" (sweeps `raw/` for files not yet in `log.md`, and repo
docs whose content changed since their source page's `updated` date) or by
naming a specific file. Process one source at a time:

1. Read the source end-to-end.
2. Create or update its page in `sources/` — a faithful summary plus pointers,
   never a full copy.
3. Extract entities and concepts. For each: search `index.md` and aliases for
   an existing page; **update** rather than duplicate. Target granularity is
   moderate — a page per load-bearing thing, not per noun.
4. Add bidirectional context: when page A gains a link to B, make sure B's
   text gives the reader a path back to A where that is useful.
5. Update `index.md`; append an entry to `log.md`.

### Query (answering questions from the wiki)

1. Start at `index.md`; follow links rather than re-reading raw sources when
   the wiki already covers the topic. Fall back to raw sources for anything
   the wiki lacks — and treat that gap as a signal.
2. If the synthesized answer is durable and non-trivial, file it back: extend
   an existing page or add a concept page, then log the query.

### Lint (periodic health check)

1. Sweep all pages for: dead `[[links]]`, orphan pages (nothing links in),
   contradictions between pages or between a page and its source, stale
   claims (source changed since `updated`), and missing aliases.
2. Fix what is mechanical; record judgment calls under `## Open questions` on
   the affected page.
3. Append a lint report to `log.md`.

## Style rules

- Ground every quantitative claim in a source (bracket citation or a
  file/section pointer). No unsourced numbers.
- Prefer updating an existing page over creating a new one.
- Pages are for durable knowledge; session-specific chatter goes in `log.md`
  only.
- Keep the repo's own caveats intact when summarizing (e.g. synthetic-data
  results are sanity checks, not findings; webcam numbers are lower bounds).
- Never copy raw participant gaze data or personally identifying detail into
  the wiki.
