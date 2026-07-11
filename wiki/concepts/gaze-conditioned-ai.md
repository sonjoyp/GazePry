---
type: concept
tags: [gaze-ai, genai, llm, collection-surface, context]
aliases: [Gaze-Conditioned AI, Gaze-Aware AI, Gaze and LLMs, GenAI Gaze]
sources: [reid-research-plan]
reviewed: false
updated: 2026-07-11
---

A cluster of 2025–2026 work feeding **gaze into large language / vision-language
models** — gaze-conditioned LLMs, gaze-aware VLMs, and gaze-aware AI assistants.
For GazePry this is context, not method: it shows *why gaze collection is
proliferating* (a new, benign-looking reason to capture the stream), which
widens the very attack surface the re-ID thesis exploits. The societal framing
is [[abdrabou-2025-gaze-to-data]]. None of these papers is a security result;
several are **preprint-flagged** in plan §21.

## Key facts

- **GazeLLM** [11] ([[yang-2025-gazellm]]) — a plug-and-play zero-shot LLM
  reasoning framework that boosts gaze-target detection. Peer-reviewed (Vis.
  Intell. 2025).
- **GazeQwen** [16] ([[pham-2026-gazeqwen]]) — lightweight gaze-conditioned LLM
  modulation for streaming video understanding. *Preprint.*
- **GazeVLM** [18] ([[mathew-2026-gazevlm]]) — a vision-language model unifying
  person/gaze-target/object detection ("gaze understanding") from visual +
  language prompts. *Preprint.*
- **From Gaze to Guidance** [26] ([[danry-2026-gaze-to-guidance]]) — multimodal
  gaze-aware AI assistants that infer and adapt to users' cognitive needs
  (Microsoft Research / MIT). *Preprint.* Also a D3 cognitive-state data point.

## Related

- [[gaze-estimation]] — the capability these consume.
- [[enabling-conditions]] — proliferating reasons to collect gaze widen the
  surface.
- [[abdrabou-2025-gaze-to-data]] — the privacy/societal critique of the same
  trend.
- [[leakage-vectors-d1-d6]] — the assistant work touches D3 (cognitive state).

## Mentions in sources

- Plan §1/§18.7 (adjacent gaze-AI landscape), §21 (preprint flags for [16],
  [18], [26]) [11], [16], [18], [26].
