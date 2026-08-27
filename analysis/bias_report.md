# LLM Judge Bias Report — Phase B

**Student:** Le Quoc An
**Date:** 2026-08-27
**Judge mode:** deterministic offline fallback (not a live GPT-4o-mini judgement)

## Results

Ten human-labelled questions were compared between the human reference answer (A) and the local retrieval answer (B). The fallback selected B in every pair because its lexical relevance/completeness score favoured long policy excerpts.

| Measure | Result |
|---|---:|
| Evaluated pairs | 10 |
| Position-inconsistent pairs | 0 |
| Position bias rate | 0.0% |
| Cohen's κ vs human labels | 0.000 |
| Decisive results preferring the longer answer | 10/10 |
| Verbosity bias | 100.0% |

The two swap passes produced the same original-order winner for all ten questions, so this implementation shows no measured position bias. However, the fallback has severe verbosity bias: it rewards long retrieved passages over concise correct answers. This also explains κ = 0.0; it must not be interpreted as evidence that an LLM judge is unreliable.

For production, run the same pairwise protocol with the configured LLM and the strict JSON rubric, retain swap-and-average, and monitor both κ and verbosity bias. A concise-answer penalty or explicit citation/accuracy criterion should prevent long context excerpts from winning merely because they contain more overlapping terms.
