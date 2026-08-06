"""Challenge 44 solution — reference implementation with reasoning comments."""
from __future__ import annotations

import io
import logging
import logging.handlers

_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def level_rank(level_name: str) -> int:
    """Map a level name to its numeric rank (10=DEBUG ... 50=CRITICAL)."""
    name = level_name.upper()
    if name not in _LEVELS:
        raise ValueError(f"unknown level: {level_name}")
    return int(_LEVELS[name])


def should_log(configured: str, event: str) -> bool:
    """True when an event at `event` level passes the `configured` threshold."""
    return level_rank(event) >= level_rank(configured)


def make_logger(name: str, level: str) -> logging.Logger:
    """Return a logger with one StringIO handler at the given threshold.

    propagate=False prevents double emission through the root logger's
    default handler — the classic duplicate-line bug.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level_rank(level))
    logger.propagate = False

    # Clear any handlers from previous calls so re-runs stay deterministic.
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    return logger


class CorrelatedLogger:
    """A logger whose every line carries a request ID prefix.

    Implemented with logging.LoggerAdapter: the extra context is injected via
    process() on every record — the production pattern for correlation IDs.
    """

    def __init__(self, name: str, request_id: str) -> None:
        self._adapter = logging.LoggerAdapter(
            make_logger(name, "INFO"),
            {"request_id": request_id},
        )
        # LoggerAdapter.process prefixes the message with the extra context.
        self._adapter.process = self._prefix  # type: ignore[method-assign]

    def _prefix(self, msg: str, kwargs):  # type: ignore[no-untyped-def]
        rid = self._adapter.extra["request_id"]
        return f"[{rid}] {msg}", kwargs

    def info(self, msg: str) -> None:
        self._adapter.info("%s", msg)

    def error(self, msg: str) -> None:
        self._adapter.error("%s", msg)

    def captured(self) -> str:
        return self._adapter.logger.handlers[0].stream.getvalue()
