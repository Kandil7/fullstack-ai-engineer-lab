"""
Challenge 13: Lists - Reference Solution
=========================================
"""

from __future__ import annotations


def batch_prompts(prompts: list[str], batch_size: int) -> list[list[str]]:
    """Split prompts into consecutive batches of at most `batch_size`.

    Why this approach: slicing at a stride walks the list once and copies each
    element exactly once -- O(n) total with n/batch_size slice allocations.
    The hand-rolled alternative that accumulates into a `current` list and
    flushes it is also O(n) but three times the code and one off-by-one bug
    (forgetting the trailing partial batch) away from silently dropping the
    tail of every request. The slice bound is clamped by Python for free, so
    the final short batch needs no special case.
    """
    if batch_size < 1:
        raise ValueError(f"batch_size must be >= 1, got {batch_size}")
    return [prompts[i : i + batch_size] for i in range(0, len(prompts), batch_size)]


def align_batch_results(results: list[tuple[int, str]], count: int) -> list[str]:
    """Reorder out-of-order provider results back into request order.

    Why this approach: the position is already known, so a pre-allocated
    buffer plus one indexed store per result is O(n) with zero ordering
    comparisons -- a `bytearray` of occupancy flags separates "not yet filled"
    from a legitimately empty completion. `sorted(results)` is the reflex,
    but it pays
    O(n log n) comparisons to rediscover an order it was handed: at
    n = 100_000 that is ~1.7M comparisons versus ~0. Sorting also hides
    duplicate and out-of-range positions instead of raising on them, so a
    provider that echoes the same index twice quietly drops a response.
    """
    out: list[str] = [""] * count
    seen = bytearray(count)
    filled = 0
    for pos, text in results:
        if not 0 <= pos < count:
            raise ValueError(f"position {pos} outside range(0, {count})")
        if seen[pos]:
            raise ValueError(f"duplicate position {pos}")
        seen[pos] = 1
        out[pos] = text
        filled += 1
    if filled != count:
        raise ValueError(f"expected {count} results, got {filled}")
    return out


def build_conversations(
    shared_prefix: list[dict[str, str]],
    user_prompts: list[str],
) -> list[list[dict[str, str]]]:
    """Build one conversation per user prompt: prefix messages + a user message.

    Why this approach: `list(shared_prefix)` makes a *new list* whose slots
    point at the *same* message dicts. That is the only correct middle ground
    between the two failures:

    - `conv = shared_prefix` then `conv.append(...)` aliases the caller's
      list, so every request appends to the one shared template. Request 500
      arrives carrying 499 other users' prompts -- a cross-tenant prompt leak
      and an unbounded token bill.
    - `copy.deepcopy(shared_prefix)` per conversation is safe but duplicates
      every message dict n times. At 10_000 conversations over a 40-message
      prefix that is 400_000 extra dicts (~70 MB) to hold data nobody
      mutates; sharing costs one pointer each (~3 MB).

    The appended user message is freshly constructed per conversation, so it
    is the only object a caller can mutate without touching a neighbour.
    """
    return [
        [*shared_prefix, {"role": "user", "content": prompt}] for prompt in user_prompts
    ]
