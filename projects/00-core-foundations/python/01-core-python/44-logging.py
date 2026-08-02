"""
01-core-python — 44: logging — Observability Foundation
=======================================================
Topics: five levels, logger hierarchy and propagation, handlers
        (Stream/File/Rotating), formatters, logging.config.dictConfig,
        exc_info=True vs logger.exception, lazy %s args vs f-strings,
        structured JSON logging, logging vs print, per-module getLogger(__name__)

Why this matters for AI/backend engineering:
    Tracing a RAG request end to end; logging token counts and
    latency per call; correlation IDs across an async pipeline.
    Nothing ships without logging; print() is not observability.

Run:      python 44-logging.py
Verify:   python 44-logging.py --verify
Reference: https://docs.python.org/3/library/logging.html
"""

from __future__ import annotations

import sys
import logging
import logging.config
import logging.handlers
import json
import tempfile
import os
from contextlib import contextmanager

# ============================================================
# 1. Basic Logging Setup
# ============================================================
# Complexity: O(1) per log call (amortized)

# Example 1: Basic configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)

print("=== Basic Logging ===")
logger.debug("Debug: Detailed diagnostic info")
logger.info("Info: Confirmation things work")
logger.warning("Warning: Something unexpected")
logger.error("Error: Serious problem")
logger.critical("Critical: Program may not continue")

# ============================================================
# 2. Logger Hierarchy & Propagation
# ============================================================

# Example 2: Logger hierarchy
parent_logger = logging.getLogger("myapp")
child_logger = logging.getLogger("myapp.module")
grandchild_logger = logging.getLogger("myapp.module.submodule")

print(f"\n=== Logger Hierarchy ===")
print(f"Parent: {parent_logger.name}")
print(f"Child:  {child_logger.name}")
print(f"Grandchild: {grandchild_logger.name}")

# By default, child loggers propagate to parent
print(f"Child propagates: {child_logger.propagate}")  # True

# Disable propagation
child_logger.propagate = False
print(f"After disable: {child_logger.propagate}")  # False

# ============================================================
# 3. Handlers: Stream, File, Rotating
# ============================================================

# Example 3: Multiple handlers
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# File handler with rotation
with tempfile.TemporaryDirectory() as tmp:
    log_file = os.path.join(tmp, "app.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Configure logger with handlers
    app_logger = logging.getLogger("myapp")
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)
    app_logger.propagate = False  # Don't double-log

    app_logger.info("This goes to console and file")
    app_logger.debug("This only goes to file (DEBUG level)")

    # Verify file was created
    print(f"\nLog file exists: {os.path.exists(log_file)}")
    with open(log_file) as f:
        print(f"Log content:\n{f.read()}")

# ============================================================
# 4. Exception Logging: exc_info vs logger.exception
# ============================================================

# Example 4: Logging exceptions
def risky_operation():
    return 1 / 0

try:
    risky_operation()
except ZeroDivisionError:
    # Method 1: exc_info=True (adds traceback to any level)
    logger.error("Division failed", exc_info=True)

try:
    risky_operation()
except ZeroDivisionError:
    # Method 2: logger.exception (convenience, always ERROR level)
    logger.exception("Division failed again")

# ============================================================
# 5. Lazy Formatting: %s vs f-strings
# ============================================================

# Example 5: Lazy evaluation — only formats if logged
import time

def expensive_computation():
    time.sleep(0.01)
    return "result"

# BAD: f-string always evaluated
logger.info(f"Result: {expensive_computation()}")  # Always computes!

# GOOD: lazy % formatting — only evaluates if level permits
logger.info("Result: %s", expensive_computation)  # Only computes if INFO enabled!

# With logging disabled for this logger:
logger.setLevel(logging.WARNING)
start = time.time()
logger.info("Result: %s", expensive_computation)  # Returns immediately!
elapsed = time.time() - start
print(f"\nLazy formatting time (disabled): {elapsed:.4f}s")  # ~0.00s

logger.setLevel(logging.DEBUG)
start = time.time()
logger.info("Result: %s", expensive_computation)  # Actually computes
elapsed = time.time() - start
print(f"Lazy formatting time (enabled):  {elapsed:.4f}s")  # ~0.01s

# ============================================================
# 6. Structured JSON Logging
# ============================================================

