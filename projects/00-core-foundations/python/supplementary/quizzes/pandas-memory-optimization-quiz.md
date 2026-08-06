# Pandas Memory Optimization Quiz (Topic 40)

## Topic Overview
This quiz covers memory-aware pandas: dtype selection (`category`,
`int8`, `float32`), `memory_usage` and `info(memory_usage="deep")`,
downcasting, chunked processing, copy-on-write, and when category dtypes
backfire.

**Difficulty:** Intermediate
**Questions:** 20 (6 Easy, 9 Medium, 5 Hard)
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**Which method reports the memory usage of a DataFrame?**

A) `df.memory_usage()`
B) `df.size`
C) `df.bytes`
D) `df.heap()`

**Correct Answer:** A
**Explanation:** `df.memory_usage()` returns per-column bytes. Pass
`deep=True` to include object contents (`str` values are stored as Python
objects, which `deep=True` counts).

---

### Question 2 [Easy]
**What is the most memory-efficient dtype for a column with only 3 distinct
values out of 100,000 rows?**

A) `object`
B) `int64`
C) `category`
D) `float64`

**Correct Answer:** C
**Explanation:** A `category` dtype stores the codes (small ints) once per
row plus a small list of unique categories. With only 3 distinct values the
savings vs `object` are huge (~50x in the exercise's 100k-string example).

---

### Question 3 [Easy]
**What is the smallest signed integer dtype in pandas?**

A) `int8`
B) `int16`
C) `int32`
D) `int64`

**Correct Answer:** A
**Explanation:** `int8` stores 1 byte per value and holds -128..127.
Pandas supports `int8` through `int64` (plus unsigned variants).

---

### Question 4 [Easy]
**What does `df.info(memory_usage="deep")` do?**

A) Prints the DataFrame to the console
B) Shows dtypes, non-null counts, and DEEP memory usage including object
string contents
C) Deletes unused columns
D) Compresses the DataFrame

**Correct Answer:** B
**Explanation:** `df.info(memory_usage="deep")` counts the memory of every
object inside object columns (each Python `str` is a full object), giving a
true picture for text-heavy frames.

---

### Question 5 [Easy]
**Why does `pd.read_csv(path, chunksize=...)` matter for memory?**

A) It reads the file faster
B) It returns an iterator of row chunks instead of one giant DataFrame
C) It deduplicates rows
D) It validates the CSV

**Correct Answer:** B
**Explanation:** `chunksize` returns a `TextFileReader` iterator; each chunk
is a small DataFrame. You process, aggregate, and discard — peak memory
stays bounded instead of materializing the whole file.

---

### Question 6 [Easy]
**What is copy-on-write (CoW) in pandas 2.x/3.x?**

A) A function that copies DataFrames
B) A rule: operations share data until a write happens, then copy
C) A version control system for DataFrames
D) A dtype for text

**Correct Answer:** B
**Explanation:** Under CoW, derived frames share underlying data lazily;
the first mutation triggers a copy. This makes "views" behave predictably
and is the pandas 3.x default. Chained writes that relied on views change
behavior.

---

### Question 7 [Medium]
**Which column saves the MOST memory when converted to `category`?**

A) 1,000,000 rows with 900,000 distinct values
B) 1,000,000 rows with 5 distinct values
C) 1,000 rows with 5 distinct values
D) 1,000,000 rows of float64

**Correct Answer:** B
**Explanation:** Category savings come from low cardinality: codes are small
ints, categories are unique. High-cardinality columns (like A) can LOSE
memory because the codes add an int column and the category list still
exists — the exercise measured 8.5 MB vs 6.0 MB for a high-card column.

---

### Question 8 [Medium]
**What is the output of `pd.Series(["a"] * 100_000, dtype="object").memory_usage(deep=True)` compared to the `category` version?**

A) object is much larger (each str is a separate Python object)
B) They are equal
C) category is larger
D) It depends on the machine

