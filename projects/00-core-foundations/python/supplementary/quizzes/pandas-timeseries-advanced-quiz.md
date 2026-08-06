# Pandas Advanced Time Series Quiz (Topic 41)

## Topic Overview
This quiz covers advanced time series in pandas: DatetimeIndex mechanics,
resampling rules, rolling windows (center, min_periods, closed), asfreq
and reindex, timezone-aware conversion, custom business calendars, lag/diff
features, and no-leakage feature building.

**Difficulty:** Intermediate to Advanced
**Questions:** 20 (6 Easy, 9 Medium, 5 Hard)
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**Which function parses strings into datetime64?**

A) `pd.parse_dates()`
B) `pd.to_datetime()`
C) `pd.datetime()`
D) `pd.str_to_date()`

**Correct Answer:** B
**Explanation:** `pd.to_datetime("2024-01-05")` parses to a Timestamp, and
`pd.to_datetime(df["col"])` converts a whole column. There is no
`pd.parse_dates` or `pd.datetime` in modern pandas.

---

### Question 2 [Easy]
**What does `df.resample("W").mean()` do?**

A) Computes a rolling 7-day mean
B) Groups rows by week and averages each week
C) Repeats each row weekly
D) Converts the index to strings

**Correct Answer:** B
**Explanation:** `resample` groups by fixed time periods (here weekly) and
applies an aggregation. `rolling` is the sliding-window sibling.

---

### Question 3 [Easy]
**What is `s.shift(1)`?**

A) Moves values one position forward, leaving NaN at the start
B) Deletes the first row
C) Rotates values circularly
D) Moves values one position forward, repeating the last

**Correct Answer:** A
**Explanation:** `shift(1)` pushes values down by one; position 0 becomes
NaN. `shift(-1)` pulls values up. It is the core lag operator for feature
engineering.

---

### Question 4 [Easy]
**What does `s.diff()` compute?**

A) The cumulative sum
B) `s - s.shift(1)` — the first difference
C) The rolling mean
D) The percentage change

**Correct Answer:** B
**Explanation:** `diff()` = current minus previous, with NaN at the start.
`pct_change()` is the relative version: `(s - s.shift(1)) / s.shift(1)`.

---

### Question 5 [Easy]
**How do you convert a timezone-naive Series to a specific timezone?**

A) `s.tz_localize("America/New_York")`
B) `s.tz_convert("America/New_York")`
C) `s.astype("tz")`
D) `s.set_timezone("America/New_York")`

**Correct Answer:** A
**Explanation:** `tz_localize` ATTACHES a timezone to naive timestamps.
`tz_convert` CONVERTS between timezones (requires an already-aware index).

---

### Question 6 [Easy]
**What does `s.asfreq("D")` do?**

A) Same as resample — aggregates
B) Changes the frequency to daily, inserting NaN for missing periods
C) Drops duplicate dates
D) Converts to strings

**Correct Answer:** B
**Explanation:** `asfreq` reindexes to the target frequency WITHOUT
aggregating — gaps become NaN (or fill with `ffill`). Resample aggregates
existing rows into bins; asfreq creates empty slots.

---

### Question 7 [Medium]
**For a daily Series 2024-01-01..2024-01-14, what does
`resample("W").mean()` produce?**

A) Two weekly bins labeled by the START of each week
B) Two weekly bins labeled by the END of each week — `[4.0, 11.0]` for the
daily values 1..14
C) One bin for all 14 days
D) 14 daily bins

**Correct Answer:** B
**Explanation:** Weekly resampling buckets days 1-7 and 8-14; labels default
to the bucket END (Sundays), so means are 4.0 and 11.0 in the exercise.
Labeling (start vs end) is controlled by `label=`.

---

### Question 8 [Medium]
**What does `s.rolling(3).mean().shift(1)` produce at row t?**

A) Mean of rows t-2..t
B) Mean of rows t-3..t-1 — the current row is excluded
C) Mean of rows t-2..t-1
D) A constant

