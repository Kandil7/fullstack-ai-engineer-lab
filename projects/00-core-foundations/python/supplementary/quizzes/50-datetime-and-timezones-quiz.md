# Quiz 50: Datetime & Timezones

**Instructions:** Choose the single best answer. Answers and explanations
are at the end.

## Questions

### Q1. What does an *aware* datetime carry that a *naive* one does not?
**Difficulty:** Easy

- (A) A microseconds field
- (B) A `tzinfo` (UTC offset or IANA zone)
- (C) A Unix timestamp
- (D) A `fold` value

### Q2. What is the correct way to get "now" in Python?
**Difficulty:** Easy

- (A) `datetime.utcnow()`
- (B) `datetime.now()`
- (C) `datetime.now(timezone.utc)`
- (D) `time.time(utc=True)`

### Q3. Which of these is the IANA timezone database accessor?
**Difficulty:** Easy

- (A) `pytz.timezone()`
- (B) `zoneinfo.ZoneInfo(name)`
- (C) `datetime.zone()`
- (D) `tzdata.get(name)`

### Q4. What is the output?
**Difficulty:** Easy

```python
from datetime import datetime, timezone
d = datetime(1970, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
print(d.timestamp())
```

- (A) `1.0`
- (B) `0.0`
- (C) `1e9`
- (D) `TypeError` (naive)

### Q5. What is the output?
**Difficulty:** Easy

```python
from datetime import datetime, timezone
n = datetime(2026, 8, 6, 12, 0)                     # naive
a = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)  # aware
print(n - a)
```

- (A) `0:00:00`
- (B) `TypeError`
- (C) `-0:00:00`
- (D) `ValueError`

### Q6. What is the output?
**Difficulty:** Medium

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
tokyo = ZoneInfo("Asia/Tokyo")
d = datetime(2026, 8, 6, 3, 0, tzinfo=timezone.utc)
print(d.astimezone(tokyo))
```

- (A) `2026-08-06 03:00:00+09:00`
- (B) `2026-08-06 12:00:00+09:00`
- (C) `2026-08-05 18:00:00+09:00`
- (D) `2026-08-06 03:00:00+00:00`

### Q7. In New York, the hour 02:00–03:00 on 2026-03-08 (spring forward) — what is true of it?
**Difficulty:** Medium

- (A) It happens twice; use `fold` to pick
- (B) It does not exist — `replace(tzinfo=...)` resolves it with the pre-transition offset
- (C) It occurs once with offset −05:00
- (D) It is always resolved to 03:00 EDT by `utcoffset()`

### Q8. What is the output?
**Difficulty:** Medium

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
ny = ZoneInfo("America/New_York")
a = datetime(2026, 11, 1, 1, 30, fold=0).replace(tzinfo=ny)
b = datetime(2026, 11, 1, 1, 30, fold=1).replace(tzinfo=ny)
print(a == b)
```

- (A) `True`
- (B) `False`
- (C) `TypeError`
- (D) `None`

### Q9. What is the output?
**Difficulty:** Medium

```python
from datetime import datetime, timezone
d = datetime.fromisoformat("2026-08-06T12:00:00+00:00")
print(d.tzinfo is not None, d.hour)
```

- (A) `True 12`
- (B) `True 14`
- (C) `False 12`
- (D) `ValueError` — `fromisoformat` cannot parse offsets

### Q10. Which conversion converts the *same instant* to another zone?
**Difficulty:** Easy

- (A) `dt.replace(tzinfo=other)`
- (B) `dt.astimezone(other)`
- (C) `datetime.combine(dt.date(), dt.time(), tzinfo=other)`
- (D) `dt + other.utcoffset(dt)`

### Q11. A scheduled job must run daily at 09:30 local time in Cairo across DST. Which approach is correct?
**Difficulty:** Hard

- (A) Add `timedelta(hours=24)` to the previous UTC instant
- (B) Add `timedelta(days=1)` to the previous naive local datetime and re-attach the zone
- (C) Store the fixed UTC time 07:30 forever
- (D) Use `time.monotonic()` to compute the next run

### Q12. What is the output?
**Difficulty:** Medium

```python
from datetime import date, timedelta
print(date(2026, 3, 1) + timedelta(days=30))
```

- (A) `2026-03-31`
- (B) `2026-03-30`
- (C) `2026-04-01`
- (D) `TypeError` — cannot add `timedelta` to `date`

