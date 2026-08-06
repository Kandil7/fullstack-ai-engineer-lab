# 01-core-python — 50: Datetime & Timezones — Time Is Not a String

## Topic Overview

Python's `datetime` module splits the world into two kinds of objects:
**naive** (no timezone attached — ambiguous wall-clock time) and **aware**
(carries `tzinfo` — a UTC offset or an IANA zone). Mixing them raises
`TypeError` *on purpose*: the error is protecting you from a bug that would
otherwise silently corrupt data. `zoneinfo.ZoneInfo` (3.9+) gives correct
IANA zones — with real DST rules — on the standard library, and the storage
rule is simple: **store UTC, convert only at the display boundary**.

For AI engineers this is not pedantry. A naive-vs-aware bug leaks the
future into a training window: a model trained on "local" timestamps
silently sees tomorrow's data. TTLs on cached embeddings, scheduled
retraining, per-request latency logs, and time-based train/test splits all
break when time handling is wrong. And you measure duration with
`time.monotonic`, never wall clock.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish naive from aware datetimes and explain why mixing them raises
2. Get the current UTC time correctly (`now(timezone.utc)`, never `utcnow()`)
3. Convert between zones with `zoneinfo.ZoneInfo` and `astimezone`
4. Explain DST gaps and ambiguities and how `fold` resolves them
5. Serialize and parse ISO 8601 round-trips losslessly
6. Convert to and from Unix timestamps
7. Do calendar arithmetic with `timedelta` and choose `date` vs `datetime`
8. Measure durations with `time.monotonic` instead of `time.time`
9. Write a TTL/age check that is safe across zones

## Prerequisites

| Need | Where |
|------|-------|
| `datetime`, `date`, `timedelta` basics | `26-dates.py` |
| `strftime`/`strptime` formatting | `26-dates.py` |
| Context managers and exceptions | `30-try-except.py`, `02-advanced-python/03-context-managers-lecture.md` |
| String formatting | `31-string-formatting.py` |

## 1. Naive vs Aware — The Core Distinction

A **naive** datetime has `tzinfo=None`: it is a wall-clock reading with no
meaning about the actual instant. An **aware** datetime carries a timezone
(UTC offset or IANA zone) and *is* an instant. Arithmetic between the two
kinds raises `TypeError` — deliberately, because the result would be
meaningless.

```python
from datetime import datetime, timezone

naive = datetime(2026, 8, 6, 12, 0, 0)
aware_utc = datetime(2026, 8, 6, 12, 0, 0, tzinfo=timezone.utc)
print(f"naive:      {naive}  tzinfo={naive.tzinfo}")
print(f"aware UTC:  {aware_utc}  tzinfo={aware_utc.tzinfo}")

try:
    naive - aware_utc
except TypeError as e:
    print(f"mixed arithmetic -> TypeError: {e}")
```

```
# Output:
# naive:      2026-08-06 12:00:00  tzinfo=None
# aware UTC:  2026-08-06 12:00:00+00:00  tzinfo=datetime.timezone.utc
# mixed arithmetic -> TypeError: can't subtract offset-naive and offset-aware datetimes
```

The rule of thumb: **naive is for the display layer, aware is for storage,
computation, and comparison.** If a datetime crosses a process boundary
(DB, log, API, file), it must be aware — or its instant is undefined.

## 2. The Storage Rule — UTC Everywhere

Store UTC. Convert to local zones only at the display boundary. This makes
comparisons, sorting, and arithmetic unambiguous, and it makes your data
independent of which server (or which timezone) happened to write it.

```python
from datetime import datetime, timezone

now_utc = datetime.now(timezone.utc)
print(f"now(timezone.utc): {now_utc}  (aware: {now_utc.tzinfo is not None})")
```

```
# Output:
# now(timezone.utc): 2026-08-06 12:34:56.789012+00:00  (aware: True)
```

Two deprecated traps: `datetime.utcnow()` returns a **naive** UTC time (it
lost the tzinfo), and `datetime.now()` returns naive local time. Both are
storage bugs waiting to happen. `datetime.now(timezone.utc)` is aware,
unambiguous, and the only form you should write.

## 3. IANA Zones with `zoneinfo`

`zoneinfo.ZoneInfo("Africa/Cairo")` loads the real IANA timezone database —
including DST rules — so conversions are correct for *any* date, past or
future. `astimezone` converts an aware datetime to another zone.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

cairo = ZoneInfo("Africa/Cairo")
tokyo = ZoneInfo("Asia/Tokyo")
meeting_utc = datetime(2026, 8, 6, 9, 0, tzinfo=timezone.utc)
print(f"Meeting at: {meeting_utc.astimezone(cairo).strftime('%H:%M %Z')} Cairo, "
      f"{meeting_utc.astimezone(tokyo).strftime('%H:%M %Z')} Tokyo")
