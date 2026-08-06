# Logging — Glossary 44

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `logging` | Module | Standard-library event-logging system with levels and handlers |
| DEBUG | Level | Detailed diagnostic information (usually off in production) |
| INFO | Level | Normal operational events worth recording |
| WARNING | Level | Something is off but execution continues |
| ERROR | Level | A request/operation failed; service continues |
| CRITICAL | Level | The process cannot continue safely |
| Logger | Object | Named emitter that filters records by level |
| `getLogger(__name__)` | Idiom | Per-module logger named by the package path |
| Handler | Object | Destination for records: console, file, rotating file, socket |
| Formatter | Object | Renders a record into a text/JSON line |
| `RotatingFileHandler` | Handler | File handler that rotates at a size limit |
| `dictConfig` | Function | Declarative logging configuration via a dict |
| `logger.exception()` | Method | ERROR + current traceback; only inside except |
| `exc_info=True` | Argument | Attaches the active traceback to the record |
| Lazy formatting | Concept | `%s` args formatted only if the record is emitted |
| `extra` | Argument | Additional structured fields on a record |
| `LoggerAdapter` | Class | Wraps a logger with fixed extra context (e.g. request ID) |
| `propagate` | Attribute | Whether records bubble up to ancestor loggers |

## Detailed Definitions

### `logging`
**Definition**: The standard-library module implementing hierarchical named
loggers, level filtering, handlers, and formatters.
**Example**:
```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("ready")
```
**Related**: `Logger`, `Handler`, `Formatter`

### DEBUG
**Definition**: The lowest level; fine-grained details for local diagnosis.
**Example**:
```python
logger.debug("tensor shape: %s", x.shape)
```
**Related**: INFO, level filtering

### INFO
**Definition**: Normal, expected operational events — started, succeeded,
request count.
**Related**: DEBUG, WARNING

### WARNING
**Definition**: An anomaly that does not stop the flow: retry triggered, disk
80% full, fallback used.
**Related**: ERROR, level filtering

### ERROR
**Definition**: A concrete failure — a request 500'd, an embedding call failed
after retries — while the process keeps running.
**Related**: `logger.exception()`, CRITICAL

### CRITICAL
**Definition**: The highest level; the process is unusable and should exit or
restart.
**Related**: ERROR

### Logger
**Definition**: The object your code calls `logger.info(...)` on; it filters by
its effective level and passes records to its handlers.
**Example**:
```python
logger = logging.getLogger("rag.retriever")
logger.setLevel(logging.DEBUG)
```
**Related**: `getLogger(__name__)`, Handler

### `getLogger(__name__)`
**Definition**: The canonical way to obtain a module-scoped logger; the name
mirrors the import path, enabling per-package control.
**Example**:
```python
logger = logging.getLogger(__name__)   # e.g. "app.retriever"
```
**Related**: Logger, propagation

### Handler
**Definition**: A destination for emitted records. A logger can have several:
stderr, a file, a rotating file, syslog, a socket.
**Example**:
```python
logger.addHandler(logging.StreamHandler())
```
**Related**: `RotatingFileHandler`, `dictConfig`

### Formatter
**Definition**: Renders the record — typically timestamp, level, logger name,
message — into a line.
**Example**:
```python
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
```
**Related**: Handler, structured logging

### `RotatingFileHandler`
**Definition**: Writes to a file and rotates when it reaches `maxBytes`,
keeping `backupCount` old files.
**Example**:
```python
h = logging.handlers.RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)
```
**Related**: Handler, disk cost

### `dictConfig`
**Definition**: `logging.config.dictConfig({...})` installs loggers, handlers,
and formatters from a single declarative dict.
**Example**:
```python
import logging.config
logging.config.dictConfig({
    "version": 1,
    "handlers": {"h": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["h"], "level": "INFO"},
})
```
**Related**: Handler, Formatter

### `logger.exception()`
**Definition**: Logs at ERROR and attaches the traceback of the exception being
handled. Only meaningful inside an `except` block.
**Example**:
```python
try:
    json.loads(raw)
except ValueError:
    logger.exception("malformed response")
```
**Related**: `exc_info=True`

### `exc_info=True`
**Definition**: Argument to any logging call that attaches the current
traceback, enabling `logger.error("x", exc_info=True)` outside except blocks.
**Related**: `logger.exception()`

### Lazy formatting
**Definition**: Passing `%s` placeholders plus args; the message is formatted
only when the record actually passes the level filter.
**Example**:
```python
logger.debug("sizes: %s", [len(c) for c in chunks])   # lazy
logger.debug(f"sizes: {[len(c) for c in chunks]}")    # eager — avoid
```
**Related**: DEBUG, cost of logging

### `extra`
**Definition**: A dict merged into the record as extra attributes — the basic
mechanism for structured fields.
**Example**:
```python
logger.info("retrieve", extra={"request_id": "7ac9", "ms": 12.3})
```
**Related**: `LoggerAdapter`, JSON formatter

### `LoggerAdapter`
**Definition**: Wraps a logger, injecting fixed context (like a request ID)
into every call via `process()`.
**Example**:
```python
log = logging.LoggerAdapter(logging.getLogger("rag"), {"rid": "7ac9"})
log.info("started")   # every record carries rid=7ac9
```
**Related**: `extra`, correlation IDs

### `propagate`
**Definition**: When True (default), a record also travels to ancestor loggers
and their handlers — the usual cause of duplicate lines.
**Example**:
```python
logger.propagate = False   # stop bubbling to the root's handlers
```
**Related**: Logger, duplicate output

## Key Concepts Summary

### Level discipline
- DEBUG for internals, INFO for operations, WARNING for anomalies, ERROR for
  failures, CRITICAL for fatal
- Default threshold is WARNING until you configure otherwise

### Layout
- Libraries create loggers (`getLogger(__name__)`) but never configure handlers
- Applications configure once at startup via `dictConfig`
- Handlers (console + rotating file) and formatters attach at the app level

### Cost and safety
- Lazy `%s` args make filtered-out records nearly free
- Log volume is a real disk cost; aggregate in hot loops
- Never log secrets; redact payloads, keep metadata

### Correlation
- A request ID on every record is the join key for reconstructing traces

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `getLogger(__name__)` — ___
2. `logger.exception()` — ___
3. `RotatingFileHandler` — ___
4. `dictConfig` — ___
5. `propagate` — ___
6. Lazy formatting — ___
7. `LoggerAdapter` — ___
8. `exc_info=True` — ___

A. Logs ERROR with the active traceback
B. Bounded file rotation at a size limit
C. Module-scoped named logger
D. Declarative logging setup from one dict
E. Args formatted only if the record is emitted
F. Injects fixed context (e.g. request ID) into every record
G. Controls bubbling to ancestor loggers
H. Attaches a traceback to any logging call

**Answers:** 1-C, 2-A, 3-B, 4-D, 5-G, 6-E, 7-F, 8-H
