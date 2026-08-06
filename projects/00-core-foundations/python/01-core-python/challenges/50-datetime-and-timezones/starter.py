"""
Challenge 50: Datetime & Timezones — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import date, datetime


def to_utc(naive_local: datetime, zone: str) -> datetime:
    """Attach ZoneInfo(zone) to a naive local datetime; return aware UTC."""
    raise NotImplementedError


def day_buckets(timestamps: Iterable[datetime], tz: str) -> Iterator[date]:
    """Yield the local calendar date of each aware-UTC timestamp in tz.

    Must construct ZoneInfo(tz) EXACTLY once per call, and must be lazy
    (a generator, never a materialized list).
    """
    raise NotImplementedError


def schedule_stream(
    utc_start: datetime,
    tz: str,
    hour: int,
    minute: int,
) -> Iterator[datetime]:
    """Yield aware-UTC instants for local hour:minute on each day from
    the local date of utc_start, DST-safe (fold=0), infinitely, lazily."""
    raise NotImplementedError
