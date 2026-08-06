# Pandas GroupBy Internals Quiz (Topic 42)

## Topic Overview
This quiz covers groupby internals: split-apply-combine, aggregation vs
transformation, `agg` with named/dict specs, `transform` vs `apply` return
shapes, group keys, MultiIndex results, unstack/cohort patterns, and the
sizes/count/unique distinctions.

**Difficulty:** Intermediate
**Questions:** 20 (6 Easy, 9 Medium, 5 Hard)
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What are the three steps of `groupby`?**

A) Sort, filter, aggregate
B) Split, apply, combine
C) Map, reduce, join
D) Slice, dice, merge

**Correct Answer:** B
**Explanation:** Split rows by key values, apply a function to each group,
combine the results. Every groupby operation is this pattern — and the
challenge reimplements it by hand to prove it.

---

### Question 2 [Easy]
**What does `df.groupby("team")["score"].mean()` return?**

A) A DataFrame
B) A Series indexed by team
C) A list
D) A dict

**Correct Answer:** B
**Explanation:** Selecting one column and aggregating returns a Series with
the group keys as index. Selecting multiple columns (a list) returns a
DataFrame.

---

### Question 3 [Easy]
**What is the difference between `size()` and `count()` on a groupby?**

A) They are identical
B) `size()` counts every row (including NaN); `count()` counts non-NaN per
column
C) `count()` counts every row; `size()` skips NaN
D) `size()` is a column, `count()` is a method

**Correct Answer:** B
**Explanation:** `size()` returns the group length (rows), `count()` returns
non-missing values — and for multiple columns, `count()` returns one column
per column of the frame.

---

### Question 4 [Easy]
**What does `df.groupby("team").nunique()` do?**

A) Counts rows per team
B) Counts DISTINCT values per column within each team
C) Drops duplicates globally
D) Returns unique teams

**Correct Answer:** B
**Explanation:** `nunique()` = number of distinct values per column per
group. Used for cohort counting (unique users per month).

---

### Question 5 [Easy]
**Which aggregation computes the team with the highest total spend?**

A) `df.groupby("team")["spend"].sum().idxmax()`
B) `df.groupby("team")["spend"].max()`
C) `df.groupby("team")["spend"].mean().max()`
D) `df.groupby("team")["spend"].agg("total")`

**Correct Answer:** A
**Explanation:** `.sum()` gives per-team totals, `.idxmax()` returns the
index (team) with the largest value. `.max()` would find the largest single
purchase, not the largest team total.

---

### Question 6 [Easy]
**What does `groupby(...).transform("mean")` return?**

A) One row per group
B) A frame the SAME shape as the input, with each value replaced by its
group mean
C) The group means repeated in a list
D) A MultiIndex Series

**Correct Answer:** B
**Explanation:** `transform` broadcasts the aggregation back to the original
shape — every row carries its group's mean. Use it for "demean by group"
patterns without losing rows.

---

### Question 7 [Medium]
**Which of these is a valid named aggregation?**

A) `df.groupby("team").agg(total=("spend", "sum"))`
B) `df.groupby("team").agg({"spend": "sum"}).rename(columns={"spend": "total"})`
C) Both A and B produce a `total` column
D) Only B works — named agg is not supported

**Correct Answer:** C
**Explanation:** The modern `agg(total=("spend", "sum"))` names the output
column directly. The classic dict+rename produces the same result.
`agg("total")` is invalid — "total" is not an aggregation function.

---

### Question 8 [Medium]
**What is the output of the following?**

```python
import pandas as pd
df = pd.DataFrame({"team": ["a", "a", "b"], "x": [1, 2, 3]})
print(df.groupby("team")["x"].agg(["mean", "max"]))
```

A) A flat Series of 3 values
B) A DataFrame with index team and columns mean, max
C) A MultiIndex Series
D) A dict

**Correct Answer:** B
**Explanation:** Passing a list of functions to `agg` produces a DataFrame:
one row per group, one column per function. With multiple columns and
functions you get a MultiIndex.

---

### Question 9 [Medium]
**Why does `df.groupby("team")["x"].apply(lambda g: g + 1)` return rows
WITH the original index, while `transform` is usually safer for this?**

A) `apply` is faster
B) `apply` returns the group frames concatenated; `transform` guarantees
output aligned to the input shape
C) They return identical shapes
D) `apply` drops the index

**Correct Answer:** B
**Explanation:** `apply` is the escape hatch — it can return anything per
group, and pandas does its best to combine; alignment is not guaranteed.
`transform` REQUIRES output aligned with the input, so it fails loudly if
your function changes shape.

---

### Question 10 [Medium]
**`df.groupby("team")[["score", "age"]].agg(["mean", "max", "count"])`
returns a DataFrame whose columns are:**

A) Flat names like "mean", "max", "count"
B) A MultiIndex: (score, mean), (score, max), (score, count), (age, mean), ...
C) A single merged column
D) The teams

**Correct Answer:** B
**Explanation:** With multiple columns and multiple functions, `agg`
produces a column MultiIndex (column, function). Access via
`result[("score", "mean")]`; the challenge's `group_metrics` must match
this layout exactly.

---

### Question 11 [Medium]
**Which expression gives each team's share of total spend?**

A) `df.groupby("team")["spend"].sum() / df["spend"].sum()`
B) `df.groupby("team")["spend"].sum().sum()`
C) `df.groupby("team")["spend"].mean()`
D) `df["spend"] / df.groupby("team")["spend"].sum()`

**Correct Answer:** A
**Explanation:** Team totals divided by the GLOBAL total gives shares that
sum to 1.0 (in the exercise, three teams with spends 1, 2, 3 → shares
1/6, 2/6, 3/6). Option D divides per-row values by the team total — a
within-team fraction, not a global share.

