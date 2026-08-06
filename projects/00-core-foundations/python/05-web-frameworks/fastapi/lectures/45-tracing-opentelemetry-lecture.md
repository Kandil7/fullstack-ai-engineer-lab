# FastAPI — 45: Tracing with OpenTelemetry

## Topic Overview

Metrics say *how* the service is doing; traces say *where the time went*.
A **distributed trace** is a tree of **spans** — one root span per
request, a child span per call — connected by **context propagation**
(trace_id, span_id, parent linkage). For an async RAG pipeline, the trace
answers the question metrics cannot: "is the 2.4 s in retrieval,
embedding, or the LLM call?" **OpenTelemetry** is the standard: vendor-
neutral, with auto-instrumentation for libraries and manual spans for
your domain code. Production adds **sampling** (head sampling by
trace_id; tail sampling for the slow/failing) because traces are
expensive to store.

The mental model: a trace is a request's timeline as a tree. Each span
names a unit of work, times it, and carries attributes — the tree plus
attributes is the diagnosis.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create spans and child spans with the OpenTelemetry API.
2. Instrument an async RAG pipeline stage by stage.
3. Propagate tracing context across service boundaries.
4. Apply head/tail sampling to bound trace volume.
5. Combine auto-instrumentation with manual domain spans.

## Prerequisites

| Need | Where |
|---|---|
| Async FastAPI | `32-async-endpoints-deep-lecture.md` |
| Structured logging | `43-structured-logging-lecture.md` |
| Metrics | `44-metrics-prometheus-lecture.md` |

---

## 1. Spans

```python
with tracer.start_as_current_span("http.request") as span:
    span.set_attribute("http.path", "/generate")
    with tracer.start_as_current_span("inference.call") as child:
        child.set_attribute("model", "gpt-4o-mini")
```

A span is a named, timed unit of work with attributes. Nested contexts
make child spans; every span in the tree shares the trace_id, and each
child records its parent's span_id.

## 2. The RAG pipeline trace

The trace tree reveals where latency goes — the query metrics cannot
answer:

```python
with tracer.start_as_current_span("rag.query") as root:
    with tracer.start_as_current_span("retrieval"): ...
    with tracer.start_as_current_span("embedding"): ...
    with tracer.start_as_current_span("llm.generate"): ...
```

"2.4 s total" becomes "retrieval 300 ms, embedding 120 ms, LLM 1.9 s".
That one fact redirects the optimization from the vector store to the
model call. Span the boundaries; the boundaries are where time lives.

## 3. Context propagation

Across process boundaries the context is carried explicitly — the
`traceparent` HTTP header in practice, injected/extracted by the
propagator:

```python
carrier = {}
TraceContextTextMapPropagator().inject(carrier, context=ctx)   # caller
ctx2 = TraceContextTextMapPropagator().extract(carrier)        # callee
```

Extract at every service entry; a child that starts a *new* trace
silently breaks the story. Same discipline as correlation IDs — but
span-aware.

## 4. Sampling

Traces are expensive; sample them.

- **Head sampling** decides before the request (deterministic hash of
  trace_id vs rate) — cheap, but may drop the interesting slow ones.
- **Tail sampling** decides after — keep slow/failing traces even when
  rare.
