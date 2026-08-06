# Pandas Method Chaining Quiz (Topic 39)

## Topic Overview
This quiz covers the method-chaining style in pandas: `assign`/`pipe` for
adding columns, callable vs precomputed arguments, `query`/`loc` for
filtering, chained reads, the `_verify`-style debugging loop, and when
chaining is the wrong tool (SettingWithCopyWarning, in-place mutation).

**Difficulty:** Intermediate
**Questions:** 20 (6 Easy, 9 Medium, 5 Hard)
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What does `df.assign(x=1)` return?**

A) `None` (mutates `df` in place)
B) A new DataFrame with a column `x` equal to 1
C) A copy of `df` with no changes
D) A Series of 1s

**Correct Answer:** B
**Explanation:** `assign` is non-destructive: it returns a NEW DataFrame with
the added columns and leaves `df` untouched. It is the chainable alternative
to `df["x"] = 1`, which mutates in place.

---

### Question 2 [Easy]
**Which expression filters `df` with a query string?**

A) `df[df.a > 5]`
B) `df.query("a > 5")`
C) `df.loc["a > 5"]`
D) `df.filter("a > 5")`

**Correct Answer:** B
**Explanation:** `query` accepts a condition as a string, which is chainable
and often more readable inside a pipeline. `df[df.a > 5]` works too, but it
is not a string expression.

---

### Question 3 [Easy]
**What does `df.pipe(f)` do?**

A) Writes `df` to disk
B) Calls `f(df)` and returns the result
C) Pipes rows to a subprocess
D) Converts `df` to a numpy array

**Correct Answer:** B
**Explanation:** `pipe` passes the DataFrame to an external function
(`f(df)`) and returns whatever `f` returns. It lets you plug plain functions
into a chain without breaking the pipeline.

---

### Question 4 [Easy]
**Why is a two-step write like `df[df.a > 2]["flag"] = 1` dangerous?**

A) It is slow but correct
B) It may operate on a copy, so the write silently vanishes
C) It always raises an exception
D) It mutates the global frame

**Correct Answer:** B
**Explanation:** `df[mask]` returns a selection, then `["flag"] = 1` writes
through a second selection. pandas may give you a copy, in which case the
write is lost (with a `SettingWithCopyWarning`). Use one `.loc` selection.

---

### Question 5 [Easy]
**What is the main benefit of method chaining over sequential statements?**

A) It is always faster
B) Each step is an expression, so intermediate variables are avoided
C) It uses less memory by default
D) It automatically validates the result

**Correct Answer:** B
**Explanation:** Chaining turns each transformation into an expression
(`df.read()....assign(...).query(...)`), so you never accumulate throwaway
intermediate DataFrames as variables. Speed and memory depend on the
operations themselves, not the style.

---

### Question 6 [Easy]
**Which of these is a valid use of `assign` with a callable?**

A) `df.assign(mean=df["x"].mean())`
B) `df.assign(mean=lambda d: d["x"].mean())`
C) `df.assign(mean="x")`
D) `df["mean"] = lambda d: d["x"].mean()`

**Correct Answer:** B
**Explanation:** A callable passed to `assign` receives the current DataFrame
and returns the column values. This is critical for **incremental** chains
where later columns depend on columns added earlier in the same chain.

---

### Question 7 [Medium]
**In `df.assign(a=lambda d: d["x"] + 1, b=lambda d: d["a"] * 2)`, what does
column `b` see when it evaluates?**

A) The original `df` — column `a` is not visible
B) The DataFrame with column `a` already added
C) `None` — evaluation is lazy
D) A copy of the original frame

**Correct Answer:** B
**Explanation:** `assign` applies callables **in order** (left to right), so
later callables see earlier added columns. This is the classic incremental
chain: `b` = `(x + 1) * 2`. Precomputed values cannot do this.

---

### Question 8 [Medium]
**When is a precomputed (non-callable) argument to `assign` correct?**

A) Always — it is simpler
B) When the value is a constant or does not depend on the DataFrame
C) When it is computed from a different DataFrame
D) Both B and C

**Correct Answer:** D
**Explanation:** A precomputed value is fine when it does not depend on the
current chain state — e.g., a scalar constant or a Series computed from an
unrelated frame. If it depends on the evolving DataFrame, use a callable.

---

### Question 9 [Medium]
**What does `df.query("plan == 'free' and spend > 0")` select?**

