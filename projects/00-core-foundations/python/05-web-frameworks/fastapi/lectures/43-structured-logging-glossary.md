# Structured Logging — Glossary 43

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Bound logger | structlog | A logger with pre-bound context (kv pairs) |
| contextvars | Mechanism | Async-context state; rides await boundaries |
| Correlation ID | Concept | The request id joining every log line of a request |
| Event | Concept | What happened — the log line's subject |
| JSONRenderer | Processor | Emits one JSON object per log line |
| Level | Concept | Severity: DEBUG/INFO/WARNING/ERROR/CRITICAL |
| PII | Risk | Emails, keys, prompts — never log these |
| Processor | structlog | A pipeline function transforming each event |
| Redaction | Defense | Replacing PII values at the processor boundary |
| Sampling | Technique | Keeping a fraction of expensive events |
| structlog | Library | Structured logging with processor pipelines |
| TimeStamper | Processor | Adds an ISO timestamp to each event |

## Detailed Definitions

### Bound logger
**Definition**: `structlog.get_logger()` output whose context is merged
into every subsequent line — bind once, log everywhere.
**Related**: contextvars

### contextvars
**Definition**: Python's async-context local state; structlog merges it
into log lines, so a request id bound once follows all awaited children.
**Related**: Correlation ID

### Correlation ID
**Definition**: A unique id per request bound to the context — the join
key that reassembles a request's log story across services.
**Related**: contextvars

### Event
**Definition**: The subject of a log line ("request_started",
"inference_failed") — what happened, separate from its context.
**Related**: Bound logger

### JSONRenderer
**Definition**: The final structlog processor emitting one JSON object
per line, making logs queryable by any log system.
**Related**: Processor

### Level
**Definition**: The severity gate — DEBUG (dev), INFO (prod default),
WARNING/ERROR/CRITICAL — that bounds log volume and filters noise.
**Related**: Sampling

### PII
**Definition**: Personally Identifiable Information — emails, phone
numbers, API keys, prompt content. Logging it turns the log store into a
breach record.
**Related**: Redaction

### Processor
**Definition**: A structlog pipeline stage transforming each event dict —
adding level, timestamp, redacting, rendering — applied to every line.
**Related**: JSONRenderer

### Redaction
**Definition**: A processor replacing PII-keyed values with `[REDACTED]`
at the boundary — enforced everywhere, not per call site.
**Related**: PII

### Sampling
**Definition**: Deterministically keeping a fraction of expensive events
(e.g. hash the key vs a rate) to bound storage/CPU at volume.
**Related**: Level

### structlog
**Definition**: The structured-logging library providing processors,
contextvars integration, and JSON rendering.
**Related**: Processor

### TimeStamper
**Definition**: The structlog processor adding an ISO-formatted timestamp
to every event.
**Related**: Processor

## Key Concepts Summary

### The structured pipeline
- Event + key=value context → processors → one JSON line.
- Timestamp, level, correlation id merged automatically.
- Queryable: `request_id=<id>` returns a whole request's story.

### The three disciplines
- Levels: INFO in prod, DEBUG in dev.
- Sampling: log cheap, sample expensive.
- Redaction: PII stopped at the processor boundary.

### The debugging payoff
- Correlation ids turn alerts into diagnoses.
- `logger.exception()` preserves stack traces with context.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The request's join key across log lines — ___
2. Rides await boundaries — ___
3. Emits one JSON object per line — ___
4. Emails and keys — never logged — ___
5. Replaced at the processor boundary — ___
6. Keeping a fraction of events — ___
7. A pipeline stage transforming events — ___
8. Severity gate bounding volume — ___

**Answers:** 1-correlation ID, 2-contextvars, 3-JSONRenderer, 4-PII,
5-redaction, 6-sampling, 7-processor, 8-level
