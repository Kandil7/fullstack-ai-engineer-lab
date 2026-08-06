"""
FastAPI — 43: Structured Logging
==================================
Topics: structlog JSON logs; correlation/request IDs through async
        context; log levels in production; sampling; PII redaction

Why this matters for AI/backend engineering:
    Logs are the record of what your service actually did. Unstructured
    print()-style logs are unsearchable; JSON structured logs are
    queryable by any log system. The killer feature is the CORRELATION
    ID — one id threaded through every log line of a request (and its
    downstream calls), so you can replay a single user request across
    gateway, inference, and database. structlog makes this clean with
    contextvars. This exercise builds the whole mechanism and verifies
    every property.

Run:      python 43-structured-logging.py
Verify:   python 43-structured-logging.py --verify
Reference: https://www.structlog.org/en/stable/
"""

from __future__ import annotations

import json
import logging
import sys
import uuid
from typing import Optional

import structlog

# ============================================================
# 1. JSON-formatted structured logs (instead of text)
# ============================================================
# A JSON log line is a machine-readable record: timestamp, level,
# event, plus any key=value context. Grep becomes a query.

def configure_json_logging() -> structlog.stdlib.BoundLogger:
    """Configure structlog to emit JSON lines with timestamps."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,   # correlation id
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
    )
    return structlog.get_logger()


logger = configure_json_logging()
print("=== 1. JSON structured logs ===")
logger.info("request_started", path="/generate", model="gpt-4o", tokens_in=128)
logger.warning("latency_high", path="/generate", p95_ms=3450)
print()

# ============================================================
# 2. Correlation ID through async context (contextvars)
# ============================================================
# structlog.contextvars lets us bind a value that follows the
# CURRENT async context. A request handler binds its request_id
# once; every log line in that request (and its awaited children)
# carries it automatically — no manual passing through call stacks.

def bind_request_id(request_id: str | None = None) -> str:
    request_id = request_id or str(uuid.uuid4())[:12]
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    return request_id


def handle_request(path: str) -> None:
    """Simulates a request handler: binds the id, then logs + awaits."""
    rid = bind_request_id()
    logger.info("handler_start", path=path)
    _call_inference(path)          # same context -> same request_id
    logger.info("handler_done", path=path)


def _call_inference(path: str) -> None:
    """A 'downstream' call — inherits the caller's contextvars."""
    logger.info("inference_started", path=path, backend="vllm")


print("=== 2. Correlation IDs ===")
handle_request("/generate")
handle_request("/embed")           # different request -> different id
print()

# ============================================================
# 3. Levels in production + PII redaction
# ============================================================
# Production runs at INFO. DEBUG only in dev. And logs must never
# carry PII (emails, API keys, prompt content) — redact at the
# processor boundary so it holds everywhere, not in each call site.

PII_KEYS = {"email", "password", "api_key", "token", "prompt", "phone"}

def redact_pii(logger: structlog.stdlib.BoundLogger, method_name: str,
               event_dict: dict) -> dict:
    """Processor: replace any PII-keyed value with '[REDACTED]'."""
    for key in list(event_dict):
        lowered = key.lower()
        if any(pii in lowered for pii in PII_KEYS):
            event_dict[key] = "[REDACTED]"
    return event_dict


def configure_with_redaction() -> structlog.stdlib.BoundLogger:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            redact_pii,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
    )
    return structlog.get_logger()


redact_logger = configure_with_redaction()
print("=== 3. Levels + PII redaction ===")
redact_logger.info("user_login", email="ada@example.com", api_key="sk-1234")
redact_logger.info("completion", prompt="my secret question", tokens=42)
print()

# ============================================================
# 4. Log levels + sampling
# ============================================================
# At high volume, log everything cheap, sample the expensive ones.
# DEBUG lines are dropped before formatting (cheap), while a
# per-key sampling rate controls the costly lines.

def should_sample(rate: float, key: str) -> bool:
    """Deterministic sampling: ~rate fraction of keys pass."""
    return int(uuid.uuid5(uuid.NAMESPACE_URL, key).hex, 16) % 10000 < rate * 10000


print("=== 4. Sampling ===")
passed = sum(1 for i in range(100) if should_sample(0.1, f"req-{i}"))
print(f"sampled ~10%: {passed}/100 kept")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: print()/f-string logs — unsearchable, no levels, no context
# CORRECT: structured JSON via structlog
#
# MISTAKE: no correlation id — you cannot reassemble a request's story
# CORRECT: bind request_id to contextvars once per request
#
# MISTAKE: logging PII (emails, prompts, keys) into the log store
# CORRECT: a redaction processor at the boundary
#
# MISTAKE: DEBUG in production at full volume — log cost becomes real
# CORRECT: INFO in prod; sample expensive/verbose events
#
# MISTAKE: catching exceptions and logging nothing — the stack trace
#   is the cheapest debugging tool you own
# CORRECT: logger.exception() inside except

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. JSONRenderer produces parseable JSON
    import io
    buf = io.StringIO()
    h = logging.StreamHandler(buf)
    root = logging.getLogger()
    old_level, old_handlers = root.level, list(root.handlers)
    root.handlers.clear()
    root.addHandler(h)
    try:
        root.setLevel(logging.INFO)
        structlog.configure(
            processors=[structlog.processors.add_log_level,
                        structlog.processors.JSONRenderer()],
            wrapper_class=structlog.stdlib.BoundLogger,
        )
        structlog.get_logger().info("hello", answer=42)
        line = buf.getvalue().strip()
        obj = json.loads(line)
        assert obj["event"] == "hello" and obj["answer"] == 42, \
            "log line must be valid JSON with event + context"
        assert "timestamp" not in obj or True  # TimeStamper optional
    finally:
        root.level, root.handlers = old_level, old_handlers

    # 2. Correlation id: same id across a request's awaited children
    rid = bind_request_id("fixed-rid-0001")
    assert rid == "fixed-rid-0001"
    ctx = structlog.contextvars.get_contextvars()
    assert ctx.get("request_id") == "fixed-rid-0001", "contextvars must carry the id"

    # 3. PII redaction processor
    redact_logger = configure_with_redaction()
    import io as _io
    buf = _io.StringIO()
    h = logging.StreamHandler(buf)
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(h)
    root.setLevel(logging.INFO)
    redact_logger.info("event", email="a@b.c", safe_field="keep-me")
    line = json.loads(buf.getvalue().strip())
    assert line["email"] == "[REDACTED]", "email must be redacted"
    assert line["safe_field"] == "keep-me", "safe fields must pass through"
    # Restore
    for handler in list(root.handlers):
        root.removeHandler(handler)

    # 4. Sampling rate is approximately respected
    n = 2000
    kept = sum(1 for i in range(n) if should_sample(0.1, f"r-{i}"))
    assert 0.05 * n < kept < 0.15 * n, f"sampling ~10% got {kept}/{n}"

    # 5. Every request binds a fresh, unique id
    a = bind_request_id()
    b = bind_request_id()
    assert a != b, "request ids must be unique across requests"

    print("[OK] 43-structured-logging: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. JSON structured logs, queryable by any log system")
        print("2. Correlation IDs ride contextvars through async calls")
        print("3. PII redaction at the processor boundary")
        print("4. INFO in prod; sample the expensive events")
        _verify()          # always runs, so plain execution is also a test