A) Rows where plan is free OR spend > 0
B) Rows where plan is free AND spend > 0
C) An error — `and` is invalid in query
D) All rows

**Correct Answer:** B
**Explanation:** Inside a `query` string, `and`/`or` are valid operators
(they combine the two boolean conditions). Outside `query`, Python's
`and`/`or` on Series raise ambiguity errors — use `&`/`|` with parentheses.

---

### Question 10 [Medium]
**What happens when a chain step fails inside a long pipeline?**

A) The whole chain silently skips the step
B) An exception propagates, but you have no idea which step failed
C) The exception tells you the exact failing line, but the chain is hard to
debug because intermediates are not named
D) pandas rolls back to the original frame

**Correct Answer:** C
**Explanation:** The traceback points to the line of the exception, but
because every step is one expression, you cannot inspect the intermediate
state. The fix: temporarily break the chain into named steps, or use the
`_verify`-style loop (run + print + assert) until the chain is green.

---

### Question 11 [Medium]
**Why does `df.assign(rank=df["spend"].rank(ascending=False))` not always
match a chain that sorts by spend first?**

A) `rank` is not available in assign
B) `rank` computes on the original row order, while the sorted chain changes
row order and index labels, so later joins/indexing align differently
C) `rank` always returns integer ranks
D) Sorting removes rows

**Correct Answer:** B
**Explanation:** Precomputed Series align by index **label**. If the chain
sorts or filters rows, the labels no longer line up with the chain's rows.
Use callables (which receive the current DataFrame) whenever the chain
changes row order.

---

### Question 12 [Medium]
**What is the output of the following code?**

```python
import pandas as pd
df = pd.DataFrame({"x": [1, 2, 3]})
result = df.assign(x2=lambda d: d["x"] * 2).query("x2 > 3")
print(result.shape)
```

A) `(3, 2)`
B) `(2, 2)`
C) `(2, 3)`
D) `(3, 3)`

**Correct Answer:** B
**Explanation:** `assign` adds column `x2` = [2, 4, 6] (frame is 3 rows x 2
columns), then `query("x2 > 3")` keeps rows where x2 is 4 and 6 — 2 rows.
Shape is (2, 2).

---

### Question 13 [Medium]
**Which of the following is the chainable form of the mutation
`df["total"] = df["a"] + df["b"]`?**

A) `df.assign(total=lambda d: d["a"] + d["b"])`
B) `df.pipe(lambda d: d.assign(total=d["a"] + d["b"]))`
C) `df.assign(total=df["a"] + df["b"])`
D) A and C both work and are equivalent here

**Correct Answer:** D
**Explanation:** When the source columns already exist in `df`, a precomputed
Series works. Both A (callable) and C (precomputed) produce the same result
in this simple case. The callable version is safer when later chain steps
change the frame.

---

### Question 14 [Medium]
**What does the following code print?**

```python
import pandas as pd
s = pd.Series([3, 1, 2])
print(s.rename("v").sort_values().reset_index(drop=True).tolist())
```

A) `[1, 2, 3]`
B) `[3, 1, 2]`
C) `[0, 1, 2]`
D) `[2, 1, 3]`

**Correct Answer:** A
**Explanation:** `sort_values()` orders the values [1, 2, 3], then
`reset_index(drop=True)` gives a fresh 0-based index, `.tolist()` extracts
the values. The `rename("v")` names the Series but does not affect values.

---

### Question 15 [Medium]
**Which chain produces a DataFrame with exactly one column named `total`?**

A) `df.assign(total=1)` — DataFrame with original columns plus `total`
B) `df[["a"]].assign(total=lambda d: d["a"] * 2)`
C) `df.loc[:, ["a"]].assign(total=lambda d: d["a"] * 2).filter(["total"])`
D) `df.assign(total=lambda d: d["a"] * 2).drop(columns=["a"])`

**Correct Answer:** C
**Explanation:** A and B keep the original columns. D drops `a` but keeps
all other original columns. Only C filters down to exactly `total`.
(Depending on the original frame, D would keep `b`, `c`, …)

---

### Question 16 [Hard]
**Why does the chained two-step write NOT raise, even though the write is
lost?**

```python
import warnings, pandas as pd
df = pd.DataFrame({"a": [1, 2, 3, 4]})
df["flag"] = 0
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df[df["a"] > 2]["flag"] = 1
print(df["flag"].sum())
```

A) It raises `AttributeError`, so the print never runs
B) The write succeeds — sum is 2
C) The write targets a copy; the warning is emitted but the frame is
unchanged — sum is 0
D) `df["flag"] = 0` overwrites the write later

