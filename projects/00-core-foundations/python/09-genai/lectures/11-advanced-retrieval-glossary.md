# Advanced Retrieval — Glossary 11

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| BM25 | Retrieval | Lexical scoring: tf with idf + length norm |
| Fusion | Retrieval | Combining multiple score streams |
| Hybrid Search | Retrieval | Running lexical + semantic together |
| IDF | Retrieval | Inverse document frequency: rare terms matter more |
| Metadata Filter | Retrieval | Narrowing the search space by fields |
| Normalization | Retrieval | Mapping scores to a shared scale |
| Query Rewrite | Retrieval | Transforming a weak query into a better one |
| Term Frequency | Retrieval | How often a term appears in a doc |

## Detailed Definitions
### BM25
**Definition**: The standard lexical ranking function based on tf, idf, and
length normalization.
**Related**: Term Frequency

### Fusion
**Definition**: Merging normalized lexical and semantic scores with weights.
**Related**: Hybrid Search

### Hybrid Search
**Definition**: Running both lexical and semantic retrieval and fusing results.
**Related**: Fusion

### IDF
**Definition**: A weight rewarding terms that appear in few documents.
**Related**: BM25

### Metadata Filter
**Definition**: A pre-search constraint (source, date, type) narrowing
candidates.
**Related**: Hybrid Search

### Normalization
**Definition**: Scaling each score stream to a comparable range before fusion.
**Related**: Fusion

### Query Rewrite
**Definition**: Using an LLM to turn vague/multi-part queries into precise
search queries.
**Related**: Hybrid Search

### Term Frequency
**Definition**: The count of a term within a document; the base of lexical
scoring.
**Related**: BM25

## Key Concepts Summary
### The Idea
- Lexical and semantic fail differently; combine them

### The Rules
- Normalize before fusing
- Filter before scoring

## Practice Terms
Match each term to its definition (answers at the bottom).
1. BM25 — ___
2. Fusion — ___
3. Filter — ___
4. Query rewrite — ___
5. IDF — ___

**Answers:** 1-c, 2-e, 3-a, 4-b, 5-d where a=pre-search narrowing, b=query
improvement, c=lexical ranker, d=rare-term weight, e=score merging.
