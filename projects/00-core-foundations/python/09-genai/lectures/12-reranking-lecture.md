# GenAI — 12: Reranking

## Topic Overview

Reranking is the precision stage of multi-stage retrieval: after a cheap
**recall stage** surfaces a wide candidate set (top-50 via hybrid search, L11),
a stronger — but slower — **reranker** reorders those candidates by true
relevance to the *query*, returning a precise top-5. The insight: embeddings
encode approximate semantic similarity cheaply; a **cross-encoder** (or an
LLM) attends to the query–document *pair* and scores relevance far more
accurately. Recall first, precision second — the standard production pattern.

The two reranker families:

1. **Cross-encoders** (e.g. BGE-reranker, Cohere Rerank, monoBERT): score
   each (query, doc) pair jointly; the most accurate for a given size, but
   cannot pre-index (they need the query at scoring time) and cost
   per-pair compute.
2. **LLM rerankers**: an LLM ranks the candidate list directly (prompt
   "rank these by relevance"); flexible, but slower and costlier per query.

Why this matters: reranking reliably lifts retrieval quality by 5–15 points
recall/precision on hard corpora (measured on the L10 scoreboard), at the cost
of one extra stage's latency (10–100ms). It is the highest-impact
retrieval improvement after hybrid search — and it is a *measured* decision
like everything else in this phase.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the bi-encoder (embed) vs cross-encoder (pairwise) trade-off
2. Implement a rerank stage on top of hybrid recall (L11)
3. Score and reorder candidates with a cross-encoder API/local model
4. Implement an LLM-based reranker with a ranking prompt
5. Budget the added latency/cost and tune the recall-stage size
6. Measure the rerank gain with L10 metrics (and gate it in CI)
7. Know when reranking is NOT worth it (easy corpora, strict latency budgets)

## Prerequisites

| Need | Where |
|---|---|
| Multi-stage retrieval | `09-genai/lectures/11-advanced-retrieval-lecture.md` |
| Retrieval metrics | `09-genai/lectures/10-retrieval-quality-lecture.md` |
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |

## 1. Bi-Encoder vs Cross-Encoder

| | Bi-encoder (L6) | Cross-encoder (reranker) |
|---|---|---|
| Input | query alone, doc alone | (query, doc) pair together |
| Pre-indexable | yes (embed docs once) | no (query needed per pair) |
| Speed | fast, ms per query | slower, per-pair |
| Accuracy | approximate similarity | fine-grained relevance |
| Use | recall stage (L6/L11) | precision stage (rerank) |

The architecture insight: you *cannot* replace bi-encoder search with
cross-encoders at scale (every query would require scoring all docs). So you
embed-index the corpus, retrieve a wide top-50 cheaply, then pay cross-encoder
cost on only 50 pairs. The two-stage pattern is why production RAG is both
fast and precise.

## 2. The Rerank Stage

```python
def rerank(query: str, candidates: list[str], scorer) -> list[str]:
    """Score each candidate against the query; return reordered list."""
    scored = sorted(
        ((scorer(query, doc), i) for i, doc in enumerate(candidates)),
        reverse=True,
    )
    return [candidates[i] for _, i in scored]
```

Output:
```
['chunk_1102', 'chunk_0412', ...]  — reordered by true relevance
```

The `scorer` is the swappable part: a cross-encoder API, a local model, or an
LLM — the pipeline shape stays the same, which is exactly why reranking
integrates cleanly behind the retrieval interface (L9/L10).

## 3. Cross-Encoder Rerankers

### API (Cohere Rerank)
```python
import cohere
co = cohere.Client()

resp = co.rerank(
    model="rerank-multilingual-v3.0",
    query=query,
    documents=[f"{{'text': '{d}'}}" for d in candidates],
    top_n=5,
)
print([r.index for r in resp.results])
```

Output:
```
[12, 3, 40, 7, 2]  — indices of the best 5 candidates
```

### Local (sentence-transformers CrossEncoder)
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
scores = reranker.predict([(query, d) for d in candidates])
print(scores)
```

Output:
```
[3.21, -1.04, 0.87, ...]  — relevance logits; sort descending
```

Local cross-encoders are the private/offline option; API rerankers are the
managed option. Both follow the same pattern: pairwise scores → reorder.

## 4. LLM Reranking

An LLM ranks the candidate list directly. Flexible (can use domain rules,
can cite *why*), but slower and costlier — for small candidate sets or when
cross-encoders underperform:

```python
RANK_PROMPT = """Rank the following candidate documents by relevance to the
query. Output only the document numbers in order, best first, as JSON:
{"ranking": [n, ...]}.

Query: {query}

Candidates:
{numbered_docs}"""

