"""
Challenge 50: Datetime & Timezones — Tests

Runs against starter.py by default (functions raise NotImplementedError
and must FAIL). Set CHALLENGE_USE_SOLUTION=1 to validate solution.py
(expect ALL PASS).
"""

from __future__ import annotations

import importlib.util
import inspect
import os
import tracemalloc
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

_DIR = Path(__file__).parent
_TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"

_spec = importlib.util.spec_from_file_location("mod50", _DIR / f"{_TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def _call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except NotImplementedError:
        pytest.fail("Not implemented yet")


def _collect(fn, *args, **kwargs):
    try:
        return list(fn(*args, **kwargs))
    except NotImplementedError:
        pytest.fail("Not implemented yet")


def _next(it):
    try:
        return next(it)
    except NotImplementedError:
        pytest.fail("Not implemented yet")


# ---------------------------------------------------------------- Bronze


def test_to_utc_cairo_summer():
    got = _call(mod.to_utc, datetime(2026, 8, 6, 9, 0), "Africa/Cairo")
    assert got == datetime(2026, 8, 6, 6, 0, tzinfo=timezone.utc)


def test_to_utc_cairo_winter():
    got = _call(mod.to_utc, datetime(2026, 1, 6, 9, 0), "Africa/Cairo")
    assert got == datetime(2026, 1, 6, 7, 0, tzinfo=timezone.utc)


def test_to_utc_tokyo():
    got = _call(mod.to_utc, datetime(2026, 8, 6, 12, 0), "Asia/Tokyo")
    assert got == datetime(2026, 8, 6, 3, 0, tzinfo=timezone.utc)


def test_to_utc_utc_zone():
    got = _call(mod.to_utc, datetime(2026, 8, 6, 12, 0), "UTC")
    assert got == datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)


def test_to_utc_returns_aware_utc():
    got = _call(mod.to_utc, datetime(2026, 8, 6, 9, 0), "Africa/Cairo")
    assert got.tzinfo is not None
    assert got.utcoffset() == timedelta(0)


def test_to_utc_roundtrip():
    naive = datetime(2026, 8, 6, 9, 0)
    got = _call(mod.to_utc, naive, "Africa/Cairo")
    back = got.astimezone(ZoneInfo("Africa/Cairo")).replace(tzinfo=None)
    assert back == naive


# ---------------------------------------------------------------- Silver


def test_day_buckets_tokyo_same_day():
    ts = [datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)]
    assert _collect(mod.day_buckets, ts, "Asia/Tokyo") == [date(2026, 8, 6)]


def test_day_buckets_tokyo_next_day():
    ts = [datetime(2026, 8, 6, 23, 30, tzinfo=timezone.utc)]
    assert _collect(mod.day_buckets, ts, "Asia/Tokyo") == [date(2026, 8, 7)]


def test_day_buckets_ny_same_day():
    ts = [datetime(2026, 8, 6, 23, 30, tzinfo=timezone.utc)]
    assert _collect(mod.day_buckets, ts, "America/New_York") == [date(2026, 8, 6)]


def test_day_buckets_cairo_same_day():
    ts = [datetime(2026, 8, 6, 0, 0, tzinfo=timezone.utc)]
    assert _collect(mod.day_buckets, ts, "Africa/Cairo") == [date(2026, 8, 6)]


def test_day_buckets_empty():
    assert _collect(mod.day_buckets, [], "Asia/Tokyo") == []


def test_day_buckets_mixed_input():
    ts = [
        datetime(2026, 8, 6, 23, 30, tzinfo=timezone.utc),
        datetime(2026, 8, 7, 1, 0, tzinfo=timezone.utc),
        datetime(2026, 8, 7, 23, 59, tzinfo=timezone.utc),
    ]
    assert _collect(mod.day_buckets, ts, "Asia/Tokyo") == [
        date(2026, 8, 7),
        date(2026, 8, 7),
        date(2026, 8, 8),
    ]


def test_day_buckets_is_lazy_generator():
    gen = mod.day_buckets(iter([]), "Asia/Tokyo")
    assert inspect.isgenerator(gen), "day_buckets must return a generator, not a list"
    assert _collect(lambda *a, **k: gen, None) == []


def test_day_buckets_zoneinfo_constructed_once():
    """Constructing ZoneInfo per timestamp (n times) fails the guard."""
    import zoneinfo

    orig = zoneinfo.ZoneInfo
    count = {"n": 0}

    class CountingZoneInfo(orig):
        def __new__(cls, *args, **kwargs):
            count["n"] += 1
            return orig(*args, **kwargs)

    try:
        zoneinfo.ZoneInfo = CountingZoneInfo
        spec = importlib.util.spec_from_file_location(
            "mod50_fresh", _DIR / f"{_TARGET}.py"
        )
        fresh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fresh)

        n = 10_000
        ts = [datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)] * n
        out = list(fresh.day_buckets(ts, "Asia/Tokyo"))
        assert len(out) == n
        assert count["n"] == 1, (
            f"ZoneInfo constructed {count['n']} times, expected exactly 1"
        )
    finally:
        zoneinfo.ZoneInfo = orig