```

```
# Output:
# Meeting at: 12:00 EEST Cairo, 18:00 JST Tokyo
```

ZoneInfo objects are cheap to keep: construction reads tzdata the first
time, then the object is cached. In a hot loop, **construct the ZoneInfo
once** and reuse it — never per call. (On some platforms the `tzdata` pip
package is needed; `import zoneinfo` works out of the box on most systems.)

## 4. DST — Gaps and Ambiguities

Twice a year, most zones do something weird. Spring forward: one wall-clock
hour **never exists** (a gap). Fall back: one hour **happens twice** (an
ambiguous time). Both are handled by `zoneinfo` + the `fold` attribute.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

ny = ZoneInfo("America/New_York")
gap_naive = datetime(2026, 3, 8, 2, 30)  # 2am -> 3am on 2026-03-08
gap_aware = gap_naive.replace(tzinfo=ny)
print(f"Gap resolves to: {gap_aware}  (offset {gap_aware.utcoffset()})")

instant = datetime(2026, 11, 1, 6, 30, tzinfo=timezone.utc)  # fall-back day
print(f"One UTC instant -> {instant.astimezone(ny)}")
```

```
# Output:
# One UTC instant -> 2026-11-01 02:30:00-05:00
```

For a gap (non-existent time), `replace(tzinfo=...)` keeps the pre-
transition offset, so the instant converts back to the shifted-forward
local time (02:30 becomes 03:30) — the conventional scheduling behavior.
For an ambiguous time, `fold=0` picks the first occurrence (daylight),
`fold=1` the second (standard). The takeaway: **always store UTC**, where
every instant is unique and no gap or ambiguity exists.

## 5. ISO 8601 — The Wire Format

ISO 8601 with an offset (`2026-08-06T12:34:56+00:00`) is the interchange
format for logs, APIs, databases, and ML dataset metadata. `isoformat()`
serializes; `fromisoformat` parses it back losslessly.

```python
from datetime import datetime, timezone

now_utc = datetime(2026, 8, 6, 12, 34, 56, 789012, tzinfo=timezone.utc)
iso = now_utc.isoformat()
parsed = datetime.fromisoformat(iso)
print(f"ISO: {iso}")
print(f"Round-trip identical: {parsed == now_utc}")
```

```
# Output:
# ISO: 2026-08-06T12:34:56.789012+00:00
# Round-trip identical: True
```

The round-trip is lossless: the offset is preserved, so `parsed` is still
aware. A naive ISO string (no offset) round-trips to a **naive** datetime —
which is why you must always include the offset when writing timestamps.

## 6. Unix Timestamps — The Numeric Interchange

A Unix timestamp is seconds since 1970-01-01 00:00:00 UTC — a single
unambiguous number, the standard numeric interchange for metrics and
databases. `.timestamp()` converts an aware datetime to epoch seconds;
`fromtimestamp(ts, tz=timezone.utc)` converts back.

```python
from datetime import datetime, timezone

now_utc = datetime(2026, 8, 6, 12, 34, 56, 789012, tzinfo=timezone.utc)
ts = now_utc.timestamp()
back = datetime.fromtimestamp(ts, tz=timezone.utc)
print(f"Epoch seconds: {ts:.0f} -> back to UTC: {back.isoformat()}")
```

```
# Output:
# Epoch seconds: 1785976496 -> back to UTC: 2026-08-06T12:34:56.789012+00:00
```

Always pass `tz=timezone.utc` to `fromtimestamp`; without it, you get a
naive local time — the same trap as `utcnow()`.

## 7. `timedelta` Arithmetic and `date`

`timedelta` does the calendar math: add/subtract days, weeks, hours — no
manual day counting. And when the time part is meaningless (a dataset
snapshot date, a retention cutoff), use `date`, not `datetime`: it cannot
carry a timezone bug because it cannot carry a time.

```python
from datetime import date, timedelta

snapshot = date(2026, 8, 1)
train_cutoff = snapshot - timedelta(days=30)
print(f"Snapshot {snapshot}, training window starts {train_cutoff}")

window_end = snapshot + timedelta(days=7)
print(f"Retention window ends {window_end} (weekday {window_end.strftime('%A')})")
```

```
# Output:
# Snapshot 2026-08-01, training window starts 2026-07-02
# Retention window ends 2026-08-08 (weekday Saturday)
```

One rule to remember: **`timedelta` arithmetic on an aware datetime adds
exact elapsed time**, so adding 24 hours across a DST transition lands at a
different local time. If you mean "the same local time tomorrow", build the
naive local datetime and attach the zone — never add 24h blindly.

