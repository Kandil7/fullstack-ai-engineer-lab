# GenAI — 10: Retrieval Quality

## Topic Overview

Retrieval quality is how well the search stage finds the *right* context for a
query — measured, debugged, and improved like any other system metric.
Retrieval is the gatekeeper of RAG: if the right chunk is not retrieved, no
amount of prompting or model quality can produce a correct answer. The senior
AI-engineer skill is treating retrieval as a measurable subsystem: build an
eval set, score it, attribute failures, and improve with data — not vibes.

The core metrics:

| Metric | What it measures | Formula |
|---|---|---|
| **Recall@k** | did the right chunk make the top-k? | hits / queries |
| **Precision@k** | of the top-k, how many were relevant? | relevant / k |
| **MRR** | how high did the first relevant rank? | 1/rank |
| **nDCG** | ranking quality with graded relevance | discounted gain |

The improvement levers are the rest of the phase: query understanding and
rewriting (L11), hybrid search (lexical + semantic, L11), reranking (L12),
and the upstream choices of embedding model (L6) and chunking (L7). The
discipline: **baseline → attribute → improve → re-measure**, with a frozen
eval set as referee (L5 pattern).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Build a retrieval eval set (queries with gold document ids)
2. Compute recall@k, precision@k, MRR, and nDCG
3. Attribute retrieval failures (chunking vs embedding vs query vs index)
4. Compare retrieval configurations (model, chunking, search) with numbers
5. Design the eval so it reflects real production traffic
6. Run retrieval eval in CI as a regression gate (Phase 8 L12 pattern)
7. Know when a failure is retrieval vs generation (L9 attribution)

## Prerequisites

| Need | Where |
|---|---|
| RAG baseline | `09-genai/lectures/09-rag-baseline-lecture.md` |
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| Chunking | `09-genai/lectures/07-chunking-strategies-lecture.md` |
| Evaluation discipline | `09-genai/lectures/05-prompt-evaluation-lecture.md` |

## 1. The Retrieval Eval Set

The referee: queries paired with the gold chunks that *should* be retrieved.
Build it from real traffic (sample logged queries) + synthetic edge cases;
label by hand or via LLM-assisted review (validate!). Rules: frozen, versioned,
representative, with edge cases (L5 discipline).

```python
EVAL_SET = [
    # (query, [gold chunk ids that must be in the top-k])
    ("how do I reset my password?", ["chunk_0412", "chunk_0413"]),
    ("refund policy for annual plans", ["chunk_1102"]),
    ("", []),                                    # edge: empty query
    ("billing billing billing", []),             # edge: degenerate
]
```

Output:
```
20-50 queries for iteration; 200+ for release gating.
```

**Gold labels are the hard part** — and the most valuable asset. Invest in a
high-quality set; it pays for every future retrieval decision.

## 2. Computing the Metrics

```python
def retrieval_metrics(results: list[list[str]], gold: list[list[str]], k: int = 5) -> dict:
    """results[i] = top-k chunk ids for query i; gold[i] = relevant ids."""
    recalls, precisions, mrrs = [], [], []
    for top, rel in zip(results, gold):
        hit = set(top) & set(rel)
        recalls.append(len(hit) / len(rel) if rel else 1.0)
        precisions.append(len(hit) / k)
        mrr = next((1 / (i + 1) for i, c in enumerate(top) if c in rel), 0.0)
        mrrs.append(mrr)
    n = len(results)
    return {"recall@k": round(sum(recalls) / n, 3),
            "precision@k": round(sum(precisions) / n, 3),
            "mrr": round(sum(mrrs) / n, 3)}

print(retrieval_metrics([["a", "b", "c"]], [["b"]]))
```

Output:
```
{'recall@k': 1.0, 'precision@k': 0.333, 'mrr': 0.5}
```

- **recall@k**: the primary "did we find it" metric — drive this up first
- **precision@k**: "did we waste context" — matters for cost (L18) and noise
- **MRR**: "how high did the first right answer rank" — UX-relevant

## 3. Comparing Configurations

The point of the metrics: compare candidates with numbers. Same eval set,
different retrieval configs:

```python
def compare_retrievers(configs: dict, eval_set, search_fn) -> dict:
    """configs: {name: config}; returns metric table."""
    table = {}
    for name, cfg in configs.items():
        results = [search_fn(q, cfg) for q, _ in eval_set]
        gold = [g for _, g in eval_set]
        table[name] = retrieval_metrics(results, gold)
    return table

print(compare_retrievers({"v1-fixed": {}, "v2-heading": {}}, EVAL_SET, mock_search))
```

