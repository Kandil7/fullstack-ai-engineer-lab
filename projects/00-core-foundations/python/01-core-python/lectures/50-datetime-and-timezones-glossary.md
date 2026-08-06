# 50: Datetime & Timezones — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `astimezone` | Method | Converts an aware datetime to another zone |
| aware datetime | Concept | Carries `tzinfo`; represents a real instant |
| `date` | Class | Calendar date without time; cannot have a tz bug |
| `fold` | Attribute | Picks first (0) or second (1) occurrence of an ambiguous local time |
| `fromisoformat` | Function | Parses ISO 8601 strings back to datetime |
| `fromtimestamp` | Function | Converts epoch seconds to a datetime (always pass `tz=`) |
| gap | Concept | A local hour that never exists during spring-forward |
| ambiguous time | Concept | A local hour that happens twice during fall-back |
| IANA zone | Concept | Named timezone with real DST rules (e.g. `Africa/Cairo`) |
| `isoformat` | Method | Serializes a datetime as ISO 8601 |
| `monotonic` | Function | `time.monotonic` — only moves forward; measure durations |
| naive datetime | Concept | `tzinfo=None`; ambiguous wall-clock time |
| `timedelta` | Class | Duration for calendar/elapsed arithmetic |
| `timestamp()` | Method | Epoch seconds (UTC) for an aware datetime |
| `timezone.utc` | Constant | The UTC timezone object for aware datetimes |
| `utcnow()` | Anti-pattern | Deprecated; returns NAIVE UTC — never use |
| `ZoneInfo` | Class | IANA timezone database access (3.9+) |
| `now(timezone.utc)` | Pattern | The correct way to get current UTC time |

## Detailed Definitions

### ambiguous time
**Definition**: A local wall-clock time that occurs twice during a
fall-back transition — the same hour happens first in daylight time, then
again in standard time. `fold=0` picks the first, `fold=1` the second.

**Example**:
```python
from datetime import datetime
from zoneinfo import ZoneInfo
ny = ZoneInfo("America/New_York")
print(datetime(2026, 11, 1, 1, 30, fold=0).replace(tzinfo=ny).utcoffset())  # -4:00 (first)
print(datetime(2026, 11, 1, 1, 30, fold=1).replace(tzinfo=ny).utcoffset())  # -5:00 (second)
```

**Complexity**: O(1).

**Related**: gap, `fold`, `ZoneInfo`

### `astimezone`
**Definition**: `dt.astimezone(zone)` returns the same instant expressed in
another zone — the only correct way to convert between timezones. The
result is always aware.

