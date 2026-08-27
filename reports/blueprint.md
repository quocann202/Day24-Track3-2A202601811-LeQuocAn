## CI/CD Blueprint: RAG Eval + Guardrail Stack

**Student:** Le Quoc An
**Date:** 2026-08-27

### Guard Stack Pipeline

| Layer | Tool | Latency P95 | Failure action |
|---|---|---:|---|
| PII detection | Presidio + regex fallback | 0.38 ms | Reject request, redact and log event |
| Topic/jailbreak | NeMo Input Rail + local policy fallback | 0.01 ms | 503 with safe refusal |
| RAG pipeline | Day 18 retrieval/generation | <2000 ms target | Grounded fallback response |
| Output check | NeMo Output Rail + PII scan | <300 ms target | Block/redact and log event |

### CI Gates

- [ ] RAGAS faithfulness >= 0.75 on the 50-question set.
- [ ] Adversarial suite pass rate >= 90% (18/20).
- [ ] P95 total guard latency < 500 ms.
- [ ] `pytest tests/ -q` passes before merge.

### Monitoring

| Signal | Threshold | Response |
|---|---|---|
| Faithfulness | <0.70 | investigate retrieval/context regression |
| Guard block rate | <80% on attack suite | add patterns and update rail tests |
| Guard P95 | >600 ms | inspect NeMo/API latency and scale or cache |
| PII events | >10/hour | security alert and audit |

### Current Lab Baseline

The guard implementation blocks PII, prompt injection, jailbreak, sensitive-data requests, and clearly off-topic prompts using NeMo where configured and a deterministic local policy otherwise. On 2026-08-27, the offline guard suite passed **20/20** and measured **0.39 ms P95 total** (Presidio 0.38 ms; input rail 0.01 ms). Phase A results must be generated from the real Day 18 pipeline output (`answers_50q.json`), so no synthetic RAGAS score is presented as production evidence.