**Correct Answer:** A
**Explanation:** Object stores 100,000 separate Python string objects
(~5.4 MB in the exercise); category stores 100,000 codes (~0.1 MB) plus one
copy of the string. Savings grow with repetition.

---

### Question 9 [Medium]
**Why must you downcast BEFORE any arithmetic that could overflow?**

A) Downcast changes column names
B) `int8` max is 127 — a later `+1` could overflow silently (wraparound)
C) Downcast removes NaN
D) It makes the chain slower

**Correct Answer:** B
**Explanation:** Small ints are real limits. If you downcast a column whose
range fits `int8` today, any operation that pushes past 127 wraps around
silently. Downcast as the LAST step, and only when you know the range.

---

### Question 10 [Medium]
**Which of these converts a column to the smallest float that fits?**

A) `df["x"].astype("float32")`
B) `df["x"].astype("float16")` — smallest float always
C) `pd.to_numeric(df["x"], downcast="float")`
D) `df["x"].astype("float64")`

**Correct Answer:** C
**Explanation:** `to_numeric(downcast="float")` picks the smallest float
dtype that can represent the data (float32, or float64 if needed).
Casting to a fixed small float (A/B) can silently lose precision.

---

### Question 11 [Medium]
**In a chunked `read_csv` loop, what is the correct accumulation pattern for
a mean?**

A) `total = sum(mean_of_each_chunk) / n_chunks`
B) Accumulate `sum` and `count` per chunk, then divide at the end
C) Keep all chunks in a list, then concat
D) Take the mean of the first chunk

**Correct Answer:** B
**Explanation:** A mean of chunk means is wrong (chunks differ in size).
Accumulate weighted sums and counts, then `total_sum / total_count`. C
defeats the purpose — it materializes everything.

---

### Question 12 [Medium]
**What does the exercise's 10^6-row chunked-vs-full comparison show about
peak memory?**

A) Chunked peak ≈ full-read peak (both materialize everything)
B) Chunked peak is much lower (~109 MB vs ~141 MB for a ~27 MB CSV)
C) Full read uses less memory than chunked
D) Chunked read is slower but identical memory

**Correct Answer:** B
**Explanation:** A full `read_csv` builds the DataFrame plus parse buffers
at once. Chunked processing bounds the working set — the measured ceiling
guard (130 MB) cleanly separates the honest chunked implementation from a
naive full materialization.

---

### Question 13 [Medium]
**Which of these is NOT affected by copy-on-write semantics?**

A) `sub = df.iloc[:2]; sub["c"] = 1` (write on a slice)
B) `df.copy()` deep copies
C) `df.loc[mask, "col"] = x` on the original frame
D) Chained writes through an alias

**Correct Answer:** B
**Explanation:** Under CoW, derived frames copy on their own mutation, so
writes through aliases/slices no longer reach the parent (A, D change
behavior). A deep `df.copy()` always copies — CoW does not change that.

---

### Question 14 [Medium]
**Why does `memory_usage()` on an object column undercount without
`deep=True`?**

A) It only counts the first 100 rows
B) It counts the 8-byte pointer per cell, not the string objects they point
to
C) Object columns are free
D) It counts strings but not dtypes

**Correct Answer:** B
**Explanation:** Object columns store 8-byte references. The actual `str`
objects live on the heap; `deep=True` walks them and adds their size. For
text-heavy frames the difference is enormous.

---

### Question 15 [Medium]
**What is the safest order for a memory-optimizing chain?**

A) Downcast everything first, then drop duplicates
B) Analyze range/cardinality, then downcast/convert as the last steps,
then verify values survived
C) Convert to category for every column
D) Drop rows first, then measure

**Correct Answer:** B
**Explanation:** Optimization must be grounded in measurement: check ranges
and cardinalities, apply conversions, and re-verify values (float32
rounding, int wraparound, category losses) before trusting the result.