**Example**:
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
utc = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
print(utc.astimezone(ZoneInfo("Asia/Tokyo")))  # 2026-08-06 21:00:00+09:00
```

**Complexity**: O(1).

**Related**: `ZoneInfo`, `timezone.utc`

### aware datetime
**Definition**: A datetime carrying `tzinfo` — a UTC offset or IANA zone.
It denotes a single real instant, so comparison and arithmetic with other
aware datetimes are well-defined.

**Example**:
```python
from datetime import datetime, timezone
d = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
print(d.tzinfo is not None)  # True
```

**Complexity**: O(1).

**Related**: naive datetime, `timezone.utc`, `ZoneInfo`

### `date`
**Definition**: A calendar date with no time component. Because it cannot
carry a time, it cannot carry a timezone bug — the right type for snapshot
dates, retention cutoffs, and daily buckets.

**Example**:
```python
from datetime import date, timedelta
print(date(2026, 8, 1) - timedelta(days=30))  # 2026-07-02
```

**Complexity**: O(1).

**Related**: `datetime`, `timedelta`

### `fold`
**Definition**: The integer attribute (0 or 1) that disambiguates a local
time that occurs twice: 0 = first occurrence (daylight), 1 = second
(standard). For non-existent gap times, `fold` is conventionally 0.

**Example**:
```python
from datetime import datetime
from zoneinfo import ZoneInfo
ny = ZoneInfo("America/New_York")
a = datetime(2026, 11, 1, 1, 30, fold=0).replace(tzinfo=ny)
b = datetime(2026, 11, 1, 1, 30, fold=1).replace(tzinfo=ny)
print(a == b)  # False - two different instants
```

**Complexity**: O(1).

**Related**: ambiguous time, gap

### `fromisoformat`
**Definition**: The parser counterpart to `isoformat`: turns an ISO 8601
string back into a datetime. With an offset, the result is aware; without,
it is naive — always include the offset.

**Example**:
```python
from datetime import datetime
d = datetime.fromisoformat("2026-08-06T12:00:00+00:00")
print(d.tzinfo is not None)  # True
```

**Complexity**: O(len) for parsing.

**Related**: `isoformat`, naive datetime

### `fromtimestamp`
**Definition**: `datetime.fromtimestamp(ts, tz=...)` converts epoch seconds
to a datetime. The `tz` argument is mandatory in practice — without it you
get naive local time.

**Example**:
```python
from datetime import datetime, timezone
print(datetime.fromtimestamp(0, tz=timezone.utc))  # 1970-01-01 00:00:00+00:00
```

**Complexity**: O(1).

**Related**: `timestamp()`, `timezone.utc`

### gap
**Definition**: A local wall-clock hour that does not exist during the
spring-forward transition (e.g. 02:00-03:00 in New York on the transition
day). `replace(tzinfo=...)` resolves it with the pre-transition offset, so
converting back yields the shifted-forward time.

**Example**:
```python
from datetime import datetime
from zoneinfo import ZoneInfo
ny = ZoneInfo("America/New_York")
d = datetime(2026, 3, 8, 2, 30).replace(tzinfo=ny)
print(d.utcoffset())  # -1 day, 19:00:00 == -05:00 (pre-transition)
```

**Complexity**: O(1).

**Related**: ambiguous time, `fold`

### IANA zone
**Definition**: A named timezone from the IANA tz database — e.g.
`Africa/Cairo`, `America/New_York` — carrying the complete historical and
future DST rules. `zoneinfo.ZoneInfo(name)` loads it.

**Example**:
```python
from zoneinfo import ZoneInfo
z = ZoneInfo("Africa/Cairo")
print(z)  # Africa/Cairo
```

**Complexity**: first construction reads tzdata; the object is then cached.

**Related**: `ZoneInfo`, `astimezone`

### `isoformat`
**Definition**: `dt.isoformat()` serializes a datetime in ISO 8601 —
`2026-08-06T12:34:56.789012+00:00` for aware UTC. The standard wire format
for logs, APIs, and dataset metadata.

**Example**:
```python
from datetime import datetime, timezone
print(datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc).isoformat())
# 2026-08-06T12:00:00+00:00
```

**Complexity**: O(len).

**Related**: `fromisoformat`, `timestamp()`

### `monotonic`
**Definition**: `time.monotonic()` returns seconds from an arbitrary epoch
that only moves forward — immune to NTP jumps, manual clock edits, and DST.
The correct clock for measuring durations.

**Example**:
```python
import time
start = time.monotonic()
time.sleep(0.01)
print(f"{(time.monotonic() - start) * 1000:.1f} ms")
```

**Complexity**: O(1).

**Related**: `time.time` (wall clock), `timedelta`

### naive datetime
**Definition**: A datetime with `tzinfo=None` — a wall-clock reading with
no instant meaning. Mixing it with an aware datetime raises `TypeError` by
design.

**Example**:
```python
from datetime import datetime, timezone
n = datetime(2026, 8, 6, 12, 0)          # naive
a = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)  # aware
try:
    n - a
except TypeError:
    print("mixing raises TypeError")