**Correct Answer:** C
**Explanation:** `df[df["a"] > 2]` selects rows, `["flag"] = 1` writes into
that selection — which pandas may have copied. With
`warnings.simplefilter("always")` you catch the `SettingWithCopyWarning`,
but the original frame still holds `flag == 0` everywhere, so the sum is 0.

---

### Question 17 [Hard]
**In pandas 2.2.3, which two-step write does NOT emit a
`SettingWithCopyWarning` (category-detected via
`w.category.__name__`)?**

A) `sub = df[df["a"] > 1]; sub["flag"] = 1`
B) `df.loc[df["a"] > 1]["flag"] = 1`
C) `sub = df.iloc[:2]; sub["flag"] = 1`
D) All of them warn

**Correct Answer:** B
**Explanation:** `loc[...]` returns a view in a way pandas can track;
writing through `df.loc[mask]["col"] = x` does not always trigger the
warning in 2.2.3 — but it is STILL a chained write and may not stick. The
lesson: do not rely on warning detection; use a single `.loc[mask, col] = x`.

---

### Question 18 [Hard]
**What is the output?**

```python
import pandas as pd
df = pd.DataFrame({"plan": ["free", "pro", "free", "pro"],
                   "spend": [5, 20, 1, 30]})
out = (df.assign(pct=lambda d: d["spend"] / d["spend"].sum())
         .query("plan == 'pro'")
         .sort_values("pct", ascending=False))
print(out["pct"].round(2).tolist())
```

A) `[0.54, 0.36]`
B) `[0.36, 0.54]`
C) `[0.54, 0.36, 0.09, 0.02]`
D) `[0.09, 0.02]`

**Correct Answer:** A
**Explanation:** `pct` = spend / total spend (5+20+1+30 = 56) → pro rows are
20/56 ≈ 0.36 and 30/56 ≈ 0.54. `query` keeps only pro rows (2 rows), then
`sort_values(..., ascending=False)` orders 0.54 before 0.36.

---

### Question 19 [Hard]
**Why does comparing precomputed `assign` vs callable `assign` matter when
the chain contains `sort_values`?**

A) Precomputed Series align by label, so rows reordered by the chain no
longer match positions
B) Callables run faster
C) `sort_values` drops the index
D) It does not matter

**Correct Answer:** A
**Explanation:** `assign` with a precomputed Series aligns it to the current
frame by **index label**. After `sort_values`, the labels are in a different
row order, so the values land on the wrong rows. Callables receive the
current frame and compute on it directly, so they are always correct.

---

### Question 20 [Hard]
**Which chain is the cleanest equivalent of these statements?**

```python
df = df.dropna(subset=["email"])
df["domain"] = df["email"].str.split("@").str[1]
df = df[df["domain"].isin(["gmail.com", "outlook.com"])]
```

A) `df.dropna(subset=["email"]).assign(domain=lambda d: d["email"].str.split("@").str[1]).query("domain in ['gmail.com', 'outlook.com']")`
B) `df.dropna(subset=["email"]).assign(domain=df["email"].str.split("@").str[1]).query("domain in ['gmail.com', 'outlook.com']")`
C) `df.assign(domain=lambda d: d["email"].str.split("@").str[1]).dropna(subset=["email"]).query("domain in ['gmail.com', 'outlook.com']")`
D) A and B are equivalent and both correct

**Correct Answer:** A
**Explanation:** The precomputed `df["email"]...` in B is computed from the
ORIGINAL frame and would misalign after `dropna` (labels shifted) — exactly
the callable-vs-precomputed trap. A computes `domain` on the current frame
(callable), after dropna. C also works semantically but computes `domain`
before dropping, which is wasteful.

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|---|--------|
| 1 | B | 6 | B | 11 | B | 16 | C |
| 2 | B | 7 | B | 12 | B | 17 | B |
| 3 | B | 8 | D | 13 | D | 18 | A |
| 4 | B | 9 | B | 14 | A | 19 | A |
| 5 | B | 10 | C | 15 | C | 20 | A |

## Scoring Guide

| Score | Proficiency |
|-------|-------------|
| 18-20 | Expert — you can build and debug production chains |
| 14-17 | Proficient — review callable vs precomputed `assign` |
| 10-13 | Developing — redo lecture 39 and the practice chain |
| < 10 | Beginner — study method chaining before proceeding |