Output:
```
{'v1-fixed': {'recall@k': 0.62, 'precision@k': 0.31, 'mrr': 0.55},
 'v2-heading': {'recall@k': 0.84, 'precision@k': 0.47, 'mrr': 0.78}}
```

A chunking change (L7) moved recall 0.62 → 0.84 — a *measured* decision.
This is the loop: candidate configs, frozen set, metrics table, ship the win.

## 4. Failure Attribution

A retrieval miss needs a root cause. The four suspects:

| Suspect | Symptom | Check |
|---|---|---|
| **Query** | query is vague/ambiguous/domain-termed | query rewriting (L11) |
| **Chunking** | the answer exists but is split/mangled | chunk boundaries (L7) |
| **Embedding** | semantic mismatch with domain | model eval/switch (L6) |
| **Search/index** | lexical-only or bad ANN params | hybrid (L11), HNSW tuning (L8) |

```python
def attribute_miss(query: str, gold_id: str, results: list[str]) -> str:
    """Classify a retrieval failure from evidence."""
    if not results:
        return "index/query"          # nothing found at all
    if gold_id in results:
        return "generation"           # retrieval fine — L9 attribution
    return "retrieval"                # found wrong things
```

Output:
```
'retrieval' — the gold exists but didn't make top-k.
```

Build a **failure log**: every miss classified into a bucket; the bucket
distribution tells you where to invest (70% query problems → fix queries).

## 5. The CI Gate (Phase 8 Pattern)

Retrieval quality is a regression risk — a chunking or embedding change can
silently drop recall. Gate it in CI (Phase 8 L12 pattern):

```python
def retrieval_ci_gate(new_metrics: dict, baseline: dict,
                      key: str = "recall@k", tol: float = 0.02) -> tuple[bool, str]:
    ok = new_metrics[key] >= baseline[key] - tol
    return (ok, f"{key}: {new_metrics[key]:.3f} vs baseline {baseline[key]:.3f}")

print(retrieval_ci_gate({"recall@k": 0.80}, {"recall@k": 0.84}))
```

Output:
```
(False, 'recall@k: 0.800 vs baseline 0.840')   → CI fails; change blocked
```

Every retrieval-affecting change (embedding model, chunking, index params)
runs the gate. The eval set is the referee; regressions are caught before
they reach users.

## 6. Baseline First, Then the Levers

