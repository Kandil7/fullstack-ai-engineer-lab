# 01-core-python — 44: Logging — Observability Starts Here

## Topic Overview

`print()` is for scratching an itch; `logging` is for running a service. The
standard-library `logging` module gives you levels, hierarchical loggers,
handlers, formatters, and rotation — the minimum viable observability stack,
with zero dependencies.

For AI and backend engineers this is the difference between "it printed
something" and "I can reconstruct what happened to request #7ac9 across three
services." A RAG request that fails needs its trace: which prompt, how many
tokens, what latency, which retriever result — all correlated by a request ID.
That starts here, with `getLogger(__name__)` and structured records.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the five levels and when to use each
2. Create module loggers with `logging.getLogger(__name__)`
3. Attach stream, file, and rotating handlers
4. Format records with timestamps, levels, and custom fields
5. Configure logging programmatically and via `dictConfig`
6. Use `logger.exception()` vs `exc_info=True` correctly
7. Explain propagation and logger hierarchy
8. Use lazy `%s` args instead of eager f-strings
9. Emit structured JSON logs for machine consumption
10. Explain why logging (not print) is the observability baseline

## Prerequisites

| Need | Where |
|------|-------|
| Modules and imports | `25-modules.py` lecture |
| Exceptions | `30-try-except.py` lecture |
| JSON | `28-json.py` lecture |

## 1. Levels — The Five-Stage Ladder

```python
import logging

logging.debug("details for local debugging")
logging.info("normal operational events")
logging.warning("something is off, but we continue")
logging.error("a request failed")
logging.critical("the process cannot continue")
```

The default level is WARNING, so `debug`/`info` are invisible until you
configure a lower threshold. Levels are a *filter*, not a style choice: logs
below the configured level cost almost nothing; logs above it may page someone.

## 2. Module Loggers — `getLogger(__name__)`

Never `logging.info(...)` from a library. Create a logger per module:

```python
import logging

logger = logging.getLogger(__name__)   # "myapp.retriever" in a package

logger.info("retrieved %d chunks in %.1f ms", 5, 12.3)
```

The name follows the package hierarchy (`myapp.retriever`), which makes
per-module level control possible: quiet the noisy `httpx` logger while keeping
your own at DEBUG.

## 3. Handlers and Formatters — Where Records Go

A logger emits records; handlers decide what happens to them. The classic
production setup: console for humans, rotating file for retention.

```python
import logging

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()                       # stderr
console.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
))
logger.addHandler(console)

rotating = logging.handlers.RotatingFileHandler(
    "outputs/logs/app.log", maxBytes=1_000_000, backupCount=3
)
logger.addHandler(rotating)
```

Duplicate records are the classic mistake here: the root logger already has a
default handler, so records propagate twice unless you set
`logger.propagate = False` or don't configure both.

## 4. `dictConfig` — Configuration as Data

Programmatic `addHandler` calls sprawl. The production pattern is one
`dictConfig` at application startup:

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "outputs/logs/app.log",
            "maxBytes": 1_000_000,
            "backupCount": 3,
            "formatter": "standard",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "INFO"},
}

logging.config.dictConfig(LOGGING_CONFIG)
```

One dict, declarative, reviewable in code review. This is the standard library's
answer to `log4j.properties`.

## 5. `logger.exception()` — The Traceback Idiom

Inside an `except` block, `logger.exception("...")` logs at ERROR and attaches
the current traceback:

```python
try:
    json.loads(raw)
except ValueError:
    logger.exception("malformed response from model")   # includes traceback
```

Outside an exception block use `logger.error("...", exc_info=True)` to get the
same traceback capture.

## 6. Lazy Formatting — `%s` Args, Not F-Strings

`logger.info("tokens=%s", n)` builds the string only if the record will be
emitted. `logger.info(f"tokens={n}")` builds it unconditionally — the cost of
formatting debug strings that will be discarded at INFO level.

```python
# EXPENSIVE at DEBUG-threshold-INFO: f-string always evaluated
logger.debug(f"chunk sizes: {[len(c) for c in chunks]}")

# LAZY: only evaluated if DEBUG is enabled
logger.debug("chunk sizes: %s", [len(c) for c in chunks])
```

## 7. Structured Logging — JSON Records

Text logs are for humans; JSON logs are for machines (and therefore for the
dashboards built by machines). Add a request/correlation ID as a field:

```python
logger.info("retrieve",
            extra={"request_id": "7ac9", "chunks": 5, "ms": 12.3})
```

With a JSON formatter each line becomes `{"level": "INFO", "message": "retrieve",
"request_id": "7ac9", ...}` — queryable in any log platform. `extra` fields are
the poor-man's structured logging that needs no third-party library.

## 8. Production Pattern — Request-Scoped Correlation

```python
class RequestAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[{self.extra['request_id']}] {msg}", kwargs

