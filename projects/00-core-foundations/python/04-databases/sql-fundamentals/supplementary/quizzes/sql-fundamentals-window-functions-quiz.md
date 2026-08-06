# SQL Fundamentals — Window Functions Quiz (Topic 09)

## Topic Overview

Window functions: OVER, PARTITION BY, ORDER BY in windows, ranking
functions (ROW_NUMBER/RANK/DENSE_RANK), navigation (LAG/LEAD), frames
(ROWS BETWEEN), running totals, and moving averages.

- **Difficulty:** 6 Easy, 9 Medium, 5 Hard
- **Questions:** 20
- **Time:** 25 minutes
- **Passing Score:** 16/20 (80%)

---

## Questions

### Question 1 [Easy] — What does adding OVER to an aggregate do?

A. It groups rows and collapses them
B. It computes the aggregate per row without collapsing rows
C. It orders the table permanently
D. It forces a full table scan

**Correct Answer:** B

**Explanation:** A window function keeps one output row per input row
while computing values over a related set of rows — the opposite of
GROUP BY collapse. C and D are false properties of window functions.

---

### Question 2 [Easy] — What does PARTITION BY do?

A. Splits rows into independent groups; windows restart per partition
B. Sorts the whole result set
C. Limits the number of rows
D. Groups rows and collapses them

**Correct Answer:** A

**Explanation:** PARTITION BY divides the rows; every window function
restarts its computation at each partition boundary. B describes
ORDER BY; C describes LIMIT; D describes GROUP BY.

---

### Question 3 [Easy] — What does ROW_NUMBER() assign?

A. A rank with gaps after ties
B. A rank without gaps after ties
C. A unique sequential position per partition
D. The same number to tied rows

**Correct Answer:** C

**Explanation:** ROW_NUMBER gives each row a distinct 1, 2, 3... position
per partition — ties never share a number. A is RANK, B is DENSE_RANK,
D is exactly what ROW_NUMBER avoids.

---

### Question 4 [Easy] — What does LAG(col, 1) return?

A. The value of the next row
B. The value of the previous row
C. The first value of the partition
D. The average of the column

**Correct Answer:** B

**Explanation:** LAG looks backward by the offset (1 = previous row);
LEAD looks forward. C is FIRST_VALUE; D is an aggregate, not
navigation.

---

### Question 5 [Easy] — What is the default frame for a window
function?

A. Only the current row
B. The whole partition (UNBOUNDED PRECEDING to UNBOUNDED FOLLOWING)
C. The last three rows
D. No frame — the function fails

**Correct Answer:** B

**Explanation:** Without a ROWS/RANGE clause, aggregates over windows
compute over the whole partition. C is an invented default; A is the
frame only when explicitly requested.

---

### Question 6 [Easy] — Code Output: RANK vs DENSE_RANK

```sql
SELECT metric, RANK() OVER (ORDER BY metric DESC) r,
       DENSE_RANK() OVER (ORDER BY metric DESC) d
FROM runs;
```

Given metrics `0.9, 0.9, 0.8`, what are the (r, d) columns?

A. `(1,1), (2,2), (3,3)`
B. `(1,1), (1,1), (3,2)`
C. `(1,1), (2,1), (2,3)`
D. `(1,1), (1,1), (2,3)`

**Correct Answer:** B

**Explanation:** Tied rows share a position in both; RANK then leaves a
gap (1, 1, 3), DENSE_RANK does not (1, 1, 2). A treats ties as
distinct; C and D scramble the gap semantics.

---

### Question 7 [Medium] — Code Output: running total frame

```sql
SELECT amt, SUM(amt) OVER (ORDER BY amt
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
FROM runs;
```

Given `1.0, 2.0, 3.0`, what are the cumulative values?

A. `1.0, 2.0, 3.0`
B. `1.0, 3.0, 6.0`
C. `6.0, 6.0, 6.0`
D. `1.0, 1.5, 2.0`

**Correct Answer:** B

**Explanation:** The frame runs from the partition start to the current
row: 1, then 1+2, then 1+2+3. A shows raw values; C is the whole-
partition default; D is a cumulative average.

---

### Question 8 [Medium] — Code Output: moving average edges

```sql
SELECT AVG(amt) OVER (ORDER BY amt
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
FROM runs;
```

