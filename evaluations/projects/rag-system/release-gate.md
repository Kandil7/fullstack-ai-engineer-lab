# Release Gate: rag-system

- **Project:** rag-system
- **Version:** 1.0.0
- **Created:** 2026-06-26
- **Status:** Not ready
- **Owner:** —

---

## Purpose

This checklist defines the criteria for releasing the RAG system to production. RAG systems have unique quality requirements around retrieval accuracy, hallucination prevention, and cost efficiency.

---

## Gate Criteria

### 1. Retrieval Quality Metrics

- [ ] Recall@5 > 0.85 on the evaluation dataset
- [ ] Precision@3 > 0.80 on the evaluation dataset
- [ ] MRR > 0.70 on the evaluation dataset
- [ ] Evaluation dataset covers all knowledge domains (≥ 10 questions per domain)
- [ ] No single question has Recall@5 = 0 (complete retrieval failure)
- [ ] Baseline metrics documented in `evaluations/rag/baselines/`

**Evaluation dataset:** —
**Date tested:** —
**Results report:** —

### 2. Hallucination Rate

- [ ] Faithfulness score > 0.95 on evaluation dataset
- [ ] No Critical hallucinations (fabricated facts presented as truth)
- [ ] High-severity hallucinations < 5% of questions
- [ ] LLM-as-judge evaluation completed for all generated answers
- [ ] Manual review of 10% random sample confirms faithfulness

**Hallucination rate:** —%
**Date tested:** —
**Review methodology:** —

### 3. Latency Benchmarks

- [ ] Retrieval latency (p50) < 200ms
- [ ] Retrieval latency (p99) < 500ms
- [ ] End-to-end latency (p50) < 3s
- [ ] End-to-end latency (p99) < 5s
- [ ] Tested under expected production load (≥ 100 concurrent queries)
- [ ] No timeout errors under normal load

**Load test results:** —
**Date tested:** —

### 4. Cost Analysis

- [ ] Cost per query documented (embedding + generation)
- [ ] Monthly cost projection for expected usage
- [ ] Embedding model costs within budget
- [ ] LLM generation costs within budget
- [ ] Caching strategy implemented for repeated queries
- [ ] Cost monitoring/alerting configured

**Cost per query:** $—
**Monthly projection:** $—
**Budget:** $—

### 5. Knowledge Base Quality

- [ ] All source documents ingested and indexed
- [ ] No duplicate chunks in the vector database
- [ ] Chunk quality reviewed (no split mid-sentence for prose, no split mid-function for code)
- [ ] Metadata correctly applied (source file, section, topic)
- [ ] Ingestion pipeline is idempotent (re-running doesn't create duplicates)

**Total chunks:** —
**Source documents:** —
**Date ingested:** —

### 6. Error Handling & Monitoring

- [ ] Retrieval failures return graceful error messages (not stack traces)
- [ ] LLM API failures retry with exponential backoff (max 3 retries)
- [ ] Rate limiting on LLM API calls
- [ ] Monitoring dashboards show: query count, latency, error rate, cost
- [ ] Alerts configured for: latency > 5s, error rate > 5%, cost spike
- [ ] Fallback behavior defined (what happens when retrieval returns 0 results)

**Monitoring location:** —
**Alert configuration:** —

### 7. Testing

- [ ] Unit tests for chunking logic
- [ ] Unit tests for embedding generation
- [ ] Integration tests for retrieval pipeline
- [ ] Integration tests for end-to-end query flow
- [ ] Regression tests using golden dataset
- [ ] Load test completed without failures

**Test coverage:** —%
**Test command:** —
**Date tested:** —

---

## Gate Decision

- [ ] **PASS** — All criteria met. RAG system is release-ready.
- [ ] **CONDITIONAL PASS** — Minor issues documented; release with monitoring.
- [ ] **BLOCK** — Critical issues found. Cannot release.

**Decision made by:** —
**Date:** —
**Rationale:** —

---

## Post-Release Monitoring

After release, monitor for 2 weeks:

| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| Faithfulness < 0.90 | Immediate | Investigate hallucination source |
| Latency p99 > 10s | Immediate | Check LLM API health |
| Error rate > 10% | Within 1 hour | Check retrieval pipeline |
| Cost > 2x daily average | Within 1 day | Review query patterns |

---

## Notes

- RAG quality degrades over time as knowledge base becomes stale — schedule monthly re-evaluation
- Hallucination rate is the most critical metric for user trust
- Cost analysis should include both development and production environments
- This gate is more stringent than typical API services due to AI-generated content risks
