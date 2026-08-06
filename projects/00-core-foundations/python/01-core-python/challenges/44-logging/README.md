# Challenge 44: Logging

## 🥉 Bronze — Level Ranker (~15 min)

**Task:** Implement `level_rank(level_name: str) -> int` mapping logging level
names to their numeric rank, and `should_log(configured: str, event: str) -> bool`
returning True when `event` meets the configured threshold.

**Signature:**
```python
def level_rank(level_name: str) -> int: ...
def should_log(configured: str, event: str) -> bool: ...
```

| Input | Expected |
|-------|----------|
| `level_rank("DEBUG")` | `10` |
| `level_rank("WARNING")` | `30` |
| `should_log("INFO", "DEBUG")` | `False` |
| `should_log("WARNING", "ERROR")` | `True` |

**Constraints:** n ≤ 10^3. Any correct approach passes.

---

## 🥈 Silver — Logger Factory (~35 min)

**Task:** Implement `make_logger(name: str, level: str) -> logging.Logger` that
returns a logger with exactly one `StringIO` handler (captured output) at the
given threshold, with `propagate=False` so it does not double-print.

**Signature:**
```python
def make_logger(name: str, level: str) -> logging.Logger: ...
```

Verify: emitting INFO/WARNING/ERROR on an INFO logger captures exactly the
INFO+ records; DEBUG is dropped. Retrieve captured text via `logger.handlers[0].stream.getvalue()`.

**Constraints:** n ≤ 10^3. Must not touch real files or stderr.

---

## 🥇 Gold — Correlated Logger (~75 min)

**Task:** Implement `CorrelatedLogger(name: str, request_id: str)` wrapping
`logging.LoggerAdapter` so that every emitted record line starts with
`[<request_id>] `. Return a small object with `.info/.warning/.error` and
`.captured()` (all text emitted so far).

**Signature:**
```python
class CorrelatedLogger:
    def __init__(self, name: str, request_id: str) -> None: ...
    def info(self, msg: str) -> None: ...
    def error(self, msg: str) -> None: ...
    def captured(self) -> str: ...
```

| Action | Expected |
|--------|----------|
| `log.info("started")` | captured contains `[rid-7ac9] started` |
| `log.error("failed")` | captured contains `[rid-7ac9] failed` |

**Constraints:** 10^5 log calls; single handler; must use a `LoggerAdapter`
(or equivalent) so every line is prefixed. Verify the prefix on every line.

**Follow-up:** how do you carry the same request ID across async tasks?
(Answer: contextvars — see `02-advanced-python/04-async-await`.)

---

## Running

```bash
pytest challenges/44-logging/test_challenge.py -v
```