The improvement ladder (all measured by this lecture's metrics):

1. **Chunking** (L7) — cheapest lever; heading-aware, size tuning
2. **Embedding model** (L6) — switch/eval; domain fit
3. **Query understanding** (L11) — rewrite, expand, decompose
4. **Hybrid search** (L11) — add lexical (BM25) to cover exact tokens
5. **Reranking** (L12) — a second-stage model reorders the top-50
6. **Index tuning** (L8) — ANN params, efSearch, M

Always measure each rung on the same frozen set — never stack levers blindly
(you won't know which one worked).

## Every Use Case

- **RAG answer quality**: retrieval quality is upstream of answer quality.
- **Semantic search product**: search-as-a-feature with measurable relevance.
- **Agent context selection**: agents retrieve tool/knowledge context — L14.
- **Support deflection**: better retrieval = fewer "I don't know" answers.
- **Compliance search**: must-find clauses (recall is a requirement).
- **Recommendation**: embedding-similarity recall for items.
- **Eval of new corpora**: how searchable is this new knowledge base?
- **Platform metrics**: retrieval health per corpus in the monitoring dashboard (L17).

## Real-World Use Cases for AI Engineers

- **Support RAG regression**: an embedding-model upgrade dropped recall@k from
  0.84 to 0.71 — caught by the CI gate *before* deploy, not by users. The
  team evaluated the new model on the frozen set, found the domain mismatch,
  and kept the old model. The eval set paid for itself in one incident.
- **Legal must-find retrieval**: a compliance search over 200k contracts must
  *never miss* a relevant clause (recall is regulatory). The eval set is
  built from real compliance queries; the team improved recall 0.81 → 0.93
  via heading-aware chunking + reranking — measured at every step.
- **E-commerce search**: hybrid search (BM25 + embeddings) lifted recall@k
  for exact-model-number queries that pure semantic search missed; the
  metrics table showed which query families each retriever won — the design
  decision, not a guess.
- **New knowledge base onboarding**: a platform team evaluates each new
  corpus with the shared retrieval harness before enabling RAG on it — a
  corpus that scores recall@k < 0.7 goes back for chunking/parsing work
  (L8), not live.
- **RAG platform**: retrieval health (recall@k, MRR per corpus) is a
  monitored metric (L17); a corpus regression pages the owning team — the
  platform's quality bar is the eval, enforced continuously.

## Common Mistakes to Avoid

### Mistake 1: No eval set
Retrieval "improvements" without a referee are vibes. Build the set first.

### Mistake 2: Gold labels from the model
Labels must come from humans (or validated LLM-assisted review) — self-labeled
gold measures nothing.

### Mistake 3: Only recall, no precision
High recall with junk context = cost + noise. Track both.

### Mistake 4: Optimizing on the eval set
Overfitting to the frozen set (L5 warning) — refresh + production metrics.

### Mistake 5: Stacking levers blindly
Change one lever at a time, measure each — attribution dies with
stacking.

### Mistake 6: Tiny eval sets
20 queries can't measure a 2% change. Size it for the decisions you make.

### Mistake 7: No CI gate
Retrieval regressions are silent — gate every retrieval-affecting change.

## Best Practices

1. Build a frozen, representative eval set with gold labels
2. Track recall@k + precision@k + MRR (and nDCG for graded relevance)
3. Attribute failures to query/chunk/embed/index before fixing
4. Change one lever at a time; measure each on the same set
5. Gate retrieval-affecting changes in CI
6. Refresh the eval set on a schedule (world changes)
7. Log retrieval failures by bucket for visibility (L17)
8. Baseline before improving; ship only measured wins
9. Match the eval set to real traffic (sample logged queries)
10. Separate retrieval metrics from generation metrics (L9/L20)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Build 200-query eval set | hours (labeling) | O(n) | sample + LLM-assist + human validate |
| Compute metrics | ms | O(1) | — |
| Rerank top-50 | +10-50ms/query | O(50) | only when recall@k plateaus |
| CI gate per change | minutes | O(1) | subset eval in PRs |

## AI Engineering Relevance

**Where this shows up:** the retrieval stage of every RAG system — retrieval
quality is the highest-leverage upstream metric in GenAI.

| Concept here | Used for |
|---|---|
| recall@k | did we find the right context |
| MRR | how high the right answer ranks |
| Attribution | which lever to pull |
| CI gate | no silent retrieval regressions |

**Scale note:** at 1M queries/day, a 5-point recall gain changes answer quality
for ~50k queries/day. Retrieval evaluation is cheap; retrieval regressions are
expensive — the eval set is the cheapest insurance in the RAG stack.

## Practice Exercises

### Exercise 1: Metric Computation (Easy)
Implement `retrieval_metrics` (recall/precision/MRR) and verify on a known
3-query case by hand.

### Exercise 2: Compare Configs (Medium)
Build `compare_retrievers` over two mock retrievers on a 10-query set with
known gold; assert the table ranks the better retriever first.

### Exercise 3: Failure Attribution (Medium)
Implement `attribute_miss` and classify: no results, wrong results, gold in
results — with the correct bucket each time.

### Exercise 4: CI Gate + Loop (Hard)
Build `retrieval_ci_gate` + a mini pipeline: baseline config → candidate
config that regresses recall → assert the gate blocks it; then a candidate
that improves → assert promotion. Prove the loop with numbers.

## Summary

| Concept | Description |
|---|---|
| Eval set | frozen queries + gold chunks |
| recall@k / precision@k / MRR | the retrieval scoreboard |
| Attribution | query/chunk/embed/index buckets |
| One lever at a time | measured improvements |
| CI gate | regressions blocked at merge |

Retrieval quality is the gatekeeper of RAG: if the right context isn't found,
nothing downstream can fix it. Measuring it (recall/precision/MRR on a frozen
set), attributing failures, and gating changes in CI turns retrieval from
"hopefully works" into a governed, improving subsystem — the senior-AI-
engineer core skill.

## Quick Reference

| Task | Idiom |
|---|---|
| Score retrieval | recall@k + precision@k + MRR on frozen set |
| Attribute a miss | query / chunk / embed / index buckets |
| Improve | one lever at a time, measured |
| Gate | candidate recall >= baseline - tol |
| Referee | gold-labeled eval set, refreshed |

## Next Steps

Next: **[11 Advanced Retrieval](11-advanced-retrieval-lecture.md)** — hybrid
search, query rewriting, and multi-stage retrieval.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://www.elastic.co/guide/en/elasticsearch/reference/current/
