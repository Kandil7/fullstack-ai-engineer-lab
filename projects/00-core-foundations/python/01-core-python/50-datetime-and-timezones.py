"""
01-core-python — 50: Datetime & Timezones — Time Is Not a String
================================================================
Topics: naive vs aware datetimes, zoneinfo.ZoneInfo, UTC storage rule,
        DST transitions and ambiguous times, ISO 8601, Unix timestamps,
        timedelta arithmetic, time.monotonic for measurement, date vs datetime

Why this matters for AI/backend engineering:
    A naive-vs-aware bug leaks the future into your training window: a model
    trained on "local" timestamps silently sees tomorrow's data. TTLs on cached
    embeddings, scheduled retraining, and per-request latency logs all break if
    time handling is wrong. Measure duration with monotonic, not wall clock.

Run:      python 50-datetime-and-timezones.py
Verify:   python 50-datetime-and-timezones.py --verify
Reference: https://docs.python.org/3/library/datetime.html
"""

from __future__ import annotations

import sys
import time
from datetime import date, datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - 3.9+ always has it
    ZoneInfo = None  # type: ignore

# ============================================================
# 1. Naive vs Aware — THE Core Distinction
# ============================================================
# Naive: no timezone attached; ambiguous wall-clock time. Aware: carries tzinfo
# (UTC offset or IANA zone). Mixing them raises TypeError — on purpose.

# Example 1: the two kinds
naive = datetime(2026, 8, 6, 12, 0, 0)
aware_utc = datetime(2026, 8, 6, 12, 0, 0, tzinfo=timezone.utc)
print(f"naive:      {naive}  tzinfo={naive.tzinfo}")
print(f"aware UTC:  {aware_utc}  tzinfo={aware_utc.tzinfo}")

try:
    naive - aware_utc
except TypeError as e:
    print(f"mixed arithmetic -> TypeError: {e}")

# Output:
# naive:      2026-08-06 12:00:00  tzinfo=None
# aware UTC:  2026-08-06 12:00:00+00:00  tzinfo=datetime.timezone.utc
# mixed arithmetic -> TypeError: can't subtract offset-naive and offset-aware datetimes

# ============================================================
# 2. The Storage Rule: Always UTC
# ============================================================
# Store UTC. Convert to local zones only at the display boundary. `utcnow()`
# is deprecated (returns naive); use now(timezone.utc) which returns aware.

# Example 2: correct way to get "now"
now_utc = datetime.now(timezone.utc)
print(f"\nnow(timezone.utc): {now_utc}  (aware: {now_utc.tzinfo is not None})")

# Example 3: IANA zones via zoneinfo
cairo = ZoneInfo("Africa/Cairo")
tokyo = ZoneInfo("Asia/Tokyo")
meeting_utc = datetime(2026, 8, 6, 9, 0, tzinfo=timezone.utc)
print(f"Meeting at: {meeting_utc.astimezone(cairo).strftime('%H:%M %Z')} Cairo, "
      f"{meeting_utc.astimezone(tokyo).strftime('%H:%M %Z')} Tokyo")

# Output:
# now(timezone.utc): 2026-08-06 12:34:56.789012+00:00  (aware: True)
# Meeting at: 12:00 EEST Cairo, 18:00 JST Tokyo

# ============================================================
# 3. DST Transitions — Gaps and Ambiguities
# ============================================================
# In a spring-forward zone, one wall-clock hour never exists (gap); in
# fall-back, one hour happens twice (ambiguous). zoneinfo resolves both.

# Example 4: DST gap — 02:30 on the jump day does not exist in America/New_York
ny = ZoneInfo("America/New_York")
gap_naive = datetime(2026, 3, 8, 2, 30)  # 2am -> 3am on 2026-03-08
try:
    gap_aware = gap_naive.replace(tzinfo=ny)
    print(f"\nGap resolves to: {gap_aware}  (offset {gap_aware.utcoffset()})")
except Exception as e:  # non-existent time raises in strict backends
    print(f"\nGap raises: {e}")

# Example 5: UTC instant is unambiguous even across a DST boundary
instant = datetime(2026, 11, 1, 6, 30, tzinfo=timezone.utc)  # fall-back day
print(f"One UTC instant -> {instant.astimezone(ny)}")

# Output:
# One UTC instant -> 2026-11-01 02:30:00-05:00

# ============================================================
# 4. ISO 8601 Round-Trip
# ============================================================
# ISO 8601 (with offset) is the wire format: logs, APIs, DBs, ML datasets.
# fromisoformat parses it back losslessly.

# Example 6: serialize / deserialize
iso = now_utc.isoformat()
parsed = datetime.fromisoformat(iso)
print(f"\nISO: {iso}")
print(f"Round-trip identical: {parsed == now_utc}")

# Example 7: Unix timestamps — the numeric interchange format
ts = now_utc.timestamp()  # seconds since epoch, UTC
back = datetime.fromtimestamp(ts, tz=timezone.utc)
print(f"Epoch seconds: {ts:.0f} -> back to UTC: {back.isoformat()}")

