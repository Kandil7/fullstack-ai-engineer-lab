# Reranking — Glossary 12

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Bi-Encoder | Ranking | Embeds query/doc separately; fast, precomputable |
| Candidate Set | Ranking | The wide top-N from stage 1 retrieval |
| Cross-Encoder | Ranking | Scores (query, doc) jointly; accurate, per-pair |
| Rank | Ranking | Position in an ordered result list |
| Reranker | Ranking | A stronger model re-scoring candidates |
| Two-Stage | Architecture | Cheap retrieve, then strong re-rank |
| Window | Ranking | The subset of candidates re-scored (M) |
| Relevance Score | Ranking | A number rating query-doc match |

## Detailed Definitions
### Bi-Encoder
**Definition**: Query and document embedded independently; similarity is a
vector dot. Precomputable for all docs.
**Related**: Cross-Encoder

### Candidate Set
**Definition**: The top-N results from cheap retrieval, awaiting reranking.
**Related**: Two-Stage

### Cross-Encoder
**Definition**: A model seeing query and doc together, outputting a match
score. Accurate but run per pair.
**Related**: Bi-Encoder

### Rank
**Definition**: A result's position (1 = best).
**Related**: Reranker

### Reranker
**Definition**: Any function scoring (query, chunk) → relevance, applied after
stage-1 retrieval.
**Related**: Window

### Two-Stage
**Definition**: Architecture: wide cheap retrieval, then narrow strong
reranking.
**Related**: Candidate Set

### Window
**Definition**: The number of candidates (M) the reranker scores, between N
retrieved and k kept.
**Related**: Reranker

### Relevance Score
**Definition**: The output of a reranker for one pair.
**Related**: Cross-Encoder

## Key Concepts Summary
### The Pattern
- Retrieve N → rerank M → keep k

### The Rules
- Stage 1 is for recall, stage 2 for precision
- Measure MRR before and after

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Two-stage — ___
2. Cross-encoder — ___
3. Window — ___
4. Bi-encoder — ___
5. Candidate set — ___

**Answers:** 1-c, 2-b, 3-e, 4-d, 5-a where a=wide stage-1 results, b=joint pair
scoring, c=cheap then strong, d=separate embeddings, e=re-scored subset.
