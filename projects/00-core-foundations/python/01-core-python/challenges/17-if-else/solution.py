"""
Challenge 17: If...Else - Reference Solution
============================================
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Iterator

TIER_RATE_MICROS: dict[str, int] = {
    "small": 200,
    "large": 3_000,
    "long-context": 4_500,
}

SMALL_CONTEXT_WINDOW = 100_000
LARGE_TIER_TOKENS = 8_000
HARD_REJECT_TOKENS = 200_000

_WORD_RE = re.compile(r"[a-z0-9]+")


def choose_model(prompt_tokens: int, complexity: str) -> str:
    """Return the model tier for one request.

    Why this approach: the cascade is ordered widest-bound-first, so each later
    branch only has to describe what the earlier ones did not already claim.
    Ordering is the whole lesson: put `prompt_tokens > 8_000 -> "large"` above
    the 100_000 test and the "long-context" branch becomes *unreachable* -- a
    bug no type checker catches, and one that silently truncates every
    long-document request in production. Cost is O(1) either way; correctness
    is not.
    """
    if prompt_tokens > SMALL_CONTEXT_WINDOW:
        return "long-context"
    if complexity == "hard":
        return "large"
    if prompt_tokens > LARGE_TIER_TOKENS:
        return "large"
    return "small"


def screen_request(
    prompt: str,
    prompt_tokens: int,
    blocked_terms: set[str],
    moderate: Callable[[str], float],
) -> tuple[str, str]:
    """Return (decision, reason) for one request.

    Why this approach: the cheap deterministic tests come first and each one
    returns immediately, so `moderate` -- a paid network round trip -- runs at
    most once and only for prompts that survived the free checks. The naive
    shape, `score = moderate(prompt)` at the top of the function followed by an
    if-cascade, is *equally correct* and costs one API call per request instead
    of one per surviving request: on a feed where 40% is rejected by word list
    alone that is a 40% waste of both spend and P95 latency. Calling
    `moderate(prompt)` inside two separate conditions doubles it again.
    The score is bound to a local exactly once for the same reason.
    """
    if prompt_tokens <= 0:
        return ("reject", "empty")
    if prompt_tokens > HARD_REJECT_TOKENS:
        return ("reject", "too_long")
    if blocked_terms and any(w in blocked_terms for w in _WORD_RE.findall(prompt.lower())):
        return ("reject", "blocked_term")
    score = moderate(prompt)
    if score >= 0.9:
        return ("reject", "moderation")
    if score >= 0.5:
        return ("review", "moderation")
    return ("allow", "ok")


def route_stream(
    requests: Iterable[tuple[int, str]],
    budget_micros: int,
) -> Iterator[tuple[str, int]]:
    """Yield (decision, cost_micros) for each (prompt_tokens, complexity) request.

    Why this approach: a generator threading one integer `remaining` through the
    loop is O(1) memory for any stream length -- building `[...]` over 3*10^5
    requests costs tens of MB and cannot start emitting until the last request
    has arrived, which is fatal for a router that has to answer request #1 now.
    Cost is accumulated in integer micro-dollars, never floats: 0.0002 dollars
    is not representable in binary, so a float budget drifts and eventually
    either overspends or refuses a request it could afford. The degrade-to-small
    branch is checked before rejecting because a cheaper answer beats no answer,
    but only when it is legal -- a long-context prompt does not fit the small
    model's window, so there the only options are pay or reject.
    """
    remaining = budget_micros
    for prompt_tokens, complexity in requests:
        tier = choose_model(prompt_tokens, complexity)
        cost = cost_micros(prompt_tokens, tier)
        if cost <= remaining:
            remaining -= cost
            yield (tier, cost)
            continue
        if tier == "long-context":
            yield ("rejected", 0)
            continue
        small_cost = cost_micros(prompt_tokens, "small")
        if small_cost <= remaining:
            remaining -= small_cost
            yield ("small", small_cost)
        else:
            yield ("rejected", 0)


def cost_micros(prompt_tokens: int, tier: str) -> int:
    """Return the ceiling cost in micro-dollars of `prompt_tokens` on `tier`.

    Why this approach: integer ceiling division bills whole micros and never
    under-bills, so the budget check is exact. `tokens / 1000 * rate` in floats
    would make the running total drift by a fraction of a micro per request --
    invisible at n=10, a real overspend at n=10^7.
    """
    return (prompt_tokens * TIER_RATE_MICROS[tier] + 999) // 1000