**Correct Answer:** B
**Explanation:** `rolling(3)` at row t averages t-2..t; `.shift(1)` moves
that window to t+1, so at row t the window is t-3..t-1 — the no-leak
rolling mean. This is THE pattern for honest time-series features.

---

### Question 9 [Medium]
**Why is `s.rolling(3).mean()` (without shift) a leak for prediction at row
t?**

A) It is too slow
B) It includes row t's own value in the window, which is unknown at
prediction time
C) It drops NaN
D) It uses the future

**Correct Answer:** B
**Explanation:** The window centered on t includes t itself — the value you
are trying to predict. Shifting the window by one makes it past-only.

---

### Question 10 [Medium]
**`df.resample("ME")` — what does the `ME` frequency mean?**

A) Every minute
B) Month end
C) Every Monday
D) Mean of everything

**Correct Answer:** B
**Explanation:** `ME` = Month End (the new alias for the deprecated `M`).
Related aliases: `W` (week), `QE` (quarter end), `YE` (year end).

---

### Question 11 [Medium]
**How do you create a custom trading calendar that skips Jan 15?**

A) `pd.date_range("2024-01-01", "2024-01-31")`
B) `pd.bdate_range("2024-01-01", "2024-01-31")` — skips weekends only
C) Build a DatetimeIndex, drop the unwanted dates, then use it as the index
D) `df.asfreq("B")`

**Correct Answer:** C
**Explanation:** `bdate_range` skips weekends only. For holidays you build
the full range, `.difference()` the holiday dates (or filter), and use the
result as the index — then `reindex`/`asfreq` against it aligns your data
to the custom calendar.

---

### Question 12 [Medium]
**What is the output of the following?**

```python
import pandas as pd
s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0],
              index=pd.date_range("2024-01-01", periods=5, freq="D"))
print(s.asfreq("D").ffill().shape)
```

A) `(5,)`
B) `(5, 2)`
C) `(5, 1)`
D) `(10,)`

**Correct Answer:** A
**Explanation:** `asfreq("D")` on an already-daily index changes nothing;
`ffill()` fills (nothing to fill); shape stays (5,). To see gaps you need a
target frequency with holes (e.g., daily data reindexed to hourly).

---

### Question 13 [Medium]
**A timezone-aware Series from `tz_localize("UTC")` then
`tz_convert("America/New_York")` — which wall time does
`2023-12-31 19:00-05:00` represent in UTC?**

A) `2023-12-31 19:00 UTC`
B) `2024-01-01 00:00 UTC` — the instant is 5 hours later
C) `2023-12-31 14:00 UTC`
D) `2023-12-31 24:00 UTC`

**Correct Answer:** B
**Explanation:** NY is UTC-5 in winter. A NY wall time of 19:00 on Dec 31
is 00:00 Jan 1 UTC — the exercise's "midnight in NYC" instant. tz_convert
changes the wall display, not the instant.

---

### Question 14 [Medium]
**Why must you build features BEFORE splitting train/test?**

A) It is faster
B) Features computed after the split cannot leak — they must be built
identically on train and test, using only past information at each row
C) Pandas requires it
D) It uses less memory

**Correct Answer:** B
**Explanation:** A rolling/lag feature must see only the past at every row.
If you split first and build features separately, each side is built with
the same past-only rule — no future information crosses the boundary. A
feature built on the full series and then split carries future information
into training rows.

---

### Question 15 [Medium]
**What is the output of the following code?**

```python
import pandas as pd
s = pd.Series([10.0, 20.0, 30.0, 50.0])
print(s.pct_change().round(3).tolist())
```

A) `[nan, 1.0, 0.5, 0.667]`
B) `[nan, 10.0, 10.0, 20.0]`
C) `[0.0, 1.0, 0.5, 0.667]`
D) `[nan, 2.0, 1.5, 1.667]`

**Correct Answer:** A
**Explanation:** `pct_change` = `(current - previous) / previous`:
(20-10)/10 = 1.0, (30-20)/20 = 0.5, (50-30)/30 = 2/3. Position 0 has no
previous value → NaN.

