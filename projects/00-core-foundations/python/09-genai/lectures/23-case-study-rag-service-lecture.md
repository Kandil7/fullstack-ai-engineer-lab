# GenAI — 23: Case Study — Production RAG Service

## Topic Overview

This lecture is the first capstone of Phase 9: a complete, production-grade
**RAG service** — from knowledge-base ingestion to a monitored, evaluated,
cost-managed answering API — integrating everything from Lectures 1–22. Where
the RAG baseline (L9) was the minimal pipeline, this case study is the *system*:
ingestion with validation and versioning (L8/L3), hybrid retrieval with
reranking (L11/L12), grounded generation with citations (L9), structured
output (L3), observability (L17), caching (L18), guardrails (L19), and an
eval harness gating every change (L20) — all on the Phase 8 assembly line
(serving L7, Docker L6, monitoring L11, CI L12).

The scenario: **"DocAnswers"** — a support knowledge-base Q&A service for a
SaaS product. We build it end to end, with the decisions at every step and the
measurements that justify them. The companion exercise
(`23-case-study-rag-service.py`) implements the core loop; this lecture is the
architect's tour.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Design a production RAG service architecture from ingestion to API
2. Wire ingestion (parse → clean → chunk → embed → index) with validation and versioning
3. Build the retrieval path (hybrid + rerank) with measured quality (L10/L12)
4. Implement grounded generation with citations and honest refusal
5. Add the production layers: observability, caching, guardrails, budgets
6. Gate changes with the eval harness in CI (L20)
7. Trace a user query through the entire system end to end

## Prerequisites

| Need | Where |
|---|---|
| All of Phase 9 | `09-genai/lectures/` (especially 7-12, 17-20) |
| Phase 8 serving | `08-mlops/lectures/07-model-serving-lecture.md` |
| Phase 8 CI | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |
| FastAPI | `05-web-frameworks/fastapi/` |

## 1. The Architecture

```
                ┌──────────────────────────────────────────────┐
 [Knowledge base] → [Ingestion: parse→clean→chunk→embed→index] │
                    (validation L10, versioning L3, hash L8)    │
                        │  (index version manifest)              │
                        ▼                                       │
 [Query] → [Guardrail input gate L19] → [Hybrid retrieval L11]  │
                        │          → [Rerank L12]               │
                        ▼          → [top-k chunks]             │
              [Cache lookup L18] —→ miss → [Grounded generation L9] │
                        │                    │  (structured output L3)
                        ▼                    ▼                    │
              [Cache store]          [Output gate L19]           │
                                             │                   │
                                             ▼                   │
                                   [FastAPI /answer L7] ← [Observability L17: trace every call]
                                             │                   │
                                             ▼                   │
                                   [Monitoring L11 + Eval L20] ──┘
```

Every layer is a Lecture; the system is the integration.

## 2. Ingestion: Versioned Knowledge

The corpus is a pipeline (L8): parse PDFs/HTML → clean → chunk (L7,
heading-aware) → embed (L6) → index (vector DB). The Phase 8 discipline: every
document is content-hashed (L3), the index carries a **version manifest**
(embedding model + chunking config + corpus version), and ingestion is
incremental — only changed docs re-embed (L8):

```python
def ingest_into_index(knowledge_base, index, *, embed_model, chunker,
                      last_index) -> dict:
    """Incremental, versioned ingestion. Returns the delta report."""
    changed = [d for d in knowledge_base
               if content_hash(d) != last_index.get(d.id)]
    new_chunks = [c for d in changed for c in chunker(d)]
    index.embed_and_store(new_chunks, model=embed_model)
    manifest = {"embed_model": embed_model, "chunker": chunker.name,
                "corpus_version": content_hash(knowledge_base)}
    index.write_manifest(manifest)          # L3: versioned, auditable
    return {"reindexed": len(changed), "chunks": len(new_chunks)}
```

Output:
```
{'reindexed': 12, 'chunks': 284}   — 12 changed docs → 284 new chunks; index
version manifest updated.
```

## 3. Retrieval: Hybrid + Rerank, Measured

The retrieval path (L11 + L12): BM25 + embeddings fused with RRF, then a
cross-encoder reranker for precision — with the quality numbers from the L10
eval driving every config choice:

```python
def retrieve(query: str, index, *, top_recall=50, top_final=5) -> list[Chunk]:
    semantic_top = index.vector_search(query, k=top_recall)    # L6
    lexical_top = index.bm25_search(query, k=top_recall)       # L11
    fused = rrf_fuse(semantic_top, lexical_top)[:top_recall]   # L11
    return rerank(query, fused, cross_encoder)[:top_final]     # L12
```

Output:
```
5 chunks — hybrid recall narrowed to 50, reranked to the best 5.
```

**Measured, always:** recall@k and MRR on the frozen retrieval suite (L10)
gate every chunking/embedding/rerank config change — the numbers from
Lectures 10-12 are the service's retrieval scoreboard.