## 8. `time.monotonic` — The Measurement Clock

`time.time()` reads the wall clock: NTP sync, manual edits, and DST
transitions can make it jump **backward**, so an elapsed-time measurement
can go negative. `time.monotonic()` only moves forward and is unaffected by
clock changes — use it for latency, timeouts, and profiling.

```python
import time

start = time.monotonic()
time.sleep(0.01)
elapsed_ms = (time.monotonic() - start) * 1000
print(f"Elapsed (monotonic): {elapsed_ms:.1f} ms")
```

```
# Output:
# Elapsed (monotonic): 10.1 ms
```

Rule: **wall clock for instants (when), monotonic for durations (how
long).** `time.perf_counter` is the same idea with higher resolution; pick
one and use it consistently.

## 9. Production Pattern — TTL Check in UTC

The classic caching problem: is this cached embedding still fresh? Do the
arithmetic in UTC with an injectable `now` so the logic is testable.

```python
from datetime import datetime, timedelta, timezone


def is_fresh(
    timestamp_utc: datetime, ttl_seconds: int, *, now: datetime | None = None
) -> bool:
    """True if timestamp_utc is within ttl_seconds of now (both aware UTC)."""
    now = now or datetime.now(timezone.utc)
    age = now - timestamp_utc
    return age.total_seconds() <= ttl_seconds


cached_at = datetime.now(timezone.utc) - timedelta(seconds=30)
print(f"Cache 30s old, TTL 60s: fresh={is_fresh(cached_at, 60)}")
print(f"Cache 30s old, TTL 10s: fresh={is_fresh(cached_at, 10)}")
```

```
# Output:
# Cache 30s old, TTL 60s: fresh=True
# Cache 30s old, TTL 10s: fresh=False
```

Two production notes: the injected `now` makes the function deterministic
in tests (no wall-clock asserts), and comparing two aware UTC datetimes is
always safe — the timezone math was done at construction time.

## Common Mistakes to Avoid

### Mistake 1: Storing local wall time in a DB
```python
# WRONG - naive local time is ambiguous and DST-broken
created_at = datetime.now()

# CORRECT - aware UTC, unambiguous everywhere
created_at = datetime.now(timezone.utc)
```

### Mistake 2: Using deprecated `datetime.utcnow()`
```python
# WRONG - returns a NAIVE UTC time; the offset is silently dropped
now = datetime.utcnow()

# CORRECT - aware UTC
now = datetime.now(timezone.utc)
```

### Mistake 3: Measuring duration with `time.time()`
```python
# WRONG - wall clock can jump backward (NTP), even negative elapsed
elapsed = time.time() - start

# CORRECT - monotonic only moves forward
elapsed = time.monotonic() - start
```

### Mistake 4: Comparing a naive timestamp to an aware one
```python
# WRONG - TypeError: can't compare offset-naive and offset-aware
if last_seen > datetime.now():

# CORRECT - both sides aware, same zone
if last_seen.astimezone(timezone.utc) > datetime.now(timezone.utc):
```

### Mistake 5: Adding 24h to an aware datetime for "same local time tomorrow"
```python
# WRONG - across a DST transition, local time drifts by one hour
tomorrow = aware_now + timedelta(hours=24)

# CORRECT - rebuild the naive local time and attach the zone
tomorrow_local = (naive_local + timedelta(days=1)).replace(tzinfo=zone)
```

## Best Practices

1. Store UTC (aware); convert to local zones only at the display boundary.
2. Use `datetime.now(timezone.utc)`; never `utcnow()` or naive `now()`.
3. Construct `ZoneInfo` once and reuse it in loops.
4. Always include the UTC offset in serialized timestamps.
5. Use `fromtimestamp(ts, tz=timezone.utc)` — never without the tz.
6. Use `date` for calendar logic; `datetime` for instants.
7. Measure durations with `time.monotonic`; read instants from the wall clock.
8. Inject `now` into functions that check freshness, so tests are
   deterministic.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `ZoneInfo(name)` first load | O(tzdata read) | O(1) (cached) | Reuse the cached object; never rebuild per call |
| `astimezone(zone)` | O(1) | O(1) | — |
| `now(timezone.utc)` | O(1) | O(1) | — |
| `isoformat()` / `fromisoformat` | O(len) | O(len) | Store epoch seconds (`int`) for compactness |
| `.timestamp()` / `fromtimestamp` | O(1) | O(1) | — |
| `timedelta` arithmetic | O(1) | O(1) | — |
| `time.monotonic()` | O(1) | O(1) | — |
| naive vs aware mixing | raises O(1) | — | Convert explicitly before comparing |

