# FastAPI — 43: Structured Logging

## Topic Overview

Logs are the record of what your service actually did. Text logs are
unsearchable strings; **structured logs** are machine-readable records —
`{"timestamp", "level", "event", "request_id", ...}` — that any log
system can query. The load-bearing feature is the **correlation ID**: one
id bound to the request's async context, threaded automatically through
every awaited child call, so a single user request is replayable from
gateway to inference to database. **structlog** provides the pieces
(processors, contextvars, JSON rendering). Production reality adds three
disciplines: **levels** (INFO in prod, DEBUG in dev), **sampling** (log
everything cheap, sample the expensive), and **PII redaction** at the
processor boundary — because log stores become breach records.

The mental model: a log line is an event with key=value context. The
correlation id is the join key that reassembles a request's story.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Configure structlog to emit JSON with timestamps and levels.
2. Bind a correlation ID via contextvars so children inherit it.
3. Add a PII redaction processor that holds everywhere.
4. Choose levels for production and sample expensive events.
5. Use `logger.exception()` inside except blocks.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI basics | `01-introduction.py` |
| Async context | `32-async-endpoints-deep-lecture.md` |
| Error handling | `29-error-handling-rfc9457-lecture.md` |

---

## 1. JSON logs via structlog

```python
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
)
logger = structlog.get_logger()
logger.info("request_started", path="/generate", model="gpt-4o", tokens_in=128)
```

The output is one JSON object per line: event + level + timestamp +
context. Grep-ability becomes query-ability; the same line works in
Datadog, Loki, CloudWatch, or plain `jq`.

## 2. Correlation IDs through async context

The problem: a request awaits many calls (auth, DB, inference, cache), and
each call would need the id passed by hand. `contextvars` solves it — bind
once, and every log line in the current async context carries it:

```python
def bind_request_id():
    request_id = str(uuid.uuid4())[:12]
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    return request_id
```

Middleware binds per request; handlers, services, and DB layers just log.
The id rides the context — including across `await` boundaries — so the
whole request story is one query: `request_id=<id>`.

## 3. PII redaction at the boundary

Never log emails, API keys, or prompt content. Enforce it with a
processor, not by hoping call sites remember:

```python
def redact_pii(logger, method_name, event_dict):
    for key in list(event_dict):
        if any(pii in key.lower() for pii in PII_KEYS):
            event_dict[key] = "[REDACTED]"
    return event_dict
```

A processor is the boundary — one function, applied to every line, tested
once. This is the difference between "we try not to log PII" and "PII
cannot reach the log store through this pipeline".

## 4. Levels and sampling

Production runs at INFO; DEBUG is for dev. Cost matters: at 10k rps a
verbose log line multiplies into real storage/CPU. **Sampling** keeps the
cheap lines (start/end) and drops the expensive ones probabilistically
per key — deterministic sampling (hash the key) so the same request is
sampled consistently across systems.

## Common Mistakes to Avoid

### Mistake 1: `print()` logging
```python
# WRONG - f"user {u} took {t}ms" — unsearchable, no levels
# CORRECT - logger.info("latency", user=u, ms=t)
```

### Mistake 2: No correlation ID
```python
# WRONG - a request's logs scattered with no join key
# CORRECT - bind request_id in middleware via contextvars
```

### Mistake 3: Logging PII
```python
# WRONG - logger.info("login", email=user.email)
# CORRECT - a redaction processor at the boundary
```

### Mistake 4: Catching and swallowing exceptions
```python
# WRONG - except: pass  (or log nothing)
# CORRECT - except Exception: logger.exception("handler failed")
```

### Mistake 5: DEBUG at production volume
```python
# WRONG - every token logged at 10k rps
# CORRECT - INFO in prod; sample expensive events
```

## Best Practices

1. JSON logs via structlog processors; ISO timestamps; levels.
2. Bind correlation IDs in middleware via contextvars.
3. Redact PII in a processor — one tested boundary.
4. INFO in prod; DEBUG in dev; sample the expensive.
5. `logger.exception()` in every except block.
6. Log events (what happened), not just errors (what broke).
7. Never log secrets or prompt content — redaction is not optional.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| JSON render | microseconds/line | — |
| contextvars merge | O(context) per line | — |
| PII processor | O(keys) per line | — |
| Full-volume DEBUG | storage × volume | sample / level-gate |
| Correlation id | O(1) per request | — |

Logging is nearly free per line and expensive only when volume meets
verbosity — which is what levels and sampling are for.

## AI Engineering Relevance

**Where this shows up:** LLM gateways (cost/latency per request), agent
traces (which tool calls happened), RAG pipelines (retrieval quality
signals), and any multi-service async path.

| Concept here | Used for |
|---|---|
| correlation id | replaying one generation across gateway+inference |
| structured events | per-request token counts, latencies, model ids |
| redaction | keeping prompts/keys out of the log store |
| sampling | bounding cost on high-volume inference logs |
| exception logging | capturing model-serving failures with context |

**Scale note:** at 10k rps, correlation ids turn "some requests failed"
into "request 7f3a… failed at step 3 with model x" — the difference
between an alert and a diagnosis.

## Practice Exercises

### Exercise 1: JSON line  (Difficulty: Easy)
Log an event with context; parse the line; assert event + keys survive.

### Exercise 2: Correlation inheritance  (Difficulty: Easy)
Bind an id; log from a nested call; assert both lines carry the id.

### Exercise 3: Redaction  (Difficulty: Medium)
Log PII-keyed fields; assert every one is redacted and safe fields pass.

### Exercise 4: Sampling  (Difficulty: Medium)
Deterministic 10% sampling; assert the kept fraction is ~10% across 2k
keys.

### Exercise 5: Request replay  (Difficulty: Hard)
Simulate a 3-step async request with one correlation id; collect all
lines; assert a query on the id returns exactly that request's steps.

### Exercise 6: Cost control  (Difficulty: Hard)
Model 10k rps at DEBUG vs INFO with sampling; assert the storage math
differs by an order of magnitude.

## Summary

| Concept | Description |
|---|---|
| structured logs | JSON events, queryable |
| correlation id | the join key via contextvars |
| redaction | PII stopped at the processor boundary |
| levels | INFO in prod, DEBUG in dev |
| sampling | deterministic, per-key cost control |

Logs become evidence when they are structured, correlated, and clean.
The correlation id is what turns a pile of lines into a request's story.

## Quick Reference

| Task | Idiom |
|---|---|
| Configure | `structlog.configure(processors=[...JSONRenderer()])` |
| Bind id | `bind_contextvars(request_id=rid)` |
| Inherit | contextvars auto-merge — children carry it |
| Redact | processor replacing PII keys |
| Exception | `logger.exception("msg")` |
| Sample | deterministic hash of the key vs rate |

## Next Steps

Next: **[44 — Metrics with Prometheus](44-metrics-prometheus-lecture.md)** —
the numbers that prove the service is alive and fast.

Continues in: **[45 — Tracing with OpenTelemetry](45-tracing-opentelemetry-lecture.md)** —
latency as a tree, end to end.

Official docs:
- structlog: https://www.structlog.org/en/stable/
- Python logging: https://docs.python.org/3/library/logging.html