---

### Question 16 [Hard]
**What is the output of the following code?**

```python
import numpy as np, pandas as pd
s = pd.Series([0.1, 0.2, 0.3], dtype="float64")
t = s.astype("float32")
print(abs(t.iloc[0] - s.iloc[0]))
```

A) `0.0`
B) A small nonzero value (~1e-8) — float32 rounds
C) `1.0`
D) `TypeError`

**Correct Answer:** B
**Explanation:** float32 has ~7 significant digits. 0.1 is not exactly
representable in binary; the float64 and float32 roundings differ, so the
difference is tiny but nonzero (the exercise measured 2.98e-08). Downcast
only when precision loss is acceptable.

---

### Question 17 [Hard]
**A column of 100,000 strings has 95,000 distinct values. Converting to
`category` will MOST LIKELY:**

A) Save ~50x memory
B) Lose memory — the exercise measured 8,513,708 bytes vs 6,000,132 for object
C) Save exactly 8 bytes per row
D) Be impossible

**Correct Answer:** B
**Explanation:** High cardinality means codes buy nothing while the category
structure (and the strings themselves) still exist. The exercise measured a
category column LARGER than the object column. Always measure; never assume
category is free.

---

### Question 18 [Hard]
**Under CoW enabled, `df2 = df.copy(deep=False); df2["x"] = 99` — what does
`df["x"]` contain afterwards?**

A) 99 — shallow copy shares data
B) The original values — CoW copies on the write
C) NaN
D) `KeyError`

**Correct Answer:** B
**Explanation:** `copy(deep=False)` shares blocks, but under CoW the first
mutation of `df2` copies-on-write, leaving `df` untouched. In the exercise,
CoW-on gave `[1, 2, 3]` while CoW-off propagated `[99, 2, 3]` — a
behavioral difference you must design for.

---

### Question 19 [Hard]
**Why is `pd.DataFrame({"id": np.arange(100_000)}).info(memory_usage="deep")`
smaller on Windows than on Linux?**

A) Windows uses int16
B) numpy `randint`-style creation yields int32 on Windows platforms
C) Linux compresses integers
D) It is not smaller

**Correct Answer:** B
**Explanation:** On Windows, numpy's default integer generation can yield
int32 (4 bytes) rather than int64 (8 bytes). The same logical column can
therefore have different sizes across OSes — one more reason to measure
instead of assume.

---

### Question 20 [Hard]
**Which approach correctly computes a global mean from chunked reads?**

```python
# (A)
total_sum = total_count = 0
for chunk in pd.read_csv("f.csv", chunksize=10_000):
    total_sum += chunk["x"].sum()
    total_count += chunk["x"].count()
print(total_sum / total_count)
```

A) A is correct
B) A is wrong — `count()` skips NaN, so the denominator undercounts; use
`len(chunk)` to include NaN rows
C) A is wrong — chunk sums are biased
D) B and C

**Correct Answer:** B
**Explanation:** The weighted accumulation (sum/count) is right, but if NaN
should count as missing in the denominator, `count()` (non-NaN only)
understates the divisor. Whether you use `count()` or `len()` depends on
whether missing values are part of the population — a semantic decision,
not an arithmetic one.

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|---|--------|
| 1 | A | 6 | B | 11 | B | 16 | B |
| 2 | C | 7 | B | 12 | B | 17 | B |
| 3 | A | 8 | A | 13 | B | 18 | B |
| 4 | B | 9 | B | 14 | B | 19 | B |
| 5 | B | 10 | C | 15 | B | 20 | B |

## Scoring Guide

| Score | Proficiency |
|-------|-------------|
| 18-20 | Expert — you can make real pipelines memory-bounded |
| 14-17 | Proficient — review category vs cardinality and CoW |
| 10-13 | Developing — redo lecture 40 and the downcast chain |
| < 10 | Beginner — study dtypes and `memory_usage` first |
