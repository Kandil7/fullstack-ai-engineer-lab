"""
Challenge 34: Debugging Techniques — Starter
============================================
Implement all three tiers. Replace every NotImplementedError.
"""

from __future__ import annotations

import random
import traceback
from typing import Callable


# ============================================================
# Bronze: Full-Stack Logging
# ============================================================

def capture(fn: Callable[[], object]) -> str:
    """Run fn; return the full traceback string, or '' on success. O(1)."""
    raise NotImplementedError


def format_exception_text(exc: BaseException) -> str:
    """Format a caught exception with its full stack. O(1)."""
    raise NotImplementedError


# ============================================================
# Silver: Boundary-Asserting Pipeline
# ============================================================

class DebugPipeline:
    """3-stage pipeline with invariant assertions at each boundary."""

    def run(self, chunks: list[str]) -> list[str]:
        """load -> process -> emit, asserting invariants. O(n)."""
        raise NotImplementedError


# ============================================================
# Gold: Repro Harness + Config Bisect
# ============================================================

def make_repro(shuffle_seed: int) -> Callable[[list[str]], list[str]]:
    """Return a deterministic shuffler seeded with shuffle_seed. O(n)."""
    raise NotImplementedError


def bisect_bad(configs: list[str], bad_from: int) -> tuple[int, int]:
    """Find first bad index with binary search.

    Returns (first_bad_index, probes_used) where
    probes_used <= ceil(log2(n)) + 1.
    """
    raise NotImplementedError