Given `1.0, 2.0, 3.0, 4.0`, what are the four values?

A. `1.0, 1.5, 2.0, 3.0`
B. `1.0, 2.0, 3.0, 4.0`
C. `2.0, 2.5, 3.0, 3.5`
D. `1.0, 1.5, 2.0, 2.5`

**Correct Answer:** A

**Explanation:** The frame cannot reach before the partition start: row
1 averages (1), row 2 averages (1+2)/2, then full 3-row windows:
(1+2+3)/3 = 2, (2+3+4)/3 = 3. B skips averaging; C assumes the frame
always has 3 rows; D uses a 2-row window everywhere.

---

### Question 9 [Medium] — Where do windows restart?

A. At every table change
B. At every PARTITION BY boundary
C. At every commit
D. At every new connection

**Correct Answer:** B

**Explanation:** PARTITION BY defines the independent groups; ranking,
navigation, and frames all reset at each boundary. The other options
are unrelated to window semantics.

---

### Question 10 [Medium] — Why add a tiebreaker to the window ORDER BY?

A. To make PARTITION BY optional
B. To make the row order deterministic for equal keys
C. To enable LAG on text columns
D. To speed up the sort

**Correct Answer:** B

**Explanation:** Rows equal on the ORDER BY key are peers — their
relative order is unspecified. A tiebreaker (e.g., `ORDER BY metric
DESC, id`) makes positions deterministic. The other options are false.

---

### Question 11 [Medium] — Code Output: LAG first row

```sql
SELECT metric - LAG(metric, 1) OVER (ORDER BY run_ts)
FROM runs;
```

What is the first row's value?

A. `0`
B. `NULL`
C. The metric itself
D. An error

**Correct Answer:** B

**Explanation:** There is no previous row at the partition start, so
LAG returns NULL — and arithmetic with NULL stays NULL. A assumes a
zero default; C would be FIRST_VALUE; D confuses NULL with an error.

---

### Question 12 [Medium] — Which functions are NOT affected by ROWS
BETWEEN frames?

A. SUM and AVG
B. Ranking functions (ROW_NUMBER, RANK, DENSE_RANK)
C. LAG and LEAD
D. COUNT over windows

**Correct Answer:** B

**Explanation:** Frames define the row set for aggregate-in-window
functions; ranking functions compute over the whole partition
regardless of the frame. A, C, and D all respect frames (C reads
offsets independent of frames but the statement asks about ROWS BETWEEN
semantics — rankings are the functions where the frame is irrelevant).

---

### Question 13 [Medium] — Code Output: SUM without explicit frame

```sql
SELECT region, amt, SUM(amt) OVER (PARTITION BY region)
FROM runs;
```

Given east 10, east 5, west 30, what are the SUM values?

A. `15, 15, 30`
B. `10, 5, 30`
C. `15, 15, 15`
D. `15, 5, 30`

**Correct Answer:** A

**Explanation:** Without a frame, the default is the whole partition:
15 for both east rows, 30 for the single west row. B is the raw amt;
C leaks 15 across partitions; D mixes raw and summed values.

---

### Question 14 [Medium] — What are "peer rows" in a window?

A. Rows from different partitions
B. Rows equal on the window ORDER BY key
C. Rows with the same LAG offset
D. Rows skipped by the frame

**Correct Answer:** B

**Explanation:** Peers share the same ORDER BY key value; they get the
same RANK positions and share frame edges. The other options describe
unrelated concepts.

---

### Question 15 [Medium] — FILTER (WHERE) in a window:

```sql
SUM(amt) FILTER (WHERE amt > 10) OVER (PARTITION BY region)
```

A. Filters rows out of the whole query
B. Restricts which rows a single window function considers
C. Replaces the PARTITION BY
D. Is invalid SQL in SQLite

**Correct Answer:** B

**Explanation:** FILTER narrows the rows for one aggregate-in-window
call without affecting other columns or functions. A would be a WHERE;
C and D are false — SQLite supports FILTER since 3.30.

---

### Question 16 [Hard] — Code Output: partitioned ranking

```sql
SELECT model, ROW_NUMBER() OVER (PARTITION BY model ORDER BY metric DESC) rn
FROM runs;
```

Given bert 0.9, bert 0.9, gpt 0.7, what are the rn values?