## 4. Generation: Grounded, Cited, Structured

The generation stage (L9 + L3): a grounded prompt, answer-only-from-context
with citations, and a validated structured response:

```python
def generate_answer(query: str, chunks: list[Chunk], llm_client) -> Answer:
    context = format_chunks(chunks)                  # numbered, citable
    raw = llm_client.complete(GROUNDED_PROMPT.format(context=context, q=query))
    answer = Answer.model_validate_json(raw)         # L3: validated structure
    answer.citations = verify_citations(answer, chunks)   # L9: claims ↔ sources
    return answer                                    # typed, validated, cited
```

Output:
```
Answer(answer='Refunds take 3-5 business days [2].', citations=['chunk_1102'])
```

## 5. The Production Layers

| Layer | Lecture | What it does |
|---|---|---|
| Input guardrail | L19 | blocks policy-violating queries before retrieval |
| Output gate | L19 | blocks PII/unsafe content before the API responds |
| Cache | L18 | semantic cache for repeated queries (hit → no generation) |
| Observability | L17 | trace every call: prompt, chunks, tokens, latency, cost |
| Budgets | L18 | token/cost caps per call and per feature |
| Monitoring | L11 | refusal-rate and latency drift alerts |
| Serving | L7 | FastAPI endpoint, model-load-once, health checks |
| CI gates | L12 + L20 | eval suite gates every change |

```python
@app.post("/answer")
def answer(req: QueryRequest) -> QueryResponse:
    trace_id = req.trace_id or new_trace_id()
    allowed, reason = check_input(req.question, POLICY)      # L19
    if not allowed:
        return QueryResponse(answer=f"Blocked: {reason}", trace_id=trace_id)
    cached = cache.get(req.question)                          # L18
    if cached:
        return QueryResponse(answer=cached, trace_id=trace_id, cached=True)
    chunks = retrieve(req.question, index)                    # L11+L12
    ans = generate_answer(req.question, chunks, client)       # L9+L3
    passed, reason = check_output(ans.answer, POLICY)         # L19
    safe = ans if passed else QueryResponse(answer="Content blocked.", ...)
    cache.set(req.question, safe.answer)                      # L18
    log_trace(trace_id, req.question, chunks, ans, tokens, cost)  # L17
    return safe
```

Output:
```
POST /answer "refund policy?" → Answer(answer='Refunds take 3-5 days [2]',
                                       citations=['chunk_1102'],
                                       trace_id='tr_9f2c...')
```

## 6. The Eval Gate: Every Change Measured

The service ships changes through the eval harness (L20) — a frozen suite
covering retrieval (gold sources), groundedness (claims↔citations), refusal
honesty, and guardrail attacks:

```python
def ship_check(candidate_service, suite) -> tuple[bool, dict]:
    report = run_suite(suite, candidate_service, EVALUATORS)  # L20
    ok = (report.scores["recall@k"] >= BASELINE["recall@k"] - 0.02 and
          report.scores["groundedness"] >= BASELINE["groundedness"] - 0.02 and
          report.scores["guardrail_catch"] >= BASELINE["guardrail_catch"] - 0.02)
    return ok, report.scores
```

Output:
```
(True, {'recall@k': 0.86, 'groundedness': 0.94, 'guardrail_catch': 0.97})
— the release gate is a report, not a review meeting.
```

## 7. Operations: Monitoring and Cost

Post-launch: the L17 traces feed the L11 dashboards (latency, refusal rate,
cache hit rate) and the L18 cost dashboard (cost per answer, by feature).
A refusal-rate drift alert fired when the corpus went stale — the ops loop
(monitor → re-ingest) is part of the system, not an afterthought.

## Every Use Case

- **Support knowledge Q&A**: the exact DocAnswers shape.
- **Internal policy copilots**: HR, finance, compliance Q&A over policies.
- **Developer docs assistants**: API docs as the corpus.
- **Legal/healthcare retrieval**: private corpora, strict citations.
- **Product search enhancement**: grounded answers above search results.
- **Onboarding assistants**: new hires query the company knowledge base.
- **Multilingual support**: embeddings + generation across languages.
- **Any "answer from our documents" product**: the pattern is universal.

## Real-World Use Cases for AI Engineers

- **SaaS support (the DocAnswers origin)**: the service resolves 55% of
  tickets without an agent; the refusal-rate metric exposed knowledge gaps
  the content team filled — the eval + monitoring loop is the product.
- **Fintech policy copilot**: a compliance assistant answers policy questions
  with citations; the output gate blocks PII, and the audit trail is the
  trace log — the compliance review approved the system *because* of the
  observability.
- **Healthcare guidelines**: nurses query clinical protocols; honest refusal
  ("not in the guidelines, ask a clinician") is designed in, and the
  groundedness eval gates every prompt change.