def llm_rerank(query: str, candidates: list[str], llm_client) -> list[str]:
    import json
    numbered = "\n".join(f"{i}: {d[:200]}" for i, d in enumerate(candidates))
    raw = llm_client.complete(RANK_PROMPT.format(query=query, numbered_docs=numbered))
    order = json.loads(raw)["ranking"]
    return [candidates[i] for i in order]
```

Output:
```
['chunk_1102', 'chunk_0412', ...]  — LLM-ranked, best first
```

**Design note:** LLM reranking is where structured output (L3) is mandatory —
the ranking JSON must parse or the stage fails loudly.

## 5. Latency and Cost Budgeting

Reranking adds one stage; budget it like any other (L18 discipline):

| Reranker | Added latency | Cost per query |
|---|---|---|
| Local MiniLM cross-encoder | 10–50ms (50 pairs) | ~0 (local) |
| Cohere/API rerank | 50–200ms | per-call fee |
| LLM rerank | 0.5–2s + tokens | highest |

```python
def rerank_budget(recall_k: int, per_pair_ms: float, budget_ms: float) -> tuple[bool, int]:
    """Is the rerank stage within budget? Returns (ok, max_recall_k)."""
    max_k = int(budget_ms / per_pair_ms)
    return recall_k <= max_k, max_k

print(rerank_budget(50, 1.2, 100))
```

Output:
```
(True, 83)   — 50 pairs × 1.2ms = 60ms, within the 100ms budget
```

Tune the recall-stage `k` (L11) against the latency budget: bigger recall
sets find more true positives but cost more per query.

## 6. Measuring the Gain (L10 Discipline)

Reranking earns its place only if the L10 metrics improve:

```python
def measure_rerank_gain(before_metrics: dict, after_metrics: dict) -> dict:
    return {
        "recall_delta": round(after_metrics["recall@k"] - before_metrics["recall@k"], 3),
        "mrr_delta": round(after_metrics["mrr"] - before_metrics["mrr"], 3),
        "worth_it": after_metrics["recall@k"] >= before_metrics["recall@k"],
    }

print(measure_rerank_gain({"recall@k": 0.70, "mrr": 0.55},
                          {"recall@k": 0.84, "mrr": 0.78}))
