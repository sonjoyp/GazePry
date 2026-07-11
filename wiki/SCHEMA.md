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
   Current sources: `README.md`, `GazePry_Information_Leakage_Report.md`,
   `GazePry_Direction1_ReID_Study_Protocol.md`, `prototype/README.md`, and the
   prototype code itself (`prototype/*.js`, `prototype/public/`,
   `prototype/analysis/`).
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

The project keeps a shared numbered bibliography: entries [1]–[29] live in
`GazePry_Information_Leakage_Report.md`; [30]–[49] are added by
`GazePry_Direction1_ReID_Study_Protocol.md` §16 (which also reproduces the
carried-over subset). Wiki pages cite with the same bracket numbers, e.g.
"EER ≈ 0.6% [20]". Do not renumber; do not invent new numbers — a genuinely
new reference is added to the source documents first, not the wiki.

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