# Output:
# ISO: 2026-08-06T12:34:56.789012+00:00
# Round-trip identical: True
# Epoch seconds: 1785976496 -> back to UTC: 2026-08-06T12:34:56.789012+00:00

# ============================================================
# 5. timedelta Arithmetic & date-only
# ============================================================
# Prefer date over datetime when the time part is meaningless (e.g. dataset
# snapshot date). timedelta does the arithmetic; no manual day math.

# Example 8: date-only and arithmetic
snapshot = date(2026, 8, 1)
train_cutoff = snapshot - timedelta(days=30)
print(f"\nSnapshot {snapshot}, training window starts {train_cutoff}")

window_end = snapshot + timedelta(days=7)
print(f"Retention window ends {window_end} (weekday {window_end.strftime('%A')})")

# Output:
# Snapshot 2026-08-01, training window starts 2026-07-02
# Retention window ends 2026-08-08 (weekday Saturday)

# ============================================================
# 6. time.monotonic — Measure Duration, Not Wall Clock
# ============================================================
# time.time() can jump backward (NTP sync, manual clock edits) and is affected
# by DST. monotonic() only moves forward — use it for latency and timeouts.

# Example 9: measuring a call
start = time.monotonic()
time.sleep(0.01)
elapsed_ms = (time.monotonic() - start) * 1000
print(f"\nElapsed (monotonic): {elapsed_ms:.1f} ms")

# ============================================================
# 7. Production Pattern — Age Check in UTC
# ============================================================
def is_fresh(timestamp_utc: datetime, ttl_seconds: int, *, now: datetime | None = None) -> bool:
    """True if timestamp_utc is within ttl_seconds of now (both aware, UTC)."""
    now = now or datetime.now(timezone.utc)
    age = now - timestamp_utc
    return age.total_seconds() <= ttl_seconds


cached_at = datetime.now(timezone.utc) - timedelta(seconds=30)
print(f"\nCache 30s old, TTL 60s: fresh={is_fresh(cached_at, 60)}")
print(f"Cache 30s old, TTL 10s: fresh={is_fresh(cached_at, 10)}")

# Output:
# Cache 30s old, TTL 60s: fresh=True
# Cache 30s old, TTL 10s: fresh=False

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: storing local wall time in a DB
#   bad = datetime.now()          # naive local; ambiguous, DST-broken
# CORRECT:
#   good = datetime.now(timezone.utc)  # aware, unambiguous

# MISTAKE: using datetime.utcnow() (deprecated, returns NAIVE UTC)
#   bad = datetime.utcnow()
# CORRECT:
#   good = datetime.now(timezone.utc)

# MISTAKE: measuring latency with time.time()
#   bad = time.time(); work(); time.time() - bad   # can go negative
# CORRECT:
#   good = time.monotonic(); work(); time.monotonic() - good

# MISTAKE: comparing a timestamp to now without converting zones
#   bad = last_seen.astimezone(tz) > datetime.now()   # naive vs aware
# CORRECT:
#   good = last_seen.astimezone(timezone.utc) > datetime.now(timezone.utc)

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # Naive/aware distinction enforced by TypeError
    n = datetime(2026, 1, 1)
    a = datetime(2026, 1, 1, tzinfo=timezone.utc)
    try:
        n - a
        assert False, "naive - aware must raise TypeError"
    except TypeError:
        pass

    # Zone conversion is reversible
    if ZoneInfo is not None:
        la = ZoneInfo("America/Los_Angeles")
        utc = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
        assert utc.astimezone(la).astimezone(timezone.utc) == utc, \
            "zone round-trip must be lossless"

    # ISO round-trip
    orig = datetime(2026, 8, 6, 9, 30, 15, 123456, tzinfo=timezone.utc)
    assert datetime.fromisoformat(orig.isoformat()) == orig, \
        "ISO 8601 round-trip must be lossless"

    # Unix timestamp round-trip
    ts = orig.timestamp()
    assert datetime.fromtimestamp(ts, tz=timezone.utc) == orig, \
        "timestamp round-trip must be lossless"

    # timedelta arithmetic
    assert date(2026, 8, 1) - timedelta(days=30) == date(2026, 7, 2), \
        "timedelta arithmetic on dates"

    # monotonic never decreases across two reads
    m1 = time.monotonic()
    m2 = time.monotonic()
    assert m2 >= m1, "monotonic must never move backward"

    # TTL helper with injected now (deterministic)
    now = datetime(2026, 8, 6, 12, 0, 0, tzinfo=timezone.utc)
    old = now - timedelta(seconds=90)
    assert not is_fresh(old, 60, now=now), "90s-old must exceed 60s TTL"
    assert is_fresh(now - timedelta(seconds=30), 60, now=now), \
        "30s-old must be within 60s TTL"
    assert is_fresh(now, 0, now=now), "exactly at TTL boundary is fresh"

    print("[OK] 50-datetime-and-timezones: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Aware in storage, convert only at the display boundary")
        print("2. Use now(timezone.utc), never utcnow() or naive now()")
        print("3. IANA zones via zoneinfo; ISO 8601 for the wire")
        print("4. Measure duration with time.monotonic()")
        print("5. date for calendar logic; datetime for instants")
        _verify()
