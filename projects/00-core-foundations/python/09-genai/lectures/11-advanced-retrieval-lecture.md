# GenAI — 11: Advanced Retrieval

## Topic Overview

Advanced retrieval is the toolkit you reach for when baseline vector search
(L9/L10) stops being enough: **hybrid search** (lexical + semantic), **query
understanding** (rewriting, expansion, decomposition), and **multi-stage
retrieval** (candidate generation → reranking, L12). The baseline finds
*semantic* matches; real production queries also need exact tokens (model
numbers, error codes, names), handle vague or multi-part questions, and scale
to millions of chunks. Advanced retrieval closes those gaps — measured with
the L10 metrics, always.

The three families:

1. **Hybrid search**: run BM25 (lexical) + vector search (semantic) in
   parallel, fuse the results (RRF — Reciprocal Rank Fusion, or weighted
   scores). Covers both "exact term" and "similar meaning" queries.
2. **Query understanding**: rewrite the query (spelling, domain terms),
   expand it (synonyms, related concepts), or decompose it (multi-hop into
   sub-queries).
3. **Multi-stage retrieval**: retrieve a wide candidate set cheaply (top-50),
   then rerank with a stronger model (L12) — recall first, precision second.

Why this matters: production RAG quality is a *retrieval* story more than a
*model* story. The teams that win on answer quality are the ones whose
retrieval finds the right chunks — and advanced retrieval is where the gains
live after the cheap levers (chunking, embedding) are exhausted.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Implement hybrid search with BM25 + embeddings and RRF fusion
2. Implement query rewriting (spelling, domain terminology)
3. Implement query expansion (synonyms/related terms)
4. Decompose multi-part queries into sub-queries
5. Build a multi-stage pipeline: cheap recall-first, precise rerank-second
6. Measure each technique with the L10 metrics and gate changes in CI
7. Decide when to apply each technique (hybrid always; rewriting when needed)

## Prerequisites

| Need | Where |
|---|---|
| Retrieval metrics | `09-genai/lectures/10-retrieval-quality-lecture.md` |
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| RAG baseline | `09-genai/lectures/09-rag-baseline-lecture.md` |
| Prompt engineering | `09-genai/lectures/04-prompt-engineering-lecture.md` |

## 1. Hybrid Search: Lexical + Semantic

Vector search excels at meaning ("how do I get my money back" → refunds); BM25
excels at exact terms ("REF-2049", "Django 5.0", error codes). They fail in
opposite directions — so run both and fuse.

```python
def bm25_scores(query_terms: list[str], doc_terms: list[list[str]]) -> list[float]:
    """Simplified BM25-ish: term frequency overlap per doc."""
    q = set(query_terms)
    return [sum(1 for t in q if t in set(d)) / len(q) if q else 0.0
            for d in doc_terms]

def vector_scores(q_vec, doc_vecs, sim_fn) -> list[float]:
    return [sim_fn(q_vec, d) for d in doc_vecs]
```

Output:
```
lexical: [0.5, 0.0, 1.0, 0.0]   (exact-term matches)
semantic: [0.72, 0.14, 0.65, 0.91]  (meaning matches)
```

## 2. Fusion: RRF (Reciprocal Rank Fusion)

RRF fuses two ranked lists without score normalization — robust and
simple: each doc's fused score is the sum of `1/(k + rank)` across lists.
A doc that ranks high in *both* lists wins.

```python
def rrf_fuse(*ranked_lists: list[str], k: int = 60) -> list[str]:
    """Fuse ranked lists by reciprocal rank — no score normalization needed."""
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])]

semantic_top = ["a", "b", "c"]
lexical_top = ["b", "d", "a"]
print("fused:", rrf_fuse(semantic_top, lexical_top)[:3])
```

Output:
```
fused: ['b', 'a', 'd']   (b ranked high in both → wins)
```

RRF is the industry default (Elasticsearch, Vespa) because it needs no tuning
of score scales between two very different scorers.

## 3. Query Rewriting

Queries as users type them are noisy: misspelled, underspecified, or using
terms the corpus doesn't. Rewriting (via LLM or rules) fixes the query *before*
search:

```python
REWRITE_PROMPT = """Rewrite this search query to use the terminology of our
knowledge base (which is about SaaS billing). Keep it a single search query.
Query: {q}"""

def rewrite_query(q: str, llm_client) -> str:
    """LLM rewrite: fix spelling, map to domain terms."""
    if len(q.strip()) < 3:
        return q
    return llm_client.complete(REWRITE_PROMPT.format(q=q)).strip()

print(rewrite_query("cant loggin to dashbord", mock_llm))
```