## AI Engineering Relevance

**Where this shows up:** every logged inference request, every cache TTL,
every time-based dataset split, every scheduled retraining job.

| Concept here | Used for |
|---|---|
| UTC storage rule | Timestamping inference requests from regions worldwide |
| `zoneinfo` + `astimezone` | Per-region latency dashboards and daily eval buckets |
| DST-aware scheduling | Cron-like retraining jobs that must not drift |
| ISO 8601 round-trip | Dataset metadata and log schemas |
| `time.monotonic` | Per-call LLM latency measurement |
| TTL pattern | Cache expiry for embeddings and reranker outputs |
| `date` bucketing | Train/validation splits by local calendar day |

**Scale note:** a timezone bug in a train/test split leaks the future into
training — a model that looks great on validation is secretly cheating. At
10M logged events, one wrong-offset row mislabels an entire day bucket;
at request rates of 200/s, an incorrect TTL either serves stale embeddings
or thrashes the cache. Time correctness is a data-quality issue before it
is a code issue.

## Practice Exercises

### Exercise 1: Local to UTC (Difficulty: Easy)
Write `to_utc(naive_local: datetime, zone: str) -> datetime` that attaches
`ZoneInfo(zone)` and converts to aware UTC. Verify Cairo summer vs winter
offsets differ.

### Exercise 2: Daily Buckets (Difficulty: Easy)
Write `day_bucket(ts_utc: datetime, zone: str) -> date` returning the local
calendar date in `zone`. Verify a 23:30 UTC timestamp lands on the *next*
day in Tokyo.

### Exercise 3: Freshness Check (Difficulty: Medium)
Write `is_fresh(ts_utc: datetime, ttl: int, *, now: datetime | None = None)`
that returns True when `now - ts_utc <= ttl` seconds. Test with an injected
`now`; assert a 90s-old timestamp fails a 60s TTL.

### Exercise 4: DST-Safe Daily Schedule (Difficulty: Hard)
Write `next_occurrence(utc_start: datetime, zone: str, hour: int, minute: int)`
returning the next occurrence of local `hour:minute` after `utc_start`.
Verify it stays at the same local time across a DST transition (construct
the naive local time, attach the zone).

### Exercise 5: Streaming Buckets (Difficulty: Hard)
Write `bucket_stream(ts_stream: Iterable[datetime], zone: str) -> Iterator[date]`
that converts an unbounded stream of aware UTC timestamps to local dates
lazily, constructing the `ZoneInfo` exactly once.

## Summary

| Concept | Description |
|---|---|
| Naive vs aware | `tzinfo=None` vs attached; mixing raises `TypeError` |
| UTC storage rule | Store UTC; convert only at display boundaries |
| `zoneinfo` | Real IANA zones with correct DST rules |
| DST gaps/ambiguity | `fold` picks the occurrence; UTC has neither problem |
| ISO 8601 | The wire format; round-trips losslessly with offset |
| Unix timestamps | Seconds since epoch; `fromtimestamp(ts, tz=utc)` |
| `timedelta` / `date` | Calendar arithmetic; `date` when time is meaningless |
| `time.monotonic` | Measure durations, never wall clock |
| TTL pattern | Compare aware UTC with injectable `now` |

Time is the one domain where "it works on my machine" is a genuine category
of bug: the same code produces different answers in different timezones,
and the naive version produces no error at all — just quietly wrong data.
Store UTC, stay aware, measure with monotonic, and your logs, splits, and
TTLs will agree with each other everywhere.

## Quick Reference

| Task | Idiom |
|---|---|
| Current UTC | `datetime.now(timezone.utc)` |
| Zone object | `z = ZoneInfo("Africa/Cairo")` (build once) |
| Convert zone | `dt.astimezone(z)` |
| Serialize | `dt.isoformat()` |
| Parse | `datetime.fromisoformat(s)` |
| To epoch | `dt.timestamp()` |
| From epoch | `datetime.fromtimestamp(ts, tz=timezone.utc)` |
| Attach zone to naive | `naive.replace(tzinfo=z)` |
| Duration | `time.monotonic()` before/after |
| Calendar math | `date + timedelta(days=n)` |
| Local date in zone | `dt.astimezone(z).date()` |

## Next Steps

Next: **[51-serialization-and-persistence](51-serialization-and-persistence-lecture.md)** — JSON, CSV, pickle, JSONL, and sqlite3 for data that survives restarts.
Continues in: **[02-advanced-python — 04 async/await](../../02-advanced-python/lectures/04-async-await-lecture.md)** (monotonic timeouts and timestamps in async pipelines).
Official docs: https://docs.python.org/3/library/datetime.html and https://docs.python.org/3/library/zoneinfo.html
