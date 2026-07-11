# CLAUDE.md — GazePry

Guidance for AI agents working in this repository.

## The wiki

This repo has an **LLM-maintained wiki** under [`wiki/`](wiki/), built on
Karpathy's LLM-wiki pattern: raw sources are immutable, the wiki is the
compiled cross-linked layer over them, and [`wiki/SCHEMA.md`](wiki/SCHEMA.md)
is the constitution that governs it.

**Before touching the wiki, read [`wiki/SCHEMA.md`](wiki/SCHEMA.md).** It
defines the page format (frontmatter, `[[wiki-links]]`, aliases,
`reviewed:` protection), the shared numbered bibliography convention, and the
three workflows:

- **Ingest** — new/changed source (or files dropped in [`raw/`](raw/)): read it,
  write/update its `sources/` page, extract entities and concepts (update, don't
  duplicate), update [`wiki/index.md`](wiki/index.md), append to
  [`wiki/log.md`](wiki/log.md).
- **Query** — answer from the wiki first (start at `index.md`), fall back to raw
  sources, and file durable answers back as pages.
- **Lint** — sweep for dead links, orphans, contradictions, stale claims, and
  missing aliases; log the pass.

Entry points: [`wiki/index.md`](wiki/index.md) (catalog) and
[`wiki/log.md`](wiki/log.md) (history).

### Common commands

- Ingest new material: drop files in `raw/`, then ask to **"ingest"**.
- Answer a question **from the wiki**: ask to **"query: <question>"**.
- Health check: ask to **"lint the wiki"**.

## Project facts an agent should not re-derive

- GazePry is a security/privacy research project on information leakage from
  webcam eye tracking; see [`wiki/entities/gazepry.md`](wiki/entities/gazepry.md).
- Active code is under `prototype/` on **WebGazer v3.5.3**. The repo-root
  SearchGazer (2016/2017) demo is **deprecated** (dead SERP selectors) — do not
  build on it.
- Never commit raw participant gaze data (`prototype/data/` is git-ignored) or
  copy it into the wiki.
- License is GPLv3.
