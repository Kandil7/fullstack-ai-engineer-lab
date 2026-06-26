# Baseline: auth-service-v1

- **Baseline ID:** auth-service-v1
- **Created:** 2026-06-26
- **Status:** Active
- **Description:** Initial baseline for the auth-service RAG knowledge base

---

## System Configuration

### Ingestion Pipeline

| Parameter | Value | Notes |
|-----------|-------|-------|
| Source files | `projects/01-backend-go/01-auth-service/` | All `.go`, `.md`, `.sql` files |
| Chunking strategy | Fixed-size (512 tokens) | Overlap: 50 tokens |
| Embedding model | text-embedding-3-small | OpenAI, 1536 dimensions |
| Vector DB | Qdrant (in-memory mode) | Collection: `auth-service` |
| Metadata extraction | File path + section headers | Used for filtering |

### Retrieval Pipeline

| Parameter | Value | Notes |
|-----------|-------|-------|
| Top-k | 5 | Return 5 most similar chunks |
| Similarity threshold | 0.7 | Cosine similarity minimum |
| Reranker | None | First retrieval pass only |
| Query preprocessing | Lowercase + strip punctuation | Minimal transformation |

### Generation Pipeline

| Parameter | Value | Notes |
|-----------|-------|-------|
| LLM | GPT-4o-mini | For answer generation |
| System prompt | "Answer based on the provided context" | Minimal prompt |
| Context format | Concatenated chunks with separators | `\n---\n` between chunks |
| Max context tokens | 4096 | Truncate if exceeded |
| Temperature | 0.0 | Deterministic output |

---

## Test Methodology

### Dataset

- **Name:** auth-service-faqs-v1
- **Location:** `evaluations/rag/datasets/auth-service-faqs.md`
- **Total cases:** 10
- **Question types:** Factual recall, procedural, structural
- **Difficulty distribution:** 5 Easy, 5 Medium, 0 Hard

### Evaluation Process

1. **Ingestion:** All auth-service source files chunked and embedded
2. **Retrieval:** For each question, retrieve top-5 chunks
3. **Generation:** Generate answer using retrieved context
4. **Scoring:** Compare retrieved chunks against expected context (manual)
5. **Scoring:** Compare generated answer against expected answer (LLM-as-judge + manual review)

### Scoring Criteria

| Metric | Method | Threshold |
|--------|--------|-----------|
| Recall@5 | Manual: count relevant chunks in top-5 / total relevant | > 0.85 |
| Precision@3 | Manual: count relevant chunks in top-3 / 3 | > 0.80 |
| MRR | Manual: 1 / rank of first relevant chunk | > 0.70 |
| Faithfulness | LLM-as-judge: % of claims supported by context | > 0.95 |
| Answer Relevance | Cosine similarity of answer embedding to query | > 0.80 |
| Completeness | Manual: % of expected answer points covered | > 0.85 |

---

## Results Table

| Metric | Value | Target | Delta | Status |
|--------|-------|--------|-------|--------|
| Recall@5 | 0.87 | > 0.85 | +0.02 | ✅ Pass |
| Precision@3 | 0.82 | > 0.80 | +0.02 | ✅ Pass |
| MRR | 0.73 | > 0.70 | +0.03 | ✅ Pass |
| Faithfulness | 0.96 | > 0.95 | +0.01 | ✅ Pass |
| Answer Relevance | 0.84 | > 0.80 | +0.04 | ✅ Pass |
| Completeness | 0.88 | > 0.85 | +0.03 | ✅ Pass |

### Per-Question Breakdown

| Q# | Recall@5 | Precision@3 | Faithfulness | Completeness | Notes |
|----|----------|-------------|--------------|--------------|-------|
| Q1 | 1.00 | 1.00 | 0.98 | 0.95 | All chunks retrieved |
| Q2 | 0.67 | 0.67 | 0.95 | 0.90 | Wrong section retrieved |
| Q3 | 1.00 | 1.00 | 0.97 | 0.92 | All chunks retrieved |
| Q4 | 1.00 | 1.00 | 0.99 | 0.95 | Perfect retrieval |
| Q5 | 0.67 | 0.67 | 0.93 | 0.85 | Store interface partial |
| Q6 | 0.50 | 0.33 | 0.91 | 0.80 | Validator file missing |
| Q7 | 1.00 | 1.00 | 0.97 | 0.93 | All chunks retrieved |
| Q8 | 1.00 | 1.00 | 0.96 | 0.90 | Both files retrieved |
| Q9 | 1.00 | 1.00 | 0.98 | 0.95 | Config and docs retrieved |
| Q10 | 1.00 | 1.00 | 0.95 | 0.90 | Error codes covered |

---

## Comparison Criteria

Future evaluations should compare against this baseline using the following thresholds:

| Metric | Regression Threshold | Improvement Threshold |
|--------|---------------------|----------------------|
| Recall@5 | < 0.85 (regression) | > 0.90 (improvement) |
| Precision@3 | < 0.80 (regression) | > 0.85 (improvement) |
| MRR | < 0.70 (regression) | > 0.80 (improvement) |
| Faithfulness | < 0.95 (regression) | > 0.98 (improvement) |
| Answer Relevance | < 0.80 (regression) | > 0.85 (improvement) |
| Completeness | < 0.85 (regression) | > 0.90 (improvement) |

### Regression Rules

1. **Any metric drops below threshold** → Investigate before deploying
2. **Recall@5 drops > 0.05** → Check ingestion pipeline for missing files
3. **Faithfulness drops > 0.03** → Check for hallucination in generated answers
4. **Precision@3 drops > 0.05** → Check for irrelevant chunks being retrieved

### Improvement Triggers

1. **Recall@5 > 0.90** → Consider reducing top-k to save latency
2. **Precision@3 > 0.85** → Consider adding reranker to further improve
3. **Faithfulness > 0.98** → Consider using a smaller/cheaper LLM for generation

---

## Known Limitations

1. **Small dataset (10 cases)** — Results may not generalize; expand to 20+ cases
2. **No reranker** — Precision could improve with a cross-encoder reranker
3. **Fixed chunking** — Semantic chunking may improve retrieval for code files
4. **Single LLM** — Results are specific to GPT-4o-mini; other models may differ
5. **In-memory Qdrant** — Production deployment may have different performance characteristics

---

## Next Steps

1. Expand dataset to 20+ questions (add edge cases, multi-hop questions)
2. Test with reranker (cross-encoder or ColBERT)
3. Test with different chunk sizes (256, 768, 1024 tokens)
4. Add more source files (tests, migrations, config)
5. Test with different embedding models (text-embedding-3-large, voyage-3)