# ------------------------------------------------------------------ Gold


def test_schedule_tokyo_daily():
    it = _call(
        mod.schedule_stream,
        datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc),
        "Asia/Tokyo",
        9,
        0,
    )
    first = [_next(it) for _ in range(4)]
    assert first == [
        datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 8, 2, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 8, 3, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 8, 4, 0, 0, tzinfo=timezone.utc),
    ]


def test_schedule_tokyo_exact_24h():
    it = _call(
        mod.schedule_stream,
        datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc),
        "Asia/Tokyo",
        9,
        0,
    )
    prev = _next(it)
    for _ in range(20):
        cur = _next(it)
        assert cur - prev == timedelta(hours=24)
        prev = cur


def test_schedule_cairo_0930_all_days():
    """250 days crossing both 2026 Cairo DST transitions (Apr 24, Oct 29):
    every occurrence must still convert back to local 09:30. A 24h-adding
    implementation drifts to 10:30 right after the spring transition."""
    it = _call(
        mod.schedule_stream,
        datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc),
        "Africa/Cairo",
        9,
        30,
    )
    cairo = ZoneInfo("Africa/Cairo")
    for _ in range(250):
        dt = _next(it)
        assert dt.astimezone(cairo).strftime("%H:%M") == "09:30"


def test_schedule_cairo_deltas_no_drift():
    """Exactly one 23h delta (spring forward), one 25h delta (fall back),
    the rest 24h — and zero net drift over 250 days."""
    it = _call(
        mod.schedule_stream,
        datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc),
        "Africa/Cairo",
        9,
        30,
    )
    prev = _next(it)
    hist: dict[float, int] = {}
    total_hours = 0.0
    for _ in range(249):
        cur = _next(it)
        h = (cur - prev).total_seconds() / 3600.0
        hist[h] = hist.get(h, 0) + 1
        total_hours += h
        prev = cur
    assert hist.get(24.0, 0) == 247, f"24h deltas wrong: {hist}"
    assert hist.get(23.0, 0) == 1, f"spring-forward delta missing: {hist}"
    assert hist.get(25.0, 0) == 1, f"fall-back delta missing: {hist}"
    assert abs(total_hours - 249 * 24.0) < 1e-9, "net drift detected"


def test_schedule_ny_gap_day_shifts_forward():
    """02:30 on 2026-03-08 does not exist (spring forward). The stream
    must resolve it the conventional way: the instant converts back to
    03:30 EDT, i.e. 07:30 UTC, and resumes at 02:30 EDT the next day."""
    it = _call(
        mod.schedule_stream,
        datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc),
        "America/New_York",
        2,
        30,
    )
    vals = [_next(it) for _ in range(10)]
    # day 0 is the LOCAL date of utc_start: Mar 1 00:00Z is Feb 28 19:00 EST
    assert vals[0] == datetime(2026, 2, 28, 7, 30, tzinfo=timezone.utc)
    # gap day (index 8 = Mar 8): shifted forward to 03:30 EDT
    assert vals[8] == datetime(2026, 3, 8, 7, 30, tzinfo=timezone.utc)
    # next day back to 02:30 EDT
    assert vals[9] == datetime(2026, 3, 9, 6, 30, tzinfo=timezone.utc)


def test_schedule_edge_2359():
    it = _call(
        mod.schedule_stream,
        datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc),
        "Asia/Tokyo",
        23,
        59,
    )
    assert _next(it) == datetime(2026, 8, 1, 14, 59, tzinfo=timezone.utc)


def test_schedule_midnight_ny():
    it = _call(
        mod.schedule_stream,
        datetime(2026, 8, 6, 0, 0, tzinfo=timezone.utc),
        "America/New_York",
        0,
        0,
    )
    first = _next(it)
    assert first == datetime(2026, 8, 5, 4, 0, tzinfo=timezone.utc)
    assert first.astimezone(ZoneInfo("America/New_York")).strftime("%H:%M") == "00:00"


def test_schedule_is_lazy_generator():
    it = _call(
        mod.schedule_stream,
        datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc),
        "Asia/Tokyo",
        9,
        0,
    )
    assert inspect.isgenerator(it), "schedule_stream must return a generator"


def test_schedule_memory_streaming():
    """4e5 occurrences must stream in < 15 MiB of traced memory. A
    materialized list is ~22 MB+ (datetime ~48 B + list pointer each)."""
    it = _call(
        mod.schedule_stream,
        datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc),
        "Africa/Cairo",
        9,
        30,
    )
    n = 400_000
    ceiling = 15 * 1024 * 1024
    tracemalloc.start()
    for _ in range(n):
        _next(it)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < ceiling, (
        f"peak {peak / 1024 / 1024:.1f} MiB >= 15 MiB ceiling — "
        "did you materialize the stream?"
    )
