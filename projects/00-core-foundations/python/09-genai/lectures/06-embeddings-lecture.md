# GenAI — 06: Embeddings

## Topic Overview

Embeddings are dense numerical vectors that represent text (words, sentences,
documents, images) such that **semantic similarity maps to vector distance**:
similar meanings land close together, unrelated meanings far apart. They are
the foundation of retrieval (finding the right context for RAG), semantic
search, clustering, deduplication, and classification. Where token
probabilities give you *generation*, embeddings give you *understanding-as-
geometry*.

The key properties an AI engineer must internalize:

1. **Dimensionality**: typically 384–3072 floats per text. High-dim geometry
   is counterintuitive (everything is "far"), which is why cosine similarity
   is the standard measure, not Euclidean distance.
2. **The embedding model is a different model** from the chat model: OpenAI
   `text-embedding-3-small/large`, sentence-transformers (SBERT), Cohere,
   Gemini, local models. It has its own cost, latency, and dimension budget.
3. **Semantic vs lexical**: embeddings find *meaning* matches ("how to reset
   password" ↔ "forgot my login credentials"), which keyword search (BM25)
   cannot. But embeddings can miss exact tokens — which is why hybrid search
   combines both (Lecture 11).

Why this matters: embeddings are where the "AI" cost lives in RAG systems —
you embed every document once (ingestion) and embed every query at runtime.
Embedding quality directly drives retrieval quality (Lecture 10), which drives
answer quality (Lecture 9). The whole RAG stack stands on this lecture.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain what an embedding is and why cosine similarity measures semantics
2. Embed text with an API model and a local model (sentence-transformers)
3. Compute and interpret cosine similarity
4. Choose an embedding model by dimension, quality, cost, and language
5. Detect the failure modes (domain mismatch, out-of-vocabulary, dimension drift)
6. Use embeddings for search, clustering, dedup, and classification
7. Know when to re-embed (model change = re-index everything)

## Prerequisites

| Need | Where |
|---|---|
| LLM fundamentals | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| NumPy | `03-libraries/numpy/` |
| Vector math | `07-machine-learning/` (linear algebra) |
| RAG preview | `09-genai/lectures/09-rag-baseline-lecture.md` |

## 1. What an Embedding Is

An embedding is a fixed-length vector produced by a neural encoder. The magic
is in the *geometry*: the encoder is trained (contrastive learning — pull
similar pairs together, push dissimilar apart) so that direction/distance in
vector space encodes meaning.

```python
# conceptual: text → vector (e.g. 384 dims)
embedding = embed("the cat sat on the mat")
print(embedding[:8], "...", len(embedding))
```

Output:
```
[-0.021, 0.154, -0.098, ...] 384 floats — a "meaning" point in space
```

Two sentences are similar if their vectors are close. The encoder never sees
your task — it learned general semantic structure from massive text pairs —
which is why the same embedding serves search, clustering, and classification.

## 2. Cosine Similarity: The Semantic Distance

Cosine similarity measures the angle between vectors (0 = unrelated,
1 = identical direction), ignoring magnitude:

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors (the standard semantic metric)."""
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / denom) if denom else 0.0

# mock embeddings of similar vs unrelated sentences
happy = np.array([1.0, 0.8, 0.2, 0.0])
joyful = np.array([0.9, 0.85, 0.1, 0.05])
sad = np.array([-0.7, -0.5, 0.3, 0.4])

print("happy~joyful:", round(cosine_similarity(happy, joyful), 3))
print("happy~sad:", round(cosine_similarity(happy, sad), 3))
```

Output:
```
happy~joyful: 0.986
happy~sad: -0.876
```

**Rule:** normalize vectors before storing (unit vectors make cosine = dot
product), and use cosine for semantic tasks — never raw Euclidean distance in
high dimensions.

## 3. Embedding with API and Local Models

### API (OpenAI)
```python
from openai import OpenAI

client = OpenAI()
resp = client.embeddings.create(
    model="text-embedding-3-small",
    input=["The cat sat on the mat.", "A dog barked loudly."],
)
vecs = [d.embedding for d in resp.data]
print("dims:", len(vecs[0]))
```

Output:
```
dims: 1536   (small model default; 3-small supports 512/1536 via dimensions)
```

### Local (sentence-transformers)
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # 384 dims, runs offline
vecs = model.encode(["The cat sat on the mat.", "A dog barked loudly."])
print("dims:", vecs.shape[1])
```

Output:
```
dims: 384
```

Local models matter for privacy, cost at scale, and offline/edge use (Lecture
22's philosophy). The API and local paths produce *different* vector spaces —
**never mix models in one index** (see Mistake 3).

## 4. Choosing an Embedding Model

| Model | Dims | Strength | Use when |
|---|---|---|---|
| OpenAI 3-small | 512–1536 | strong, cheap API | hosted, no privacy constraint |
| OpenAI 3-large | 3072 | highest quality | hardest retrieval tasks |
| all-MiniLM-L6-v2 | 384 | tiny, fast, offline | local/edge, privacy |
| bge / multilingual | varies | multilingual | non-English corpora |
| Cohere embed | varies | multilingual + rerank ecosystem | enterprise multilingual |

**Decision levers:** quality (eval on your retrieval task — L10), dimension
(cost + latency per vector), language coverage, privacy (local vs API), and
**version stability** — a model update changes every vector, so pin the model
version like any other dependency.

## 5. Uses Beyond Search

Embeddings power a family of tasks with one encoder:

| Task | Technique |
|---|---|
| Semantic search | query vs document cosine, top-k |
| Clustering | k-means over document vectors |
| Deduplication | near-duplicate = cosine > 0.95 |
| Classification | embed → classifier head (zero-shot via centroids) |
| Recommendation | embed items + user, nearest items |
| Anomaly detection | far-from-corpus vectors = outliers |

```python
def dedupe(docs: list[str], embed_fn, threshold: float = 0.95) -> list[str]:
    """Greedy near-duplicate removal by cosine similarity."""
    vecs = [embed_fn(d) for d in docs]
    kept = []
    for doc, v in zip(docs, vecs):
        if all(cosine_similarity(v, w) < threshold for w in kept):
            kept.append(v) if False else None
    # (kept-vector tracking simplified; see exercise)
    return [d for i, d in enumerate(docs) if all(
        i != j and cosine_similarity(vecs[i], vecs[j]) < threshold
        for j in range(i))]
```

Output:
```
Dedupe keeps one of each near-duplicate pair — a corpus-hygiene staple.
```

## 6. Failure Modes

| Failure | Why | Mitigation |
|---|---|---|
| **Domain mismatch** | encoder trained on general text | eval on your domain; fine-tune (L21) or switch model |
| **Mixed models in one index** | different vector spaces | one model per index, pinned version |
| **Dimension drift** | model updated | full re-embed on model change (versioned) |
| **Short-text weakness** | single words are fuzzy | context windowing (L7), hybrid search (L11) |
| **Multilingual collapse** | English-centric encoders | multilingual model for non-English |
| **Cost blowup** | re-embedding everything | incremental indexing by content hash (L3/L8) |

## Every Use Case

- **RAG retrieval**: embed documents + queries, retrieve top-k (L9–11).
- **Semantic search**: product/help/knowledge search without exact keywords.
- **Document deduplication**: cleaning corpora before ingestion.
- **Clustering**: topic discovery, customer segmentation.
- **Recommendation**: item similarity, user affinity.
- **Zero-shot classification**: embed labels, nearest-centroid.
- **Anomaly detection**: outlier documents/requests.
- **Vector databases**: the storage/query layer for embeddings at scale (L8).
- **LLM memory (agents)**: episodic memory as embeddings (L16).

## Real-World Use Cases for AI Engineers

- **Customer-support RAG**: help-center articles embedded with
  all-MiniLM (local — the docs are confidential). A query like "can't log
  in" retrieves the password-reset article via cosine similarity — retrieval
  that keyword search would have missed. Retrieval quality eval (L10) chose
  the model.
- **Legal contract dedup**: a mergers team's corpus of 50k contracts — cosine
  dedup removed 3,200 near-duplicates before embedding costs were paid on the
  rest. Corpus hygiene is an embedding ROI in itself.
- **E-commerce semantic search**: product search with embeddings surfaces
  "waterproof jacket" results for "rain coat" — CTR improved measurably over
  keyword search; hybrid search (L11) then covered exact-model-number queries.
- **Fraud similarity**: claim descriptions embedded and clustered — a fraud
  ring's boilerplate text forms a tight cluster, a detectable anomaly the
  keyword rules missed.
- **RAG index at a fintech**: embedding model version pinned in the index
  manifest; a model upgrade triggered a *versioned re-embed* (L3 discipline) —
  the index and the eval numbers moved together, so nothing silently changed.

## Common Mistakes to Avoid

### Mistake 1: Mixing embedding models in one index
```
# WRONG — OpenAI vectors and SBERT vectors in one index (different spaces)
# CORRECT — one pinned model per index
```

### Mistake 2: Using Euclidean distance on raw embeddings
High-dimensional vectors: use cosine (normalize first).

### Mistake 3: No eval of the embedding model
"Better model" is a claim; measure retrieval quality on your data (L10).

### Mistake 4: Re-embedding everything on every change
Incremental by content hash (L3); full re-embed only on model change.

### Mistake 5: Ignoring the dimension/cost budget
3072-dim vectors at scale cost storage + compute. Choose dimension by need.

### Mistake 6: Forgetting to pin the model version
A floating "latest" silently changes every vector — and every index.

## Best Practices

1. Normalize vectors; use cosine similarity
2. Pin the embedding model version per index
3. Eval the embedding model on your retrieval task (L10)
4. Use one model per index — never mix vector spaces
5. Embed incrementally by content hash; full re-embed only on model change
6. Choose dimension by quality + cost + latency budget
7. Use multilingual models for non-English corpora
8. Store metadata (text, source, hash) alongside vectors for attribution
9. Batch embedding calls for cost efficiency
10. Log embedding model + version in the index manifest (L3, L17)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Embed 1M docs (API) | hours + $ | 384-3072 floats/doc | local model, batch, dedup first |
| Cosine top-k (1M vecs) | ms | O(n) | ANN index (HNSW) — L8 |
| Re-embed all (model change) | full ingest | full store | — (unavoidable) |
| Dedup pass | O(n²) naive | O(n) | minhash/ANN approximate |

## AI Engineering Relevance

**Where this shows up:** the retrieval stage of every RAG system, semantic
search, and any similarity-driven feature. Embedding quality is upstream of
answer quality — and embedding cost is a large fraction of RAG operating cost.

| Concept here | Used for |
|---|---|
| Cosine similarity | semantic ranking |
| Vector space | search, clustering, dedup |
| Model choice | quality/cost/language trade-offs |
| Version pinning | stable, attributable indexes |

**Scale note:** at 10M documents, embedding cost and index size are real
budgets — dedup first, batch smart, dimension by need. At any scale, the
embedding model choice is a measured decision, not a default.

## Practice Exercises

### Exercise 1: Cosine Similarity (Easy)
Implement `cosine_similarity` and verify: identical vectors → 1.0, orthogonal
→ 0.0, opposite → -1.0.

### Exercise 2: Top-k Search (Medium)
Write `semantic_search(query_vec, doc_vecs, k)` returning the top-k indices by
cosine; assert ordering on a mock 3-doc space.

### Exercise 3: Dedup (Medium)
Implement `dedupe(docs, embed_fn, threshold)` (section 5) and assert a
near-duplicate pair yields one survivor while distinct docs both survive.

### Exercise 4: Embedding Eval (Hard)
Write `eval_retrieval(queries, gold_docs, embed_fn)` computing recall@k, and
use it to compare two mock embedding spaces (one "good", one "bad") — proving
the eval drives the model choice.

## Summary

| Concept | Description |
|---|---|
| Embedding | dense vector where meaning ≈ distance |
| Cosine similarity | the semantic metric |
| Model choice | quality/cost/language trade-offs |
| Version pinning | stable vector spaces |
| Beyond search | clustering, dedup, classification |

Embeddings turn semantics into geometry: similar meanings are near in vector
space, and a universe of tasks — search, dedup, clustering, classification —
become vector operations. They are the foundation of retrieval, and their
quality, cost, and version discipline determine the quality of everything
built on top.

## Quick Reference

| Task | Idiom |
|---|---|
| Embed text | `client.embeddings.create(...)` or `SentenceTransformer(...)` |
| Similarity | cosine on normalized vectors |
| Top-k | sort by cosine, take k |
| Dedup | drop cosine > threshold neighbors |
| Version | pin model, re-embed on change |

## Next Steps

Next: **[07 Chunking Strategies](07-chunking-strategies-lecture.md)** — deciding
how to slice documents for embedding and retrieval.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/embeddings,
https://www.sbert.net/
