"""
Challenge 01: Decorators -- Starter Code
=======================================
Fill in the function bodies. Do not modify signatures.

Every wrapper you write must use functools.wraps: FastAPI, pydantic and
LLM tool-schema generators all read __name__/__doc__/__signature__ off the
callable they are handed. An unwrapped decorator turns a documented tool
into "wrapper(*args, **kwargs)".
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

# A provider response: {"vector": tuple[float, ...], "tokens": int}
Usage = Mapping[str, Any]


class RateLimitError(RuntimeError):
    """Provider returned HTTP 429 -- retryable."""


class BadRequestError(RuntimeError):
    """Provider returned HTTP 400 -- NOT retryable, retrying just burns budget."""


# ---------------------------------------------------------------------------
# Bronze
# ---------------------------------------------------------------------------


def track_cost(price_per_1k_tokens: float) -> Callable[[Callable[..., Usage]], Callable[..., Usage]]:
    """Decorator factory: accumulate USD spend from each response's "tokens".

    The decorated callable must expose:
      - ``total_cost``  -> float, USD accumulated so far
      - ``call_count``  -> int, successful calls
      - ``cost_usd()``  -> float, the live total (a callable, not a snapshot)
      - ``reset()``     -> None, zero both counters

    A raised exception is charged nothing and must propagate unchanged.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Silver
# ---------------------------------------------------------------------------


def retry(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    retry_on: tuple[type[BaseException], ...] = (RateLimitError,),
    sleep: Callable[[float], None] = time.sleep,
) -> Callable[[F], F]:
    """Decorator factory: retry on `retry_on` with exponential backoff.

    Attempt i (1-based) that fails sleeps ``base_delay * 2 ** (i - 1)``.
    The final attempt must not sleep. Exceptions not in `retry_on` propagate
    immediately. On exhaustion, re-raise the last exception object.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Gold
# ---------------------------------------------------------------------------


def memo_cache(max_entries: int) -> Callable[[F], F]:
    """Decorator factory: bounded LRU memo keyed on (args, sorted kwargs).

    The decorated callable must expose ``cache_info() -> (hits, misses,
    currsize)`` and ``cache_clear() -> None``. Reading an entry makes it the
    most-recently-used one; eviction drops the least-recently-used.
    """
    raise NotImplementedError


def build_embedding_pipeline(
    embed: Callable[[str], Usage],
    *,
    max_entries: int,
    max_attempts: int,
    base_delay: float,
    price_per_1k_tokens: float,
    sleep: Callable[[float], None],
) -> Callable[[str], Usage]:
    """Stack memo_cache -> track_cost -> retry around `embed`.

    Returned callable must expose ``cache_info()``, ``cache_clear()`` and
    ``cost_usd()``, and must preserve ``embed``'s __name__, __doc__ and
    signature.
    """
    raise NotImplementedError
