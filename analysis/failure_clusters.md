# Failure Cluster Analysis — Phase A

**Student:** Le Quoc An
**Date:** 2026-08-27

## Aggregate RAGAS scores by distribution

| Metric | Factual | Multi-hop | Adversarial |
|---|---:|---:|---:|
| Faithfulness | 1.0000 | 1.0000 | 1.0000 |
| Answer relevancy | 0.5385 | 0.4273 | 0.6020 |
| Context precision | 0.1696 | 0.1235 | 0.1073 |
| Context recall | 0.7304 | 0.4264 | 0.3599 |
| **Average** | **0.6096** | **0.4943** | **0.5173** |

## Failure cluster matrix

| Worst metric | Factual | Multi-hop | Adversarial | Total |
|---|---:|---:|---:|---:|
| Faithfulness | 0 | 0 | 0 | 0 |
| Answer relevancy | 0 | 0 | 0 | 0 |
| Context precision | 20 | 20 | 10 | 50 |
| Context recall | 0 | 0 | 0 | 0 |

The dominant metric is **context precision**. The lexical local retriever consistently returns a relevant policy passage, but it does not distinguish finely enough between closely related policies, versions, and subclauses. Multi-hop questions have the lowest mean score (0.4943) because their answer requires joining two policy sources rather than quoting one retrieved chunk.

The adversarial set (0.5173) is below factual (0.6096), which is the expected signal for version conflicts and negation traps. Questions 49 (legacy leave policy) and 50 (personal VPN) both appear in the bottom ten. The recommended next change is a semantic/cross-encoder reranker together with metadata filters for policy version and effective date.

## Suggested fixes

| Weak area | Root cause | Suggested fix |
|---|---|---|
| Context precision | Lexical overlap admits near-matching policies | Add dense retrieval plus cross-encoder reranking |
| Context recall | Multi-hop evidence is split across documents | Retrieve more candidates, then compose cited evidence |
| Version conflicts | Older policies remain searchable | Filter or down-rank superseded versions by effective date |
| Answer relevancy | Context chunk is returned verbatim in offline mode | Generate a concise grounded answer from selected evidence |