---

### Question 16 [Hard]
**A 30-day daily Series has a `rolling(5).mean().shift(1)`. The FIRST row
with a non-NaN value is:**

A) Row 0
B) Row 4
C) Row 5
D) Row 6

**Correct Answer:** C
**Explanation:** `rolling(5)` first has a full window at row 4 (rows 0-4);
`shift(1)` moves that to row 5. So rows 0-4 are NaN and the first valid
value sits at row 5.

---

### Question 17 [Hard]
**For a feature table restricted to rows strictly BEFORE a cutoff, why does
adding a future spike of 10^6 after the cutoff change NOTHING in the
feature values?**

A) Because the spike is too far away
B) Because rolling/lag features at row t use only rows t-window..t-1, and
rows after the cutoff are never in any pre-cutoff window
C) Because pandas ignores large values
D) Because the shift drops it

**Correct Answer:** B
**Explanation:** Every no-leak feature at row t is a function of strictly
earlier rows. A spike AFTER the cutoff never enters any window of rows
before it — the feature table is identical with or without the spike. This
is exactly the property `verify_no_future_leak` asserts structurally.

---

### Question 18 [Hard]
**What is the output of the following code?**

```python
import pandas as pd
s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
               12.0, 13.0, 14.0],
              index=pd.date_range("2024-01-01", periods=14, freq="D"))
print(s.resample("W").mean().tolist())
```

A) `[4.0, 11.0]`
B) `[1.0, 8.0]`
C) `[3.5, 10.5]`
D) `[7.0, 7.0]`

**Correct Answer:** A
**Explanation:** Week bins: days 1-7 mean 4.0; days 8-14 mean 11.0. Labels
default to the bin END (Jan 7, Jan 14) — values are 4.0 and 11.0.

---

### Question 19 [Hard]
**Which resample label semantics does the following code demonstrate?**

```python
import pandas as pd
s = pd.Series([1.0, 2.0, 3.0],
              index=pd.to_datetime(["2024-01-01", "2024-01-08", "2024-01-15"]))
print(s.resample("W").sum().tolist())
```

A) Labels are the first day of each week
B) Labels are the last day of each week; Jan 15 lands in a new bucket with
sum 3.0 — `[3.0, 3.0]`
C) All values sum into one bucket
D) An error — the index must be regular

**Correct Answer:** B
**Explanation:** Weekly buckets end on Sundays: Jan 1 and Jan 8 both fall in
the Jan 7 bucket (sum 1+2 = 3.0), Jan 15 starts the next bucket (3.0).
Resample works on irregular indices — it BINS by the frequency.

---

### Question 20 [Hard]
**Why does `rolling("5D")` (a time-based window) behave differently from
`rolling(5)` on an irregular index?**

A) They never differ
B) `rolling("5D")` includes every row within 5 CALENDAR days of t; `rolling(5)`
always includes exactly 5 rows regardless of spacing
C) `rolling(5)` is faster on irregular data
D) `rolling("5D")` requires a string column

**Correct Answer:** B
**Explanation:** With a DatetimeIndex, `rolling("5D")` is time-based: the
window is "all rows within 5 days", which on an irregular index may contain
a variable number of rows. `rolling(5)` is count-based: exactly 5 rows.
Choosing the wrong one silently changes the feature semantics.

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|---|--------|
| 1 | B | 6 | B | 11 | C | 16 | C |
| 2 | B | 7 | B | 12 | A | 17 | B |
| 3 | A | 8 | B | 13 | B | 18 | A |
| 4 | B | 9 | B | 14 | B | 19 | B |
| 5 | A | 10 | B | 15 | A | 20 | B |

## Scoring Guide

| Score | Proficiency |
|-------|-------------|
| 18-20 | Expert — you can build honest time-series features |
| 14-17 | Proficient — review resample labeling and asfreq |
| 10-13 | Developing — redo lecture 41 and the no-leak chain |
| < 10 | Beginner — study DatetimeIndex basics first |