---

### Question 12 [Medium]
**What does `.groupby("team").agg("sum").reset_index()` produce?**

A) A Series
B) A DataFrame with `team` as a regular column instead of the index
C) A MultiIndex
D) A groupby object

**Correct Answer:** B
**Explanation:** `reset_index()` moves the group key from the index back
into a column — the classic "wide groupby result ready to merge" shape.

---

### Question 13 [Medium]
**Why must cohort months-since values be computed from a month INDEX map,
not string subtraction?**

A) Strings are slower
B) `"2024-02" - "2024-01"` is undefined — you need
`pd.unique(months)` mapped to positions (e.g., 0, 1, 2) and subtract those
C) Strings cannot be sorted
D) It is the same

**Correct Answer:** B
**Explanation:** Month arithmetic needs a position map: unique months in
order → 0,1,2... then months_since = month_pos - cohort_pos. The
challenge's `month_idx` Series does exactly this mapping before
`unstack` builds the retention matrix.

---

### Question 14 [Medium]
**What is the output of the following code?**

```python
import pandas as pd
df = pd.DataFrame({"team": ["a", "a", "b"], "x": [1.0, float("nan"), 3.0]})
print(df.groupby("team")["x"].count().tolist())
```

A) `[2, 1]` — NaN counted
B) `[1, 1]` — count skips NaN
C) `[3, 1]`
D) `[2, 2]`

**Correct Answer:** B
**Explanation:** `count()` counts non-NaN values: team a has x = [1.0, NaN]
→ 1; team b has [3.0] → 1. Output is [1, 1]. `size()` would have given
[2, 1] — the NaN row is still a row.

---

### Question 15 [Medium]
**What does `df.groupby("team")["x"].transform("sum")` return for a frame
with teams a,a,b and x = 1, 2, 10?**

A) `[3, 3, 10]`
B) `[1, 2, 10]`
C) `[13, 13, 13]`
D) `[3, 3, 10]` — sum per team broadcast to each row

**Correct Answer:** D (A and D identical — but not `[13, 13, 13]`)
**Explanation:** team a's sum is 3 → both a-rows get 3; team b's sum is 10.
The output keeps the original 3-row shape: [3, 3, 10]. Transform never
aggregates away rows.

---

### Question 16 [Hard]
**The cohort retention matrix divides each row by its cohort SIZE. Why must
the denominator be `nunique(user_id)` per cohort, not the row's own count
at month 0?**

A) They are always equal
B) A user could appear multiple times in one month; the cohort size is the
set of distinct users who started that month
C) nunique is faster
D) Count would overflow

**Correct Answer:** B
**Explanation:** If a user buys twice in their first month, `count` at
month 0 inflates the denominator. The cohort's population is the DISTINCT
users whose first purchase is that month; each month's active users are
also counted via `nunique` before the division.

---

### Question 17 [Hard]
**Why is column 0 of a retention matrix always 1.0?**

A) Because everyone is retained forever
B) Because month 0 is the cohort's own month — every user in the cohort is
active by construction
C) Because of fill_value=0
D) Only if there is no churn

**Correct Answer:** B
**Explanation:** A user is IN the cohort because they purchased that month,
so 100% of them are active in month 0. Retention below 1.0 starts at
column 1 — the fraction returning after the first month, the classic churn
red flag.

---

### Question 18 [Hard]
**`manual_group_mean` in the challenge reimplements groupby. Which
statement about the implementation is TRUE?**

A) It can use `df.groupby(...).mean()` internally
B) It must not call `groupby` — a monkeypatched test raises if it does
C) It must sort the output
D) It must return a Series

**Correct Answer:** B
**Explanation:** The Bronze test monkeypatches `pd.DataFrame.groupby` to
raise. The manual version iterates `df[key].unique()`, filters each group,
means the numeric columns, and concatenates the group means into a
DataFrame indexed by key values.

---

### Question 19 [Hard]
**What is the output of the following code?**

```python
import pandas as pd
df = pd.DataFrame({"k": ["a", "a", "b"], "v": [1, 2, 3]})
g = df.groupby("k")["v"].agg(total="sum", peak="max")
print(g.loc["a", "peak"])
```

A) `3`
B) `2`
C) `1`
D) `KeyError`

**Correct Answer:** B
**Explanation:** Named agg with `total="sum", peak="max"` creates columns
total and peak. For team a, v = [1, 2] → peak = 2.

---

### Question 20 [Hard]
**After `counts.div(sizes, axis=0)`, what does `axis=0` align on?**

A) The user_id index
B) The cohort rows — each row is divided by its own cohort size
C) The month columns
D) Nothing

**Correct Answer:** B
**Explanation:** `div(sizes, axis=0)` aligns the divisor Series by row
index: each retention row (cohort) is divided by that cohort's size.
`axis=1` would align by columns instead — the classic alignment error.

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|---|--------|
| 1 | B | 6 | B | 11 | A | 16 | B |
| 2 | B | 7 | C | 12 | B | 17 | B |
| 3 | B | 8 | B | 13 | B | 18 | B |
| 4 | B | 9 | B | 14 | B | 19 | B |
| 5 | A | 10 | B | 15 | D | 20 | B |

## Scoring Guide

| Score | Proficiency |
|-------|-------------|
| 18-20 | Expert — you understand groupby machinery end to end |
| 14-17 | Proficient — review agg/transform shapes and alignment |
| 10-13 | Developing — redo lecture 42 and the manual group mean |
| < 10 | Beginner — study split-apply-combine basics first |