```

Output:
```
{'recall_delta': 0.14, 'mrr_delta': 0.23, 'worth_it': True}
```

Typical rerank gains: recall@k +5–15 points, MRR +10–25 on hard corpora —
measured, never assumed. And like every retrieval change, it goes through the
CI gate (L10).

## 7. When NOT to Rerank

- **Easy corpora**: high baseline recall already — rerank adds latency with
  no measurable gain.
- **Tight latency budgets**: a 10ms p99 budget cannot afford a 60ms rerank
  stage.
- **Trivial candidate sets**: top-5 is already enough; reranking top-5 gains
  nothing.
- **Cost-sensitive high QPS**: rerank cost × QPS is real money (L18).

The honest answer is always the same: measure. If the L10 delta is noise, drop
the stage.

## Every Use Case

- **RAG precision**: the answer only gets the *right* context.
- **Legal must-find**: rerank maximizes the chance the exact clause is in the top-k.
- **E-commerce search**: "closest match" ordering beyond embedding similarity.
- **Support deflection**: fewer wrong contexts → fewer wrong answers.
- **Code search**: rerank by "does this file actually answer this"
  (cross-encoder on code pairs).
- **Agent tool selection**: rerank candidate tools/docs for the agent (L14).
- **Multilingual**: cross-encoders rerank across languages well.
- **HR/recruitment**: resume-vs-job semantic precision.

## Real-World Use Cases for AI Engineers

- **Support RAG (fintech)**: hybrid recall + Cohere Rerank lifted MRR from
  0.55 to 0.78 — the rerank stage is what makes the "I don't know" rate drop
  without hallucination; measured on the frozen eval, gated in CI.
- **Legal research**: cross-encoder rerank on the top-50 clauses maximized the
  chance the exact indemnity clause lands in the top-3 — recall@k went 0.81 →
  0.93. The added 40ms is invisible against the value of a correct citation.
- **E-commerce search**: local cross-encoder rerank on CPU (MiniLM, 20ms)
  fixed "closest match" ordering for ambiguous queries — no API cost, all
  measured.
- **HR platform**: LLM rerank of the top-10 resumes against a job description
  ("which 3 are the best fit?") — the LLM's ranking + reasoning is the
  hiring team's starting point.
- **RAG platform**: reranking is a per-corpus config (on/off, model, k) with
  the L10 gate — 20 teams get rerank benefits where the metrics justify it.

## Common Mistakes to Avoid

### Mistake 1: Reranking the whole corpus
Cross-encoders are per-pair; score only the recall stage's candidates.

### Mistake 2: Rerank without measuring
"Reranking feels better" — measure recall/MRR delta (L10) or drop it.

### Mistake 3: Ignoring the latency budget
A 200ms rerank on a 50ms p99 budget breaks the product. Budget first.

### Mistake 4: Unbounded recall-stage k
Top-500 rerank is 10x the per-query cost for marginal recall. Tune k.

### Mistake 5: LLM rerank without structured output
Unparseable ranking JSON fails the stage. Use JSON mode (L3).

### Mistake 6: Mixing reranker and embedder spaces
Reranking is a *score*, not a vector — don't store reranker "vectors" in the
embedding index.

### Mistake 7: Reranking the same candidates twice
Rerank once, on the widest affordable set — re-reranking the reranked adds cost.

## Best Practices

1. Recall wide (hybrid top-50), rerank precise (top-5) — the two-stage pattern
2. Budget the rerank stage against latency and cost (L18)
3. Measure the delta on the L10 frozen set; keep it only if it wins
4. Use cross-encoders for precision; LLM rerank when flexibility matters
5. Tune the recall-stage k against the budget
6. Gate rerank config changes in CI (L10 gate)
7. Log which reranker + candidate counts per query (L17)
8. Cache rerank results for repeated queries (L18)
9. Prefer local rerankers for privacy and cost at scale
10. A/B the reranker model choice like any other component

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Cross-encoder 50 pairs | 10-50ms | O(50) | smaller model / fewer candidates |
| API rerank | 50-200ms + fee | — | local model |
| LLM rerank | 0.5-2s + tokens | — | only for small sets |
| Rerank cache hit | ~0.1ms | O(cache) | lru on (query, candidates) |

## AI Engineering Relevance

**Where this shows up:** the precision stage of every serious RAG pipeline.
Reranking is the highest-impact retrieval upgrade after hybrid search — and
the discipline of measuring it keeps it honest.

| Concept here | Used for |
|---|---|
| Cross-encoder | fine-grained query-doc relevance |
| Two-stage | fast recall + precise rerank |
| LLM rerank | flexible ranking with reasoning |
| Measured gain | recall/MRR deltas on L10 set |

**Scale note:** at high QPS, rerank cost compounds (L18) — cache aggressively
and tune k; at any scale, a +10-point MRR gain changes the quality of every
answer the system produces.

## Practice Exercises

### Exercise 1: Rerank Core (Easy)
Implement `rerank(query, candidates, scorer)` and verify ordering follows the
mock scorer's scores.

### Exercise 2: Latency Budget (Medium)
Implement `rerank_budget(recall_k, per_pair_ms, budget_ms)` and assert the
max affordable k for a given budget.

### Exercise 3: Measure the Gain (Medium)
Implement `measure_rerank_gain` and assert `worth_it` flips when the deltas
cross zero.

### Exercise 4: Two-Stage Pipeline (Hard)
Build `multi_stage(query, recall_fn, cross_encoder, k_recall, k_final)` on a
mock corpus; assert the final top-k has higher MRR than recall alone, and
that increasing `k_recall` within budget improves it.

## Summary

| Concept | Description |
|---|---|
| Bi vs cross-encoder | cheap recall vs precise relevance |
| Two-stage | wide recall → precise rerank |
| Reranker types | cross-encoder API/local, LLM |
| Budgeting | latency/cost per stage (L18) |
| Measured | recall/MRR deltas decide keep/drop |

Reranking is the precision half of modern retrieval: a cheap wide recall
stage, then a strong pairwise scorer that puts the truly relevant chunks on
top. It reliably lifts retrieval quality 5–15 points — measured on the L10
scoreboard, budgeted for latency, and kept only where the numbers and the
cost agree.

## Quick Reference

| Task | Idiom |
|---|---|
| Rerank stage | score (query, doc) pairs → sort desc |
| Cross-encoder | `CrossEncoder("...")` or Cohere `rerank()` |
| LLM rerank | JSON ranking prompt (L3) |
| Budget | `recall_k * per_pair_ms <= budget_ms` |
| Decide | recall/MRR delta on frozen set (L10) |

## Next Steps

Next: **[13 Tool Calling](13-tool-calling-lecture.md)** — the model choosing
and invoking functions: the bridge to agents.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://cohere.com/rerank, https://www.sbert.net/examples/applications/retrieve_rerank/README.html
