"""Challenge 22: Asyncio Advanced — starter (signatures only)."""

from __future__ import annotations

import asyncio
from typing import Any


def run_limited(n_calls: int, limit: int) -> tuple[int, int]:
    """Run n_calls simulated API calls under Semaphore(limit).

    Return (completed, max_in_flight) where max_in_flight never exceeds
    limit and reaches it when n_calls >= limit.
    """
    raise NotImplementedError


def pipeline(items: list[str], maxsize: int) -> tuple[int, int]:
    """Producer-consumer over asyncio.Queue(maxsize=maxsize).

    Return (processed, max_observed); max_observed must be <= maxsize
    and must reach maxsize when the workload is large enough.
    """
    raise NotImplementedError


def run_batch(n: int, fail_at: int) -> tuple[int, int]:
    """TaskGroup batch where task fail_at raises ValueError.

    Return (completed, cancelled): tasks before fail_at complete, tasks
    after it are cancelled by the group, task fail_at itself fails.
    """
    raise NotImplementedError
