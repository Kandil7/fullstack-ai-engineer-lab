"""
Challenge 34: Debugging Techniques — Solution
=============================================
"""

from __future__ import annotations

import math
import random
import traceback
from typing import Callable


# ============================================================
# Bronze: Full-Stack Logging
# ============================================================

def capture(fn: Callable[[], object]) -> str:
    """Run fn; return the full traceback string, or '' on success. O(1)."""
    try:
        fn()
        return ""
    except Exception:  # noqa: BLE001 - capture is the whole point
        return traceback.format_exc()


def format_exception_text(exc: BaseException) -> str:
    """Format a caught exception with its full stack. O(1)."""
    return "".join(traceback.format_exception(
        type(exc), exc, exc.__traceback__
    ))


# ============================================================
# Silver: Boundary-Asserting Pipeline
# ============================================================

class DebugPipeline:
    """3-stage pipeline with invariant assertions at each boundary."""

    def run(self, chunks: list[str]) -> list[str]:
        """load -> process -> emit, asserting invariants. O(n)."""
        # stage 1: load — strip, assert non-empty strings
        stage1: list[str] = []
        for chunk in chunks:
            assert isinstance(chunk, str), \
                f"stage-1: chunk must be str, got {type(chunk).__name__}"
            cleaned = chunk.strip()
            assert cleaned, "stage-1: empty after strip"
            stage1.append(cleaned)

        # stage 2: process — dedupe preserving order, assert no loss
        seen: set[str] = set()
        stage2: list[str] = []
        for item in stage1:
            if item not in seen:
                seen.add(item)
                stage2.append(item)
        assert len(stage2) <= len(stage1), \
            "stage-2: item count grew"
        assert all(isinstance(x, str) and x for x in stage2), \
            "stage-2: non-string or empty output"

        # stage 3: emit — sort by length
        return sorted(stage2, key=len)


# ============================================================
# Gold: Repro Harness + Config Bisect
# ============================================================

def make_repro(shuffle_seed: int) -> Callable[[list[str]], list[str]]:
    """Return a deterministic shuffler seeded with shuffle_seed. O(n)."""
    def shuffle(items: list[str]) -> list[str]:
        rng = random.Random(shuffle_seed)
        result = items[:]
        rng.shuffle(result)
        return result

    return shuffle


def bisect_bad(configs: list[str], bad_from: int) -> tuple[int, int]:
    """Find first bad index with binary search.

    Returns (first_bad_index, probes_used) where
    probes_used <= ceil(log2(n)) + 1.
    """
    lo, hi = 0, len(configs) - 1
    probes = 0
    while lo < hi:
        mid = (lo + hi) // 2
        probes += 1
        if mid >= bad_from:      # mid is bad -> failure starts at or before
            hi = mid
        else:                    # mid is good -> failure starts after
            lo = mid + 1
    probes += 1                  # the final index check itself
    return lo, probes