Output:
```
"how to log in to the dashboard"   (domain-mapped, spelling fixed)
```

**Caution:** rewriting adds a latency + cost step (L18) and can *hurt* —
always A/B it on the retrieval eval (L10) before keeping it. Rewrite only
when the baseline misses due to query form.

## 4. Query Expansion

Expansion adds related terms to catch documents that phrase things
differently:

```python
def expand_query(query: str, synonyms: dict[str, list[str]]) -> list[str]:
    """OR-expansion: [query terms] + [synonyms of key terms]."""
    expanded = {query}
    for term in query.lower().split():
        expanded.update(synonyms.get(term, []))
    return list(expanded)

print(expand_query("cancel plan", {"cancel": ["terminate", "end subscription"]}))
```

Output:
```
['cancel plan', 'terminate plan', 'end subscription plan']
```

Expansion raises recall (L10) at the cost of precision — measure; often
combined with hybrid + rerank (L12) to recover precision.

## 5. Multi-Hop Query Decomposition

"Does the refund policy allow refunds for the annual plan?" — the answer may
live in *two* chunks (refund policy + plan types). Decompose into sub-queries,
retrieve per sub-query, merge:

```python
DECOMPOSE_PROMPT = """Break this question into 2-3 sub-questions, each about
ONE fact, as JSON: {"sub_questions": [...]}. Question: {q}"""

def decompose_query(q: str, llm_client) -> list[str]:
    import json
    raw = llm_client.complete(DECOMPOSE_PROMPT.format(q=q))
    return json.loads(raw).get("sub_questions", [q])

print(decompose_query("Can I refund the annual plan after 30 days?", mock_llm))
```

Output:
```
['What is the annual plan refund policy?', 'What is the 30-day window rule?']
```

Retrieve for each sub-query, dedupe the chunks, then generate. This is the
entry point to agentic retrieval (L14) — when decomposition needs multiple
*steps*, not just multiple queries.

## 6. Multi-Stage Retrieval

The precision/recall two-step: **recall stage** (cheap, wide — top-50 via
hybrid), **precision stage** (rerank — L12's cross-encoder or an LLM scores
the 50). Recall first, then precision:

```python
def multi_stage(query: str, recall_fn, rerank_fn, top_recall: int = 50,
                final_k: int = 5) -> list[str]:
    """Wide recall → precise rerank."""
    candidates = recall_fn(query, top_recall)      # hybrid top-50
    return rerank_fn(query, candidates)[:final_k]  # L12 cross-encoder top-5
```

Output:
```
Recall: 50 candidates → Rerank: 5 precise → recall@k and precision@k both up.
```

This is the canonical production pattern: hybrid recall + cross-encoder
rerank. Each stage is tuned and measured independently (L10).

## Every Use Case

- **Support RAG**: hybrid catches error codes; rewriting fixes misspelled product names.
- **Legal research**: multi-hop decomposition for cross-referenced clauses.
- **E-commerce**: hybrid for exact SKUs + semantic for intent.
- **Code search**: lexical for identifiers, semantic for "how do I..."
- **Agent context**: multi-stage selection of tool/docs context (L14).
- **Enterprise search**: hybrid + rerank is the modern stack.
- **Compliance must-find**: decomposition + hybrid maximize recall.
- **Multilingual**: query rewriting to the corpus language.

## Real-World Use Cases for AI Engineers

- **SaaS support**: baseline vector search missed error-code queries
  ("E-2049"). Hybrid (BM25 + embeddings, RRF-fused) lifted recall@k from
  0.62 to 0.84 — the exact-token cases the embeddings missed were covered.
  The CI gate (L10) proved the change before shipping.
- **Legal due diligence**: "does the indemnity clause cover breach of
  confidentiality?" decomposes into two sub-queries; retrieval for each,
  merged — recall for multi-clause questions jumped 0.18. Decomposition is
  now the default for multi-fact queries.
- **Fintech search**: query rewriting maps user phrasing to the policy
  corpus's terminology ("cash out" → "withdrawal"); A/B on the eval showed
  +9% recall. Without the eval, rewriting (an added cost, L18) would have
  shipped on faith.
- **E-commerce**: hybrid + rerank is the search stack; the metrics table
  shows hybrid wins exact-SKU queries, rerank fixes "closest match" ordering
  — each stage's contribution is visible in the L10 scoreboard.
- **RAG platform**: advanced retrieval is exposed as per-corpus config
  (hybrid on/off, rewrite on/off, k values) — every config change runs the
  retrieval eval gate (L10) before deployment.

