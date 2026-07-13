---
type: concept
tags: [evaluation, verification, synthetic, caveat]
aliases: [Synthetic Data Results, Simulate Results, Verify Without a Webcam, Pipeline Verification]
sources: [prototype-readme, prototype-code]
reviewed: false
updated: 2026-07-13
---

The **synthetic-data results** verify the [[analysis-pipeline]] end-to-end
without a webcam, using `simulate.py` subjects that have stable oculomotor traits
across tasks/sessions. **These are a code sanity check on synthetic data, not a
claim about real eyes** — real numbers come from the browser harness. The plan
now says this in as many words (§19a): the `data_sim/` cross-task/cross-session
rank-1 ≈0.28 at N=12 is a code sanity check on generated data, not a claim about
real eyes — and the real pilot to date is only N=2 ([[pilot-empirical-status]]).

## Key facts

- Generate + evaluate:
  ```bash
  python simulate.py --out ../data_sim --subjects 12 --sessions 2
  python reid.py --data ../data_sim --plot ../data_sim/cmc.png
  ```
- Expected (12 synthetic subjects, chance rank-1 = 0.083):

  | protocol | rank-1 | rank-5 | EER |
  |---|---|---|---|
  | all | 0.31 | 0.95 | 0.22 |
  | same_task_cross_session | 0.55 | 0.97 | 0.16 |
  | cross_task | 0.18 | 0.84 | 0.27 |
  | **cross_task_cross_session** (headline) | **0.28** | 0.86 | 0.25 |

- Sanity properties that must hold: rank-1 ≫ chance and EER < 0.5 under every
  protocol; same-task easiest, cross-task hardest — the ordering the study
  predicts.

## Related

- [[reid-protocols]] — the four protocols tabulated here.
- [[analysis-pipeline]] — the pipeline being verified.
- [[reid-metrics]] — rank-1/rank-5/EER.
- [[pilot-empirical-status]] — the *real* (N=2) pilot state, distinct from these
  synthetic numbers.

## Mentions in sources

- `README.md` (Verify without a webcam); `analysis/simulate.py`, `reid.py`;
  plan §19a (explicit "synthetic sanity check, not a claim about real eyes").
