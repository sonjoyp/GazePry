---
type: source
tags: [prototype, superseded, how-to]
aliases: [Prototype README, Direction 1 Prototype, prototype/README]
sources: [readme]
reviewed: false
updated: 2026-07-11
---

**Superseded.** `prototype/README.md` no longer exists as a separate document:
on 2026-07-10 the prototype was merged into the repo root (commits 888735c,
9abca6d) and its README content was folded into the root `README.md` — see
[[readme]] for the current summary. This page remains as a link target for the
pre-merge references.

## Key facts

- Everything this page used to describe now lives in [[readme]]: the harness
  layout (now at the repo root, not `prototype/`), quick start, the live re-ID
  demo, the synthetic verification path, the Gazepoint rig, and the
  cross-origin recipe.
- What changed beyond the move: the harness became **tracker-pluggable**
  (adapters for [[webgazer]], [[webeyetrack]], [[eyegestures]], [[gazecloud]]),
  session filenames gained the tracker family, and a regression suite
  (`npm test`) was added.

## Related

- [[readme]] — the living document that absorbed this one.
- [[prototype-code]] — the code the old README described, updated to the
  current layout.

## Mentions in sources

- Historical: `prototype/README.md` (pre-merge, gone); current content in
  `README.md`.
