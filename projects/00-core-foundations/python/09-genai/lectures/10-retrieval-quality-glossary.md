# Retrieval Quality — Glossary 10

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Eval Set | Evaluation | Labeled queries with known relevant chunks |
| Hit Rate | Metric | ≥1 relevant chunk in top-k (binary) |
| MRR | Metric | Mean reciprocal rank of first correct hit |
| Precision@k | Metric | Fraction of top-k that is relevant |
| Recall@k | Metric | Fraction of relevant items found in top-k |
| Re-Ranking | Retrieval | Re-scoring top-k with a stronger model |
| Top-k | Retrieval | The retrieved set size passed to generation |

## Detailed Definitions
### Eval Set
**Definition**: A labeled query→relevant-chunk-ID set used to score retrieval.
**Related**: Recall@k

### Hit Rate
**Definition**: Per-query binary: 1 if any relevant chunk is in top-k.
**Related**: Recall@k

### MRR
**Definition**: Mean over queries of 1/(rank of first relevant hit).
```python
mrr = mean(1 / rank_first_hit(q))
```
**Related**: Hit Rate

### Precision@k
**Definition**: The share of the top-k that is actually relevant.
**Related**: Recall@k

### Recall@k
**Definition**: The share of all relevant chunks that made it into top-k.
**Related**: Precision@k

### Re-Ranking
**Definition**: Retrieving a wide top-k, then re-scoring with a stronger model
to refine order.
**Related**: MRR

### Top-k
**Definition**: The number of chunks passed from retrieval to generation.
**Related**: Recall@k

## Key Concepts Summary
### The Metrics
- Recall: did we find it?
- Precision: was it relevant?
- MRR: was it first?

### The Rule
- Change one variable, re-run the eval set

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Recall@k — ___
2. Hit rate — ___
3. MRR — ___
4. Eval set — ___
5. Re-ranking — ___

**Answers:** 1-c, 2-e, 3-a, 4-b, 5-d where a=first-hit rank reciprocal, b=
labeled queries, c=relevant found in top-k, d=re-score retrieved set, e=any
hit in top-k.
