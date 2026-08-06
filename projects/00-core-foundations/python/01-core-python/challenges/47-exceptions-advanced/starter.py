"""
Challenge 47: Advanced Exceptions — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures or the hierarchy.
"""

from __future__ import annotations

from typing import Callable


class AIServiceError(Exception):
    """Base error for any AI-service failure. Catch this, not Exception."""


class RetryableError(AIServiceError):
    """Transient failure (429 rate limit, 503 overloaded). Safe to retry."""


class FatalError(AIServiceError):
    """Permanent failure (400 bad request). Retrying wastes money."""


class ContextWindowExceeded(FatalError):
    """Prompt too long for the model's context window."""


def classify_error(e: Exception) -> str:
    """Return 'retry' for RetryableError, 'fatal' for FatalError, else 'unknown'.

    Subclasses classify as their base (ContextWindowExceeded -> 'fatal').
    """
    raise NotImplementedError


def call_with_retry(
    fn: Callable[[], str],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.01,
) -> str:
    """Call fn, retrying ONLY RetryableError with capped exponential backoff.

    - FatalError (or any other exception) propagates immediately.
    - Delay per retry: min(base_delay * 2 ** attempt, 1.0).
    - After max_attempts retryable failures, raise the last RetryableError
      chained `from` the original (`raise ... from last_error`).
    """
    raise NotImplementedError


def gather_results(
    calls: list[Callable[[], str]],
) -> tuple[list[str], ExceptionGroup | None]:
    """Run each call exactly once; return (successes, ExceptionGroup | None).

    The group holds every failure in original order with original objects.
    None when nothing failed. Single pass, O(n) group construction.
    """
    raise NotImplementedError