### Q13. Which clock should measure a function's duration?
**Difficulty:** Medium

- (A) `datetime.now(timezone.utc)` differences
- (B) `time.time()` differences
- (C) `time.monotonic()` differences
- (D) `date.today()` differences

### Q14. What is the output?
**Difficulty:** Medium

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
d = datetime(2026, 8, 6, 9, 0).replace(tzinfo=ZoneInfo("Africa/Cairo"))
print(d.astimezone(timezone.utc).isoformat())
```

- (A) `2026-08-06T09:00:00+00:00`
- (B) `2026-08-06T06:00:00+00:00`
- (C) `2026-08-06T12:00:00+00:00`
- (D) `2026-08-06T06:00:00+03:00`

### Q15. Why is `datetime.utcnow()` dangerous?
**Difficulty:** Medium

- (A) It is slow because it queries the OS timezone database
- (B) It returns a *naive* UTC time — silently dropping the offset — so arithmetic treats it as local
- (C) It raises `DeprecationWarning` and stops working
- (D) It returns a string instead of a datetime

### Q16. What is the output?
**Difficulty:** Medium

```python
from datetime import datetime, timezone
d = datetime(2026, 3, 8, 2, 30).replace(tzinfo=ZoneInfo("America/New_York"))
print(d.utcoffset())
```

*(The lines use `from zoneinfo import ZoneInfo`; assume it is imported.)*

- (A) `0:00:00`
- (B) `-1 day, 19:00:00` (i.e. −05:00, pre-transition)
- (C) `-4:00:00`
- (D) `ValueError` — that wall time does not exist

### Q17. When storing timestamps in a database, the recommended rule is:
**Difficulty:** Easy

- (A) Store each user's local wall time
- (B) Store naive UTC
- (C) Store aware UTC (or epoch seconds), convert to local only at display
- (D) Store `time.monotonic()` values

### Q18. Cairo switches from +03:00 to +02:00 on 2026-10-29. Which hour is ambiguous in Cairo that day?
**Difficulty:** Hard

- (A) 00:00–00:59
- (B) 02:00–02:59 (clocks fall back from 03:00 to 02:00)
- (C) 09:30–10:29
- (D) No hour — Egypt has no DST

### Q19. What is the output?
**Difficulty:** Hard

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
ny = ZoneInfo("America/New_York")
d = datetime(2026, 3, 8, 2, 30).replace(tzinfo=ny)
print(d.astimezone(timezone.utc).astimezone(ny).strftime("%H:%M %z"))
```

- (A) `02:30 -0500`
- (B) `03:30 -0400`
- (C) `02:30 -0400`
- (D) `03:30 -0500`

### Q20. A log line contains `2026-08-06T09:00:00+02:00`. Which is the correct instant in UTC?
**Difficulty:** Hard

- (A) `2026-08-06T09:00:00Z`
- (B) `2026-08-06T11:00:00Z`
- (C) `2026-08-06T07:00:00Z`
- (D) `2026-08-06T09:00:00+00:00` — the offset is cosmetic

---

## Answer Key

### Q1 — (B)
`tzinfo` is the only difference. Microseconds exist in both; `fold` only
matters on aware datetimes; neither stores a timestamp.
- (A) naive datetimes have microseconds too.
- (C) datetimes don't store Unix timestamps internally.
- (D) `fold` is an attribute, not the defining feature of awareness.

### Q2 — (C)
`datetime.now(timezone.utc)` returns aware UTC — the correct idiom.
- (A) `utcnow()` is removed in 3.13 and was naive anyway.
- (B) `now()` without an argument returns naive *local* time.
- (D) `time.time` has no `utc` parameter; it returns an epoch float.

### Q3 — (B)
`zoneinfo.ZoneInfo("Africa/Cairo")` loads IANA data (3.9+).
- (A) `pytz` is third-party legacy, not the stdlib accessor.
- (C/D) no such stdlib APIs.

### Q4 — (A)
One second after the epoch is `1.0`.
- (B) `0.0` is the epoch itself.
- (C) `1e9` is 2001-09-09.
- (D) the datetime is aware, so `timestamp()` works fine.

### Q5 — (B)
Mixing naive and aware raises `TypeError` by design — comparisons and
arithmetic between them are undefined.
- (A/C) would silently treat 12:00 local as 12:00 UTC — the exact bug the
  error prevents.
- (D) wrong exception type.

