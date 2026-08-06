# Challenge 50 — Quiz: Datetime & Timezones

1. A naive datetime has:
   - A) UTC offset  (B) no tzinfo  (C) DST rules  (D) a zone name
2. `datetime.now(timezone.utc)` returns:
   - A) naive UTC  (B) aware UTC  (C) local time  (D) a timestamp
3. `datetime.utcnow()` is deprecated because it returns:
   - A) local time  (B) naive UTC  (C) a string  (D) a date
4. `astimezone()` changes:
   - A) the instant  (B) the zone, not the instant  (C) the date only  (D) nothing
5. During fall-back, a wall-clock hour:
   - A) never exists  (B) occurs twice  (C) shifts 6 hours  (D) disappears
6. For durations, use:
   - A) `time.time()`  (B) `time.monotonic()`  (C) `datetime.now()`  (D) `time.clock()`
7. `dt.timestamp()` returns:
   - A) ISO string  (B) seconds since epoch  (C) milliseconds  (D) a tuple
8. Mixing naive and aware in arithmetic:
   - A) works  (B) raises TypeError  (C) assumes UTC  (D) truncates

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