- **Legal research assistant**: private contract corpus, strict citation
  enforcement (L9) — a claim without a citation is rejected by the output
  layer, not delivered.
- **A startup's first GenAI product**: one engineer ships DocAnswers in a
  week because every layer is a Lecture — ingestion (L8), retrieval (L11/12),
  generation (L9), gates (L20), monitoring (L11/17). The assembly line makes
  the product buildable by one person.

## Common Mistakes to Avoid

### Mistake 1: Building the generation stage before retrieval
Retrieval quality is upstream (L10) — a beautiful generator with bad chunks
answers wrong. Build and measure retrieval first.

### Mistake 2: No ingestion gates
Silent parse/chunk failures poison the index (L8). Validate ingestion.

### Mistake 3: No eval gate on changes
Every prompt/chunk/embed change is a candidate (L20). Gate them.

### Mistake 4: No caching or budgets
The service's cost per answer is a product metric (L18). Design it in.

### Mistake 5: No observability
A wrong answer with no trace is a mystery (L17). Trace everything.

### Mistake 6: Guardrails as an afterthought
Input/output gates are part of the architecture (L19), not a patch.

### Mistake 7: Skipping monitoring
A stale corpus silently degrades answers (L11). Watch refusal + drift.

## Best Practices

1. Build retrieval first, measure it (L10), then generation (L9)
2. Version the index manifest (embedding + chunking + corpus) — L3
3. Incremental ingestion by content hash (L8)
4. Grounded prompt + verified citations + honest refusal (L9)
5. Input/output guardrails in the request path (L19)
6. Semantic cache + token budgets (L18)
7. Trace every call with a trace_id (L17)
8. Eval gate every change on the frozen suite (L20)
9. Monitor refusal, latency, cache-hit, and cost (L11)
10. Serve via FastAPI with health checks (L7) and CI gates (L12)

## Complexity and Cost

| Layer | Cost | Levers |
|---|---|---|
| Ingestion | one-time + incremental | hash-based re-ingest (L8) |
| Retrieval | ms per query | hybrid + ANN (L11) |
| Generation | tokens per answer | cache + smaller model + routing (L18) |
| Eval suite | per release | subset in CI, full nightly |
| Ops | monitoring infra | L17/L11 dashboards |

## AI Engineering Relevance

**Where this shows up:** the most common production GenAI system. DocAnswers
is the template: versioned ingestion, measured retrieval, grounded generation,
and production layers (caching, guardrails, observability, eval gates) —
every layer a Lecture, every decision a measurement.

| Concept here | Used for |
|---|---|
| End-to-end integration | the whole phase in one system |
| Measured layers | retrieval/grounding/guardrail numbers |
| Production layers | cache, guardrails, traces, budgets |
| CI eval gates | quality as an automatic property |

**Scale note:** at 1M questions/day, the cache hit rate and token budget are
the P&L (L18); the eval + monitoring loop is what keeps quality from drifting
as the corpus and models change. The service is never "done" — it is
operated.

## Practice Exercises

### Exercise 1: Architecture Trace (Easy)
Draw DocAnswers' layers and state which Lecture each layer comes from; trace
a query through the full path.

### Exercise 2: Ingestion Delta (Medium)
Implement `ingest_into_index` with a mock index and last_index; assert only
changed docs re-embed and the manifest records the config.

### Exercise 3: Endpoint Flow (Medium)
Implement the `/answer` flow (input gate → cache → retrieve → generate →
output gate → cache → trace) with mocks; assert: blocked input never reaches
the model; cached queries skip generation; output-gate failures return a safe
response.

### Exercise 4: Ship Gate (Hard)
Build `ship_check` over a mini suite (retrieval + groundedness + guardrail);
assert a candidate regressing any criterion is blocked, and write the release
report.

## Summary

| Concept | Description |
|---|---|
| Versioned ingestion | hash-based, incremental, manifest |
| Measured retrieval | hybrid + rerank, gated by L10 |
| Grounded generation | citations + refusal, validated (L3) |
| Production layers | cache, guardrails, traces, budgets |
| Eval gates | every change measured (L20) |

DocAnswers is the production RAG template: every layer from the phase's
lectures, integrated on the Phase 8 assembly line, with measurements gating
every decision and production layers making it operable. Build the layers
individually, integrate them deliberately, and operate them with evals and
monitoring.

## Quick Reference

| Task | Idiom |
|---|---|
| Ingest | parse→clean→chunk→embed→index, hash-versioned |
| Retrieve | hybrid (BM25+vector) RRF → rerank top-5 |
| Generate | grounded prompt + citations + JSON (L3) |
| Protect | input/output gates (L19) |
| Operate | traces (L17), dashboards (L11), cost (L18) |
| Ship | eval gate (L20) in CI (L12) |

## Next Steps

Next: **[24 Case Study: Agent](24-case-study-agent-lecture.md)** — the
production agent system on the same assembly line.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://fastapi.tiangolo.com/, https://qdrant.tech/
