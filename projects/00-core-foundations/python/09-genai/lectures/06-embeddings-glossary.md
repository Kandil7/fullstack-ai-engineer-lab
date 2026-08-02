# Embeddings — Glossary 06

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Bag of Words | Model | Text as unordered word counts |
| Cosine Similarity | Math | Cosine of the angle between two vectors |
| Dimension | Model | Length of an embedding vector |
| Embedding | Model | Dense vector representing text meaning |
| Normalization | Math | Scaling a vector to unit length |
| Semantic Search | Application | Retrieval by meaning, not keywords |
| Vector Index | Infrastructure | Structure for fast nearest-neighbor search |
| Nearest Neighbor | Math | The most similar item(s) to a query |

## Detailed Definitions
### Bag of Words
**Definition**: Representing text as a multiset of words, losing order and
synonyms.
**Related**: Embedding

### Cosine Similarity
**Definition**: The cosine of the angle between vectors; length-invariant.
```python
sim = a @ b  # after normalizing both
```
**Related**: Normalization

### Dimension
**Definition**: The number of values in an embedding vector (e.g. 768).
**Related**: Embedding

### Embedding
**Definition**: A dense vector where similar texts are geometrically close.
**Related**: Dimension

### Normalization
**Definition**: Dividing a vector by its length so it has unit norm.
**Related**: Cosine Similarity

### Semantic Search
**Definition**: Ranking results by embedding similarity instead of keywords.
**Related**: Vector Index

### Vector Index
**Definition**: A data structure (ANN) making nearest-neighbor search fast at
scale.
**Related**: Semantic Search

### Nearest Neighbor
**Definition**: The item with the highest similarity to the query.
**Related**: Cosine Similarity

## Key Concepts Summary
### The Math
- Normalize, then dot, then rank

### The Limits
- Bag-of-words: no order, no synonyms

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Embedding — ___
2. Cosine — ___
3. Normalize — ___
4. Bag of words — ___
5. Semantic search — ___

**Answers:** 1-d, 2-b, 3-c, 4-e, 5-a where a=search by meaning, b=angle-based
similarity, c=unit-length scaling, d=meaning vector, e=unordered word counts.