- **Parent-based sampling** keeps a tree consistent across services
  (children follow the parent's decision).

## 5. Auto vs manual instrumentation

- **Auto**: library instrumentation creates framework spans for you
  (FastAPI, httpx, SQLAlchemy, Redis, OpenAI clients).
- **Manual**: your domain's spans — the RAG stages, the tool calls.

Production uses both: auto for the framework plumbing, manual for the
business boundaries. Auto-only loses the domain; manual-only loses the
framework.

## Common Mistakes to Avoid

### Mistake 1: Entry-span-only tracing
```python
# WRONG - one span per request; the diagnosis is hidden
# CORRECT - span every boundary call (retrieval, embed, LLM, rerank)
```

### Mistake 2: Breaking propagation
```python
# WRONG - downstream service starts a fresh trace
# CORRECT - extract traceparent at every boundary and continue
```

### Mistake 3: 100% sampling at high rps
```python
# WRONG - storage bill explodes; the interesting traces drown
# CORRECT - head sample by trace_id; tail-sample slow/failing
```

### Mistake 4: Spans without attributes
```python
# WRONG - a span with no model/endpoint is anonymous
# CORRECT - attributes make spans queryable and diagnosable
```

### Mistake 5: One layer only
```python
# WRONG - manual spans but no framework spans (or vice versa)
# CORRECT - auto for libraries + manual for the domain
```

## Best Practices

1. Span every service boundary and external call.
2. Set attributes that make spans queryable (model, endpoint, tenant).
3. Propagate context at every entry; never start a new trace silently.
4. Head-sample by trace_id; tail-sample slow/failing traces.
5. Auto-instrument the framework; hand-span the domain.
6. Keep span names in a small vocabulary for consistent queries.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Span start/end | microseconds | — |
| Attribute set | O(attrs) | — |
| Propagation | 1 header | — |
| Full sampling | storage × volume | head/tail sampling |

The compute cost of tracing is negligible; the storage cost is real —
which is exactly what sampling controls.

## AI Engineering Relevance

**Where this shows up:** RAG pipelines, agent execution loops, multi-
model gateways, and any async chain where latency has to be attributed.

| Concept here | Used for |
|---|---|
| span tree | attribution: retrieval vs embed vs LLM |
| propagation | gateway → worker → inference continuity |
| sampling | bounding cost on high-volume generation traces |
| attributes | per-model and per-tenant trace queries |
| auto+manual | framework plumbing + domain boundaries |

**Scale note:** at 10k rps, a 1% head sample is 100 traces/sec — a
bounded, queryable diagnosis stream. That is the scale answer.

## Practice Exercises

### Exercise 1: Span tree  (Difficulty: Easy)
Create root + child; assert shared trace_id and parent linkage.

### Exercise 2: RAG attribution  (Difficulty: Easy)
Instrument 3 stages; assert children fit inside the root and are named.

### Exercise 3: Propagation  (Difficulty: Medium)
Inject to a carrier, extract in a fake service; assert the trace
continues.

### Exercise 4: Head sampling  (Difficulty: Medium)
Deterministic 10% by trace_id; assert ~10% over 2k traces.

### Exercise 5: Tail sampling  (Difficulty: Hard)
Model slow/error spans; show tail sampling keeps them while head
sampling would drop them; assert the kept set.

### Exercise 6: Auto+manual wiring  (Difficulty: Hard)
Simulate an auto-instrumented HTTP call + manual domain spans in one
trace; assert both layers appear under one root.

## Summary

| Concept | Description |
|---|---|
| span | named, timed work with attributes |
| trace | the request's span tree |
| propagation | traceparent carries the tree across services |
| sampling | head by id, tail by outcome |
| auto/manual | framework spans + domain spans |

Traces turn "the service is slow" into "retrieval is slow". Instrument
the boundaries, propagate the context, and sample deliberately.

## Quick Reference

| Task | Idiom |
|---|---|
| Start span | `with tracer.start_as_current_span("name"):` |
| Attribute | `span.set_attribute("model", "gpt-4o-mini")` |
| Propagate | inject/extract via `TraceContextTextMapPropagator` |
| Head sample | hash(trace_id) vs rate |
| Auto instrument | library instrumentation packages |

## Next Steps

Next: **[46 — Health & Readiness](46-health-and-readiness-lecture.md)** —
the endpoints that let orchestrators decide your fate.

Continues in: **[47 — Resilience Patterns](47-resilience-patterns-lecture.md)** —
timeouts, retries, circuit breakers — surviving the failures traces
reveal.

Official docs:
- OpenTelemetry: https://opentelemetry.io/docs/
- OpenTelemetry Python: https://opentelemetry.io/docs/languages/python/
