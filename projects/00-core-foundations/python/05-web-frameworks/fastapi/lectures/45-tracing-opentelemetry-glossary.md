# Tracing with OpenTelemetry — Glossary 45

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Attribute | Span | A key-value fact making a span queryable |
| Auto-instrumentation | Technique | Library hooks creating framework spans for you |
| Context | Propagation | The active trace_id/span_id state |
| Head sampling | Sampling | Deciding before the request (hash of trace_id) |
| Manual instrumentation | Technique | Your domain code's spans |
| OTel | Standard | OpenTelemetry — vendor-neutral tracing/metrics/logs |
| Parent-based sampling | Sampling | Children follow the parent's sampling decision |
| Propagation | Concept | Carrying trace context across process boundaries |
| Span | Unit | Named, timed work with attributes |
| Span tree | Concept | The request's spans with parent-child links |
| Tail sampling | Sampling | Deciding after the request (keep slow/failing) |
| trace_id | Unit | The id shared by every span of one request |
| traceparent | Wire | The HTTP header carrying propagation context |

## Detailed Definitions

### Attribute
**Definition**: A key-value fact attached to a span — model, endpoint,
tenant, status — making spans queryable and diagnosable.
**Related**: Span

### Auto-instrumentation
**Definition**: Library-provided hooks creating framework spans
automatically (FastAPI, httpx, SQLAlchemy, Redis) — the plumbing layer.
**Related**: Manual instrumentation

### Context
**Definition**: The active tracing state (trace_id, span_id, sampled
flag) carried by the current execution.
**Related**: Propagation

### Head sampling
**Definition**: Sampling decided before the request runs — a
deterministic hash of trace_id vs a rate; cheap, but may drop the slow
ones.
**Related**: Tail sampling

### Manual instrumentation
**Definition**: The spans your code creates for domain boundaries —
retrieval, embedding, LLM calls — where auto hooks cannot know the
domain.
**Related**: Auto-instrumentation

### OTel
**Definition**: OpenTelemetry — the vendor-neutral observability standard
with SDKs, exporters, and propagation for traces/metrics/logs.
**Related**: Propagation

### Parent-based sampling
**Definition**: A child service sampling consistent with the parent's
decision, so a tree stays complete or absent as a unit.
**Related**: Head sampling

### Propagation
**Definition**: Explicitly carrying trace context across process
boundaries (the `traceparent` header) so a downstream service continues
the same trace.
**Related**: traceparent

### Span
**Definition**: A named, timed unit of work with attributes — the atomic
piece of a trace.
**Related**: Span tree

### Span tree
**Definition**: A request's spans connected by parent links — the
timeline that shows where time went.
**Related**: trace_id

### Tail sampling
**Definition**: Sampling decided after the request completes — keeping
slow or failing traces even when rare, at higher cost.
**Related**: Head sampling

### trace_id
**Definition**: The id shared by every span of one request, across all
services — the tree's identity.
**Related**: Span tree

### traceparent
**Definition**: The W3C HTTP header carrying the trace context —
injected by the caller, extracted by the callee.
**Related**: Propagation

## Key Concepts Summary

### The trace lifecycle
- Start a root span per request (SERVER kind).
- Child spans per boundary call, nested via context.
- Attributes on every span (model, endpoint).
- Propagate traceparent at every service boundary.
- Sample: head by trace_id, tail by outcome.

### The layers
- Auto: framework spans.
- Manual: domain spans.
- Both, or half the story is missing.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Named, timed work — ___
2. Shared across every span of a request — ___
3. Carries context across services — ___
4. Decided before the request — ___
5. Decided after the request — ___
6. Your domain code's spans — ___
7. Library hooks creating spans — ___
8. Key-value facts on a span — ___

**Answers:** 1-span, 2-trace_id, 3-traceparent/propagation, 4-head sampling,
5-tail sampling, 6-manual instrumentation, 7-auto-instrumentation,
8-attributes