```

**Complexity**: O(1).

**Related**: aware datetime, `timezone.utc`

### `now(timezone.utc)`
**Definition**: The correct idiom for "current time": `datetime.now(timezone.utc)`
returns an aware UTC datetime. It replaces the deprecated, naive
`datetime.utcnow()`.

**Example**:
```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
print(now.tzinfo is not None)  # True
```

**Complexity**: O(1).

**Related**: `utcnow()`, aware datetime

### `timedelta`
**Definition**: A duration — days, seconds, microseconds — used for
calendar and elapsed arithmetic. Adding it to an aware datetime adds exact
elapsed time; local-time-of-day shifts across DST are *not* automatic.

**Example**:
```python
from datetime import date, timedelta
print(date(2026, 3, 1) + timedelta(days=30))  # 2026-03-31
```

**Complexity**: O(1).

**Related**: `date`, `datetime`

### `timestamp()`
**Definition**: `dt.timestamp()` converts an aware datetime to Unix epoch
seconds (UTC-based). The numeric interchange format for metrics, databases,
and compact storage.

**Example**:
```python
from datetime import datetime, timezone
d = datetime(1970, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
print(d.timestamp())  # 1.0
```

**Complexity**: O(1).

**Related**: `fromtimestamp`, `isoformat`

### `timezone.utc`
**Definition**: The fixed UTC timezone object. Use it to build aware UTC
datetimes and as the `tz` argument everywhere an aware UTC is required.

**Example**:
```python
from datetime import datetime, timezone
d = datetime(2026, 8, 6, tzinfo=timezone.utc)
print(d.utcoffset())  # 0:00:00
```

**Complexity**: O(1).

**Related**: aware datetime, `now(timezone.utc)`

### `utcnow()`
**Definition**: `datetime.utcnow()` — deprecated in 3.12, removed in 3.13.
It returns a **naive** UTC time, silently dropping the offset. Any
arithmetic or comparison then treats it as local wall time — a latent
data-corruption bug.

**Example**:
```python
# WRONG (removed in 3.13):
# now = datetime.utcnow()  -> naive!

# CORRECT:
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
```

**Complexity**: O(1).

**Related**: `now(timezone.utc)`, naive datetime

### `ZoneInfo`
**Definition**: `zoneinfo.ZoneInfo(name)` — the class that loads an IANA
timezone (3.9+). Zone objects are cached after first load; construct once
and reuse.

**Example**:
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
tokyo = ZoneInfo("Asia/Tokyo")
utc = datetime(2026, 8, 6, 3, 0, tzinfo=timezone.utc)
print(utc.astimezone(tokyo))  # 2026-08-06 12:00:00+09:00
```

**Complexity**: first construction O(tzdata read); conversions O(1).

**Related**: IANA zone, `astimezone`

## Key Concepts Summary

### The Two Kinds of Datetime
- **Naive** (`tzinfo=None`): wall-clock reading, no instant, no storage.
- **Aware** (`tzinfo` set): a real instant; safe to store, compare, compute.
- Mixing them raises `TypeError` — that error is a feature.

### Storage and Wire Rules
- Store UTC, always aware: `datetime.now(timezone.utc)`.
- Serialize with offset: `isoformat()`; parse with `fromisoformat`.
- For numbers, use `.timestamp()` / `fromtimestamp(ts, tz=timezone.utc)`.
- Never `utcnow()` (naive) and never `fromtimestamp(ts)` without `tz`.

### DST Survival Guide
- Gaps: the hour never exists — `replace(tzinfo=...)` shifts forward.
- Ambiguities: `fold=0` first occurrence, `fold=1` second.
- The clean escape: work in UTC, where neither problem exists.

### Measurement Rule
- Instants: wall clock (`datetime.now(timezone.utc)`).
- Durations: `time.monotonic()` — never `time.time()` for elapsed.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. naive datetime — ___
2. `ZoneInfo` — ___
3. `fold` — ___
4. gap — ___
5. `monotonic` — ___
6. `timestamp()` — ___
7. `isoformat` — ___
8. ambiguous time — ___
9. `utcnow()` — ___
10. `astimezone` — ___

A. `tzinfo=None`; wall-clock with no instant meaning
B. Loads IANA timezones with real DST rules
C. Picks first or second occurrence of an ambiguous hour
D. A local hour that never exists (spring forward)
E. Clock that only moves forward — measure durations with it
F. Epoch seconds for an aware datetime
G. ISO 8601 serialization
H. A local hour that happens twice (fall back)
I. Deprecated; returns naive UTC
J. Converts an aware datetime to another zone

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
