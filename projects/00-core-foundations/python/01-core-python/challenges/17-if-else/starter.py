"""
Challenge 17: If...Else - Starter Code
======================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator

# Price per 1000 prompt tokens, in micro-dollars (1 USD == 1_000_000 micros).
TIER_RATE_MICROS: dict[str, int] = {
    "small": 200,
    "large": 3_000,
    "long-context": 4_500,
}


def choose_model(prompt_tokens: int, complexity: str) -> str:
    """Return the model tier for one request.

    Cascade order matters: the widest bound must be tested first or its branch
    becomes unreachable. See README for the exact rule order.
    """
    raise NotImplementedError


def screen_request(
    prompt: str,
    prompt_tokens: int,
    blocked_terms: set[str],
    moderate: Callable[[str], float],
) -> tuple[str, str]:
    """Return (decision, reason) for one request.

    `moderate` is a paid network call. It must be invoked at most once per
    request, and never for a request the cheap deterministic rules already
    rejected.
    """
    raise NotImplementedError


def route_stream(
    requests: Iterable[tuple[int, str]],
    budget_micros: int,
) -> Iterator[tuple[str, int]]:
    """Yield (decision, cost_micros) for each (prompt_tokens, complexity) request.

    Lazy and single-pass. Tracks remaining budget across the stream, degrading
    to the cheap tier where that is legal instead of rejecting outright.
    """
    raise NotImplementedError


def cost_micros(prompt_tokens: int, tier: str) -> int:
    """Return the ceiling cost in micro-dollars of `prompt_tokens` on `tier`.

    Integer arithmetic only -- no floats anywhere in the billing path.
    """
    raise NotImplementedError
