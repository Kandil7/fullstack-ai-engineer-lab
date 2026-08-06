# Challenge 50: Datetime & Timezones

Time is not a string — and not a naive datetime either. Convert correctly,
bucket by local day, and schedule across DST without drifting.

## 🥉 Bronze — Local to UTC (~15 min)

**Task:** Implement `to_utc(naive_local, zone)`, which attaches the IANA
zone to a **naive** local datetime and returns the equivalent **aware UTC**
datetime. The result must have `tzinfo is not None`.

**Signature:**
```python
def to_utc(naive_local: datetime, zone: str) -> datetime:
```

| Input | Expected |
|---|---|
| `datetime(2026, 8, 6, 9, 0), "Africa/Cairo"` | `2026-08-06 06:00:00+00:00` (Cairo summer, UTC+3) |
| `datetime(2026, 1, 6, 9, 0), "Africa/Cairo"` | `2026-01-06 07:00:00+00:00` (Cairo winter, UTC+2) |
| `datetime(2026, 8, 6, 12, 0), "Asia/Tokyo"` | `2026-08-06 03:00:00+00:00` (JST, UTC+9) |
| `datetime(2026, 8, 6, 12, 0), "UTC"` | `2026-08-06 12:00:00+00:00` |

**Constraints:** Any correct approach passes.

---

## 🥈 Silver — Daily Buckets (~35 min)

**Task:** Implement `day_buckets(timestamps, tz)`, a **generator** that
yields the local calendar `date` of each aware-UTC timestamp in `tz` — the
bucketing rule for per-region daily metrics and eval splits. The
`ZoneInfo(tz)` object must be constructed **exactly once per call**, not
once per timestamp.

**Signature:**
```python
def day_buckets(
    timestamps: Iterable[datetime],
    tz: str,
) -> Iterator[date]:
```

| Input | Expected |
|---|---|
| `[2026-08-06T12:00Z], "Asia/Tokyo"` | `[date(2026, 8, 6)]` (21:00 JST, same day) |
| `[2026-08-06T23:30Z], "Asia/Tokyo"` | `[date(2026, 8, 7)]` (next day in JST) |
| `[2026-08-06T23:30Z], "America/New_York"` | `[date(2026, 8, 6)]` (19:30 EDT, still Aug 6) |
| `[2026-08-06T00:00Z], "Africa/Cairo"` | `[date(2026, 8, 6)]` (03:00 Cairo, same day) |
| `[]` | `[]` |

**Constraints:** `n <= 10^6` timestamps. The tests count `ZoneInfo`
constructions by reloading the module with a counting `ZoneInfo` — a
per-timestamp construction (n calls) fails the guard; constructing once
passes. Must be lazy: return a generator, never a materialized list.

---

## 🥇 Gold — DST-Safe Daily Schedule (~75 min)

**Task:** Implement `schedule_stream(utc_start, tz, hour, minute)`, an
infinite **generator** of aware-UTC datetimes: one per day, for
`local_date(utc_start) + i` days, at the local wall time `hour:minute`,
resolved with `zoneinfo` (`fold=0`). "DST-safe" means: on normal days the
instant converts back to exactly `hour:minute` local; on a gap day
(non-existent local time) it converts back to the shifted-forward time
(the conventional resolution). Adding 24 hours to the previous instant
**drifts by one hour across every DST transition** — that is the bug to
avoid. Construct the naive local datetime, attach the zone, convert.

**Signature:**
```python
def schedule_stream(
    utc_start: datetime,
    tz: str,
    hour: int,
    minute: int,
) -> Iterator[datetime]:
```

| Input | Expected (first 3 yields, Tokyo) |
|---|---|
| `2026-08-01T00:00Z, "Asia/Tokyo", 9, 0` | `2026-08-01T00:00Z, 2026-08-02T00:00Z, 2026-08-03T00:00Z` |

**Constraints:** designed for a stream of `10^7`+ days, O(1) memory per
yield, lazy single-pass. The tests verify 250 Cairo days crossing **both**
2026 DST transitions (Apr 24 spring, Oct 29 fall) all convert back to
09:30 local with zero net drift (a 24h-adding solution drifts to 10:30
right after the first transition and never recovers), verify the New York
gap day (2026-03-08 02:30) resolves to the shifted-forward 03:30 EDT, and
run a `tracemalloc` ceiling (15 MiB) over `4 * 10^5` yielded occurrences —
a materialized list is ~22 MB and fails the ceiling.

**Follow-up:** what breaks first at 10^9 days? (Answer: nothing in this
function — it is O(1) per yield — but the *consumer* must stream; any
materialization is impossible at that scale.)

---

## Running

```bash
pytest challenges/50-datetime-and-timezones/test_challenge.py -v
```

## Test File Structure

```
challenges/50-datetime-and-timezones/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
