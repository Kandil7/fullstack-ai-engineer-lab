"""
Challenge 50: Datetime & Timezones — Reference Solution
========================================================
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


def to_utc(naive_local: datetime, zone: str) -> datetime:
    """Attach ZoneInfo(zone) to a naive local datetime; return aware UTC.

    Why this approach: replace(tzinfo=ZoneInfo(zone)) makes the naive
    datetime aware with the zone's rules (including DST for that date),
    then astimezone(timezone.utc) expresses the same instant in UTC.
    """
    return naive_local.replace(tzinfo=ZoneInfo(zone)).astimezone(timezone.utc)


def day_buckets(timestamps: Iterable[datetime], tz: str) -> Iterator[date]:
    """Yield the local calendar date of each aware-UTC timestamp in tz.

    Why this approach: the ZoneInfo is built ONCE and reused (its first
    construction reads tzdata; per-timestamp construction would be
    wasteful), and the generator yields lazily so a 10^6-item stream
    never materializes. O(1) memory, O(n) total time.
    """
    zone = ZoneInfo(tz)
    for ts in timestamps:
        yield ts.astimezone(zone).date()


def schedule_stream(
    utc_start: datetime,
    tz: str,
    hour: int,
    minute: int,
) -> Iterator[datetime]:
    """Yield aware-UTC instants for local hour:minute on each day from
    the local date of utc_start, DST-safe (fold=0), infinitely, lazily.

    Why this approach: the local date is advanced with timedelta(days=1)
    on the NAIVE side, then the zone is attached (fold=0 default), then
    converted to UTC. Adding 24h to the previous UTC instant would drift
    by one hour across each DST transition. This form stays at the same
    local wall time every day; gap days resolve to the shifted-forward
    time by zoneinfo's pre-transition-offset rule. O(1) per yield.
    """
    zone = ZoneInfo(tz)
    day = utc_start.astimezone(zone).date()
    while True:
        naive = datetime.combine(day, time(hour, minute))
        yield naive.replace(tzinfo=zone).astimezone(timezone.utc)
        day += timedelta(days=1)