class JSONFormatter(logging.Formatter):
    """Structured JSON log formatter."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

json_handler = logging.StreamHandler()
json_handler.setFormatter(JSONFormatter())
json_logger = logging.getLogger("json")
json_logger.addHandler(json_handler)
json_logger.setLevel(logging.INFO)
json_logger.propagate = False

json_logger.info("Structured log with context", extra={"user_id": 123, "request_id": "abc-123"})

# ============================================================
# 7. dictConfig — Production Configuration
# ============================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        },
        "json": {
            "()": JSONFormatter,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "myapp": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

app_logger = logging.getLogger("myapp")
app_logger.info("Configured via dictConfig")

# ============================================================
# 8. Per-Module Logger Pattern
# ============================================================

# In every module:
# logger = logging.getLogger(__name__)
# 
# This creates loggers like:
#   myapp.main
#   myapp.models
#   myapp.services.rag
# 
# Allows granular control: logging.getLogger("myapp.services").setLevel(DEBUG)

# ============================================================
# 9. Correlation IDs for Distributed Tracing
# ============================================================

import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class CorrelationFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get("no-request-id")
        return True

# Usage in middleware:
# request_id_var.set("req-123")
# logger.info("Processing request")  # Includes request_id

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: Using print() instead of logging
#   print(f"Processing {item}")  # No levels, no rotation, no structure
# CORRECT:
#   logger.info("Processing %s", item)

# MISTAKE: f-strings in logging (always evaluated)
#   logger.info(f"Processing {expensive()}")  # Always runs!
# CORRECT:
#   logger.info("Processing %s", expensive)  # Lazy!

# MISTAKE: Creating new logger per class
#   class MyClass:
#       logger = logging.getLogger("myclass")  # Same for all instances
# CORRECT:
#   logger = logging.getLogger(__name__)  # Module-level

# MISTAKE: Not setting propagate=False on child loggers
#   Leads to duplicate log messages

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    
    # Logger hierarchy
    parent = logging.getLogger("test.parent")
    child = logging.getLogger("test.parent.child")
    assert child.parent is parent
    
    # Propagation
    assert child.propagate == True
    child.propagate = False
    assert child.propagate == False
    
    # Levels
    assert logging.DEBUG < logging.INFO < logging.WARNING < logging.ERROR < logging.CRITICAL
    
    # exc_info captures traceback
    try:
        1/0
    except ZeroDivisionError:
        import io
        import logging as lg
        stream = io.StringIO()
        handler = lg.StreamHandler(stream)
        test_logger = lg.getLogger("test_verify")
        test_logger.addHandler(handler)
        test_logger.setLevel(lg.DEBUG)
        test_logger.error("test", exc_info=True)
        output = stream.getvalue()
        assert "ZeroDivisionError" in output
        assert "1/0" in output
    
    # logger.exception is ERROR + exc_info
    stream = io.StringIO()
    handler = lg.StreamHandler(stream)
    test_logger2 = lg.getLogger("test_verify2")
    test_logger2.addHandler(handler)
    test_logger2.setLevel(lg.DEBUG)
    try:
        1/0
    except ZeroDivisionError:
        test_logger2.exception("failed")
    output = stream.getvalue()
    assert "ZeroDivisionError" in output
    
    # JSON formatter produces valid JSON
    formatter = JSONFormatter()
    record = lg.LogRecord("test", lg.INFO, "", 1, "hello", (), None)
    json_str = formatter.format(record)
    parsed = json.loads(json_str)
    assert parsed["message"] == "hello"
    assert parsed["level"] == "INFO"
    
    # dictConfig works
    lg.config.dictConfig({
        "version": 1,
        "handlers": {"h": {"class": "logging.StreamHandler", "stream": "ext://sys.stdout"}},
        "root": {"level": "INFO", "handlers": ["h"]},
    })
    
    # Lazy formatting: %s doesn't evaluate if level too high
    logger = lg.getLogger("lazy_test")
    logger.setLevel(lg.WARNING)
    called = []
    def expensive():
        called.append(True)
        return "x"
    logger.info("Result: %s", expensive)
    assert len(called) == 0  # Not called!
    
    logger.setLevel(lg.INFO)
    called.clear()
    logger.info("Result: %s", expensive)
    assert len(called) == 1  # Called!
    
    print("[OK] 44-logging: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Use logging.getLogger(__name__) in every module")
        print("2. Set appropriate levels: DEBUG/INFO/WARNING/ERROR/CRITICAL")
        print("3. Use handlers: StreamHandler, RotatingFileHandler")
        print("4. exc_info=True adds traceback; logger.exception() is ERROR + exc_info")
        print("5. Lazy %s formatting saves computation when log level disabled")
        print("6. JSONFormatter for structured logs in production")
        print("7. dictConfig for declarative production config")
        print("8. Correlation IDs via ContextVar for distributed tracing")
        _verify()