logger = RequestAdapter(logging.getLogger("rag"), {"request_id": "7ac9"})
logger.info("retrieval started")          # [7ac9] retrieval started
```

Every log line from a request carries its ID — the join key that reconstructs a
full trace from many services.

## Common Mistakes to Avoid

### Mistake 1: `print()` for production logging

```python
# WRONG — no levels, no timestamps, no rotation, no filtering
print("user logged in", user_id)
# CORRECT
logger.info("user logged in: %s", user_id)
```

### Mistake 2: configuring handlers inside a library/module import

```python
# WRONG — every importer re-configures handlers (duplicate output)
# CORRECT — libraries only create loggers; apps configure once at startup
```

### Mistake 3: duplicate log lines from propagation

```python
# WRONG — root logger has a default handler AND you added another
logger = logging.getLogger()
logger.addHandler(StreamHandler())   # now everything prints twice
# CORRECT — set logger.propagate = False, or configure only the root
```

### Mistake 4: logging sensitive data

```python
# WRONG — tokens, passwords, full prompts in logs
logger.info("prompt: %s", user_prompt_with_secrets)
# CORRECT — log metadata, redact payloads
```

### Mistake 5: logging inside hot loops at INFO

```python
# WRONG — 1M rows x 1 log line = log flooding and real disk cost
for row in rows:
    logger.info("row: %s", row)
# CORRECT — aggregate: log per batch or per shard
```

## Best Practices

1. One `getLogger(__name__)` per module; never log via the root from libraries
2. Configure once at application entry point with `dictConfig`
3. Set the default level to INFO in production, DEBUG in dev
4. Use `logger.exception()` in except blocks to capture tracebacks
5. Use lazy `%s` formatting for anything that might be filtered out
6. Add a correlation/request ID to every record
7. Log at boundaries: request in/out, retries, model calls, failures
8. Rotate files (`RotatingFileHandler`) and cap retention
9. Redact secrets; log metadata, not payloads
10. Keep log statements cheap and free of side effects

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| Record below threshold | ~free | level check short-circuits |
| Record formatted | O(message) | only if the level passes |
| Lazy `%s` args | O(1) until emission | args formatted only when emitted |
| Eager f-string | O(message) always | paid even when discarded |
| File handler | I/O per record | batch/aggregate in hot paths |
| Rotating handler | I/O + occasional rename | bounded disk usage |

**At scale:** at 1M requests/hour, one extra INFO line per request is ~10 GB of
log volume per month. Logging is a cost center — spend deliberately.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| correlation ID | tracing one RAG request across retriever + LLM + cache |
| `logger.exception` | capturing the failing model call with its traceback |
| JSON formatter | feeding Langfuse/Prometheus-style pipelines |
| token/latency fields | cost-per-request accounting in a GenAI service |
| level discipline | INFO for operational events, DEBUG for internals |

**Scale note:** when you serve 200 concurrent requests, log lines interleave;
without a request ID in every record the log is unrecoverable. The ID is the
foundation of all later observability tooling.

## Practice Exercises

### Exercise 1: Level Filter (Easy)
Configure a logger at INFO with a console handler, emit all five levels, and
verify only WARNING and above appear by default.

### Exercise 2: Module Hierarchy (Medium)
Create `app.db` and `app.retriever` loggers, set `app.retriever` to DEBUG while
`app` stays at INFO, and confirm only the retriever shows debug lines.

### Exercise 3: Correlation ID (Hard)
Implement a `LoggerAdapter` that prefixes a request ID, emit a 3-step
"retrieve -> rerank -> generate" sequence with one shared ID, and verify the
output lines are reconstructable in order.

## Summary

| Concept | Description |
|---------|-------------|
| Levels | debug < info < warning < error < critical |
| `getLogger(__name__)` | per-module named loggers in the package hierarchy |
| Handlers | where records go: console, file, rotating, network |
| `dictConfig` | declarative configuration at startup |
| `logger.exception` | log with traceback inside except blocks |
| Lazy args | `%s` formatting only when the record is emitted |
| Structured JSON | machine-readable records with correlation IDs |

Logging turns runtime behavior into queryable evidence. Every AI service — from
a RAG endpoint to a training job — ships observability or ships blind.

## Quick Reference

| Task | Idiom |
|------|-------|
| Module logger | `logging.getLogger(__name__)` |
| Log with traceback | `logger.exception("msg")` |
| Level filter | `logger.setLevel(logging.INFO)` |
| Declarative setup | `logging.config.dictConfig({...})` |
| Rotating file | `RotatingFileHandler(path, maxBytes=..., backupCount=...)` |
| Structured field | `logger.info("msg", extra={"k": v})` |
| Avoid duplicate output | `logger.propagate = False` |

## Next Steps

Next: **[45-testing-with-pytest](45-testing-with-pytest-lecture.md)** — proving behavior.
Continues in: **[02-advanced-python — 19 logging](../../02-advanced-python/lectures/19-logging-lecture.md)** (structured logging deep dive) and
**[09-genai — 17 LLM observability](../../../09-genai/lectures/17-llm-observability-lecture.md)**.
Official docs: https://docs.python.org/3/howto/logging.html