## Common Mistakes to Avoid

### Mistake 1: Hybrid without fusion care
Raw score concatenation breaks (different scales). Use RRF or normalized
fusion.

### Mistake 2: Rewriting without A/B
Rewriting adds latency + cost and can hurt. Measure on the eval set first.

### Mistake 3: Expansion without precision control
Unbounded expansion tanks precision. Measure; pair with rerank.

### Mistake 4: Decomposition for simple queries
Decompose only multi-fact queries — single-fact decomposition adds cost and
noise.

### Mistake 5: Stacking techniques unmeasured
Each technique has a cost; stack only what the L10 metrics justify.

### Mistake 6: Ignoring the recall-stage budget
top-50 with a slow rerank = latency blowup. Tune top_recall by latency (L18).

### Mistake 7: No regression gate
A hybrid/rewrite change that silently drops recall is an incident. Gate it.

## Best Practices

1. Hybrid + RRF as the default; it covers both exact and semantic
2. Measure every technique on the L10 frozen set before keeping it
3. Rewrite queries only when baseline misses are query-form issues
4. Decompose only multi-fact queries
5. Use multi-stage (recall wide, rerank precise) for precision-critical tasks
6. Budget the added latency/cost of each stage (L18)
7. Gate all retrieval changes in CI (L10 gate)
8. Log query + rewritten query + stages used for debugging (L17)
9. Tune one stage at a time
10. Keep BM25 indexes fresh (reindex on corpus change — L3)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| BM25 search | ms | O(terms) | — |
| Vector search | ms | O(n) | ANN index |
| RRF fusion | µs | O(k) | — |
| Query rewrite (LLM) | +100-500ms, +tokens | — | rule-based rewrite |
| Rerank 50 (cross-encoder) | +10-50ms | O(50) | LLM rerank (slower) |
| Decomposition (LLM) | +1 call | — | only for multi-fact |

## AI Engineering Relevance

**Where this shows up:** production RAG retrieval — the difference between
"finds the right chunk" and "hopefully finds something" is usually advanced
retrieval, not a bigger model.

| Concept here | Used for |
|---|---|
| Hybrid + RRF | exact AND semantic coverage |
| Query rewrite/expand | matching user language to the corpus |
| Decomposition | multi-fact and multi-hop questions |
| Multi-stage | recall-first, precision-second |

**Scale note:** at millions of chunks, hybrid adds a BM25 index (cheap) and
reranking is batched or cached; at any scale, every advanced technique is
*measured* — the L10 metrics are the referee that decides whether the
complexity earns its cost.

## Practice Exercises

### Exercise 1: RRF Fusion (Easy)
Implement `rrf_fuse` and verify: a doc ranked high in both lists beats one
ranked high in only one.

### Exercise 2: Hybrid Pipeline (Medium)
Build `hybrid_search(query, docs, embed_fn, sim_fn, k)` running BM25 +
vector, fusing with RRF; assert a mixed query (exact + semantic) retrieves
both the exact-term doc and the semantic doc.

### Exercise 3: Query Rewrite A/B (Medium)
Implement `rewrite_query` with a mock LLM and `compare` it against baseline
on a 10-query eval (L10 metrics) — assert the decision (keep/drop) is based
on the numbers.

### Exercise 4: Decomposition (Hard)
Build `decompose_query` + `multi_stage` and test on a two-fact query: assert
both facts' chunks are retrieved and the final top-k beats single-shot
retrieval on the eval.

## Summary

| Concept | Description |
|---|---|
| Hybrid + RRF | exact + semantic, fused robustly |
| Query rewrite | user language → corpus language |
| Expansion | recall booster, precision cost |
| Decomposition | multi-fact queries |
| Multi-stage | wide recall, precise rerank |

Advanced retrieval is where production RAG quality is won after the cheap
levers: hybrid search covers what embeddings miss, query understanding fixes
what users type, and multi-stage retrieval delivers both recall and precision.
Every technique is measured on the L10 scoreboard — complexity only earns a
place when the numbers say so.

## Quick Reference

| Task | Idiom |
|---|---|
| Fuse rankings | RRF: `sum(1/(k+rank))` |
| Hybrid | BM25 + vector → RRF |
| Rewrite | LLM domain-mapped query (A/B first) |
| Expand | OR synonyms of key terms |
| Multi-stage | hybrid top-50 → rerank top-5 (L12) |

## Next Steps

Next: **[12 Reranking](12-reranking-lecture.md)** — the precision stage:
reordering candidates with a stronger model.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://www.elastic.co/guide/en/elasticsearch/reference/current/bm25.html