### Q6 — (B)
03:00 UTC + 9 hours = 12:00 JST, same calendar day.
- (A) keeps the UTC wall time — a wrong instant.
- (C) subtracts 9 hours — the wrong direction.
- (D) `astimezone` always converts; the offset must change.

### Q7 — (B)
02:30 on spring-forward day doesn't exist. `replace(tzinfo=...)` attaches
the pre-transition offset (−05:00) by convention, so it round-trips to
03:30 EDT.
- (A) that's *fall* back — ambiguity, not a gap.
- (C) wrong offset for that day.
- (D) nothing "resolves to 03:00" — the resolution is to the shifted time.

### Q8 — (B)
`fold=0` gives the first occurrence (EDT, −04:00), `fold=1` the second
(EST, −05:00) — two different instants, so `==` is `False`.
- (A) would mean both were the same instant — the whole point of `fold`
  is that they aren't.
- (C) both are aware; no error.
- (D) `==` on datetimes returns a bool.

### Q9 — (A)
An offset in the string makes the result aware, and 12:00+00:00 is 12:00
UTC.
- (B) no timezone conversion happens in parsing.
- (C) the offset makes it aware.
- (D) `fromisoformat` handles offsets natively.

### Q10 — (B)
`astimezone` expresses the same instant in another zone.
- (A) `replace` *reattaches* the zone label without converting — 12:00 UTC
  becomes "12:00 NY" — a different instant.
- (C) rebuilds a new naive-ish time, same reattachment problem.
- (D) manual offset math breaks during DST transitions.

### Q11 — (B)
Advance the naive local date and re-attach the zone each day; zoneinfo
handles transitions. DST-safe scheduling.
- (A) drifts one hour per transition (10:30 after spring-forward).
- (C) 07:30 UTC is correct only half the year in Cairo.
- (D) `monotonic` measures durations, not wall-clock instants.

### Q12 — (A)
Mar 1 + 30 days = Mar 31. `timedelta` days are calendar days on `date`.
- (B) that would be 29 days.
- (C) that would be 31 days.
- (D) `date + timedelta` is fully supported.

### Q13 — (C)
`monotonic` never jumps (NTP, clock edits, DST) — the only correct
duration clock.
- (A/B) wall clocks can jump backward/forward.
- (D) `date.today()` has day granularity and isn't monotonic.

### Q14 — (B)
Cairo is UTC+3 in summer: 09:00 local = 06:00 UTC.
- (A) keeps local wall time as UTC — a different instant.
- (C) applies the offset backwards.
- (D) the offset in the output must be `+00:00` after converting to UTC.

### Q15 — (B)
`utcnow()` returns naive UTC; comparing/storing it treats it as local
wall time — silent data corruption. (Deprecated in 3.12, removed in 3.13.)
- (A) it's fast; that's not the issue.
- (C) it doesn't raise; it's silently wrong — worse.
- (D) it returns a datetime, but naive.

### Q16 — (B)
02:30 on 2026-03-08 is a gap; `replace` keeps the pre-transition offset
−05:00 (`-1 day, 19:00:00` is timedelta's rendering of −05:00).
- (A) `0:00:00` is UTC's offset, not NY's.
- (C) −04:00 is the post-transition offset; the gap resolves with the
  pre-transition one.
- (D) no error — the resolution is conventional, not an exception.

### Q17 — (C)
Store aware UTC (or epoch); convert to local only for display.
- (A) local wall times are ambiguous during fall-back.
- (B) naive UTC is `utcnow()` territory — offset dropped.
- (D) monotonic values have no calendar meaning at all.

### Q18 — (B)
Egypt falls back at 03:00 → 02:00, so 02:00–02:59 happens twice.
- (A) 00:00 was verified unambiguous (both folds give +03:00).
- (C) 09:30 is a normal hour, no overlap.
- (D) Egypt resumed DST in 2023; 2026 has both transitions.

### Q19 — (B)
The gap 02:30 resolves to 07:30 UTC; converting back to NY after
the transition yields 03:30 −04:00.
- (A) would mean the time existed — it didn't.
- (C) mixes the non-existent time with the new offset.
- (D) wrong offset for the resolved instant.

### Q20 — (C)
+02:00 means local = UTC + 2, so 09:00 local = 07:00 UTC.
- (A) ignores the offset entirely.
- (B) applies the offset in the wrong direction.
- (D) the offset is exactly the point — it converts the wall time to an
  instant.