A. `1, 2, 1`
B. `1, 1, 1`
C. `1, 2, 2`
D. `2, 1, 1`

**Correct Answer:** A

**Explanation:** ROW_NUMBER restarts at 1 per partition and assigns
distinct positions even on ties: bert gets 1, 2; gpt starts fresh at 1.
B is RANK's tie behavior; C and D break the restart or the distinct
position rule.

---

### Question 17 [Hard] — Why does the first moving-average value use
fewer rows than the window width?

A. The frame cannot extend before the partition start
B. LAG returns NULL there
C. SQLite rounds the frame
D. The ORDER BY is unstable

**Correct Answer:** A

**Explanation:** Frames are bounded by the partition: `2 PRECEDING`
before row 1 reaches only row 1. The truncation is structural, not
rounding (C) or ordering (D); B is about LAG, not frames.

---

### Question 18 [Hard] — Code Output: LAG with offset 2

```sql
SELECT LAG(amt, 2) OVER (ORDER BY run_ts) FROM runs;
```

Given `1.0, 2.0, 3.0, 4.0`, what is returned?

A. `NULL, NULL, 1.0, 2.0`
B. `NULL, 1.0, 2.0, 3.0`
C. `2.0, 3.0, 4.0, NULL`
D. `1.0, 1.0, 1.0, 1.0`

**Correct Answer:** A

**Explanation:** Offset 2 looks two rows back: rows 1 and 2 have no such
row (NULL); row 3 sees 1.0; row 4 sees 2.0. B is offset 1; C is LEAD;
D is nonsense.

---

### Question 19 [Hard] — What does this compute?

```sql
SELECT model, run_ts, metric,
       SUM(metric) OVER (PARTITION BY model ORDER BY run_ts
         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
FROM runs;
```

A. The total metric per model
B. A 3-row sliding sum per model
C. A cumulative sum per model
D. The average metric per model

**Correct Answer:** B

**Explanation:** The frame takes the current row plus two previous —
a 3-row sliding window, truncated at partition starts. A would drop
the ORDER BY/frame; C needs UNBOUNDED PRECEDING; D would use AVG.

---

### Question 20 [Hard] — Which query pairs each run with its rank
within the model WITHOUT a subquery?

A. `SELECT model, RANK() OVER (PARTITION BY model ORDER BY metric DESC) FROM runs`
B. `SELECT model, RANK() FROM runs`
C. `SELECT model, COUNT(*) FROM runs GROUP BY model`
D. `SELECT model, metric FROM runs ORDER BY model`

**Correct Answer:** A

**Explanation:** The OVER clause computes the per-partition rank inline
with no collapse and no subquery. B is invalid — RANK needs OVER; C is
an aggregate count; D returns no rank.

---

## Answer Key

| Q | Difficulty | Answer | Distractor Analysis |
|---|---|---|---|
| 1 | Easy | B | Windows keep rows; GROUP BY collapses |
| 2 | Easy | A | Partition = independent window groups |
| 3 | Easy | C | ROW_NUMBER: unique sequential position |
| 4 | Easy | B | LAG looks backward; LEAD forward |
| 5 | Easy | B | Default frame = whole partition |
| 6 | Easy | B | RANK gaps, DENSE_RANK doesn't |
| 7 | Medium | B | Cumulative frame sums to current row |
| 8 | Medium | A | Frame truncated at partition start |
| 9 | Medium | B | Restart at each partition boundary |
| 10 | Medium | B | Tiebreakers make peer order deterministic |
| 11 | Medium | B | No previous row -> NULL |
| 12 | Medium | B | Rankings ignore frames |
| 13 | Medium | A | Default frame = partition total |
| 14 | Medium | B | Peers share the ORDER BY key |
| 15 | Medium | B | FILTER scopes one function's rows |
| 16 | Hard | A | ROW_NUMBER restarts and stays distinct |
| 17 | Hard | A | Frames are partition-bounded |
| 18 | Hard | A | Offset 2 -> two NULLs first |
| 19 | Hard | B | Sliding 3-row sum |
| 20 | Hard | A | OVER computes rank inline |

## Scoring Guide

| Score | Verdict |
|---|---|
| 18-20 | Window functions mastered — proceed to the advanced quiz |
| 16-17 | Review frames and ranking semantics (questions 6-13) |
| Below 16 | Re-read the window-functions lecture, then retake |
