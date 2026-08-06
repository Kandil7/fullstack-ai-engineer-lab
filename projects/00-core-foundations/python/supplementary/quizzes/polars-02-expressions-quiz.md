# Polars 02 — Expressions Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

Shared frame for most questions:
```python
import polars as pl
df = pl.DataFrame({
    "name": ["alice", "bob", "carol", "dan"],
    "campaign": ["a", "b", "c", "a"],
    "score": [0.9, 0.4, 0.7, 0.2],
    "spend": [10, 20, 30, 40],
})
```

---

## Easy

**E1 (code-output).** What prints?
```python
print(df.select(pl.col("score").mean())["score"].to_list())
```

- A) `[0.55]`
- B) `[0.5]`
- C) `[2.2]`
- D) `[0.55, 0.55, 0.55, 0.55]`

**E2 (code-output).** What prints?
```python
print(df.select(pl.col("spend").sum()).item())
```

- A) `100`
- B) `25`
- C) `10`
- D) `[100]`

**E3.** What does `pl.col("score")` represent?

- A) an expression placeholder for the `score` column
- B) the already-computed score values
- C) a DataFrame subset
- D) a Python list

**E4 (code-output).** What prints?
```python
print(df.filter(pl.col("score") > 0.5).select("campaign", "score").rows())
```

- A) `[('a', 0.9), ('c', 0.7)]`
- B) `[('a', 0.9), ('b', 0.4), ('c', 0.7)]`
- C) `[('c', 0.7)]`
- D) `[('a', 0.9), ('a', 0.2)]`

**E5.** Which is the correct way to rename a computed column?

- A) `(pl.col("spend") / pl.col("score")).alias("cpp")`
- B) `pl.alias("cpp", pl.col("spend") / pl.col("score"))`
- C) `pl.col("spend") / pl.col("score").alias("cpp")`
- D) `(pl.col("spend") / pl.col("score")).name("cpp")`

**E6 (code-output).** What prints?
```python
print(df.select(pl.len()).item())
```

- A) `4`
- B) `1`
- C) `4.0`
- D) `[4]`

---

## Medium

**M1 (code-output).** What prints?
```python
print(df.select((pl.col("spend") / pl.col("score")).alias("cpp"))["cpp"].to_list())
```

- A) `[11.111..., 50.0, 42.857..., 200.0]`
- B) `[0.09, 0.02, 0.0233..., 0.005]`
- C) `[10.0, 20.0, 30.0, 40.0]`
- D) `[9.0, 0.8, 2.1, 0.08]`

**M2 (code-output).** What prints?
```python
print(df.select(pl.col("score").rank(descending=True))["score"].to_list())
```

- A) `[1.0, 3.0, 2.0, 4.0]`
- B) `[4.0, 2.0, 3.0, 1.0]`
- C) `[0.9, 0.4, 0.7, 0.2]`
- D) `[1.0, 4.0, 2.0, 3.0]`

**M3 (code-output).** What prints?
```python
print(df.select(
    pl.when(pl.col("score") > 0.5).then(pl.lit("high")).otherwise(pl.lit("low")).alias("band")
)["band"].to_list())
```

- A) `['high', 'low', 'high', 'low']`
- B) `['high', 'high', 'high', 'low']`
- C) `['low', 'low', 'high', 'low']`
- D) `[True, False, True, False]`

**M4 (code-output).** What prints?
```python
print(df.group_by("campaign").agg(
    pl.col("score").mean().alias("m"),
    pl.col("spend").sum().alias("s"),
    pl.len().alias("c"),
).sort("campaign").rows())
```

- A) `[('a', 0.55, 50, 2), ('b', 0.4, 20, 1), ('c', 0.7, 30, 1)]`
- B) `[('a', 0.9, 10, 1), ('b', 0.4, 20, 1), ('c', 0.7, 30, 1)]`
- C) `[('a', 0.55, 50, 2), ('c', 0.7, 30, 1), ('b', 0.4, 20, 1)]`
- D) `[('a', 2, 50, 0.55), ('b', 1, 20, 0.4), ('c', 1, 30, 0.7)]`

**M5.** Which statement about the `.alias()` precedence trap is true?

- A) `pl.col("spend") / pl.col("score").alias("x")` aliases the
  *division result* because alias binds to the whole expression
- B) `pl.col("spend") / pl.col("score").alias("x")` aliases only
  `score`; the division output keeps the default name
- C) alias always renames the first column mentioned
- D) alias is a no-op outside `select`

**M6 (code-output).** What prints?
```python
print(df.select(pl.col("spend").rank(descending=True))["spend"].to_list())
```

- A) `[4.0, 3.0, 2.0, 1.0]`
- B) `[1.0, 2.0, 3.0, 4.0]`
- C) `[40.0, 30.0, 20.0, 10.0]`
- D) `[10.0, 20.0, 30.0, 40.0]`

**M7 (code-output).** What prints?
```python
print(df.sort("score").select("name").to_series().to_list())
```

- A) `['dan', 'bob', 'carol', 'alice']`
- B) `['alice', 'bob', 'carol', 'dan']`
- C) `['dan', 'carol', 'bob', 'alice']`
- D) `['alice', 'carol', 'bob', 'dan']`

**M8.** `df.with_columns(pl.col("spend").rank(descending=True).alias("r"))`
creates:

- A) a new DataFrame with an added `r` column
- B) a mutated copy of `df` where `spend` is replaced
- C) a view into `df`
- D) an error: rank cannot be combined with with_columns

**M9.** Which expression form is invalid Polars?

- A) `pl.col("spend") + 10`
- B) `pl.col("spend") > pl.col("spend").mean()`
- C) `"spend" > 10` inside `filter`
- D) `pl.col("score").sum().over("campaign")`

---

## Hard

**H1 (code-output).** What prints?
```python
print(df.with_columns(pl.col("spend").rank(descending=True).alias("r"))
      .select("campaign", "score", "r").rows())
```

- A) `[('a', 0.9, 4.0), ('b', 0.4, 3.0), ('c', 0.7, 2.0), ('a', 0.2, 1.0)]`
- B) `[('a', 0.9, 1.0), ('b', 0.4, 3.0), ('c', 0.7, 2.0), ('a', 0.2, 4.0)]`
- C) `[('a', 0.9, 3.0), ('b', 0.4, 4.0), ('c', 0.7, 2.0), ('a', 0.2, 1.0)]`
- D) `[('a', 0.9, 1.0), ('b', 0.4, 2.0), ('c', 0.7, 3.0), ('a', 0.2, 4.0)]`

**H2.** What is the semantic difference between
`df.filter(pl.col("score") > 0.5)` and
`df.select(pl.col("score").filter(pl.col("score") > 0.5))`?

- A) filter keeps whole rows; the inner `.filter()` narrows the column
  and changes its length
- B) they are identical in every case
- C) select raises; only filter is valid
- D) filter is lazy; the inner filter is eager

**H3.** `pl.col("score").mean().over("campaign")` computes:

- A) the mean of `score` within each `campaign` group, broadcast back
  to every row
- B) one global mean applied to every row
- C) the mean per row (nonsense)
- D) an error: `over` is only for rank

**H4.** Which claim about expression composition is true?

- A) expressions compose into bigger expressions and are executed by
  the engine as a single optimized plan
- B) every expression triggers an immediate column computation
- C) expressions can only be used inside `select`
- D) string column names are themselves expressions

**H5.** Given `df.filter(pl.col("score") > 0.5)`, Polars evaluates
the predicate:

- A) per element, vectorized, without Python-level iteration
- B) with a Python for-loop over rows (like a list comprehension)
- C) by converting to pandas first
- D) only for the first row (short-circuit)

---

## Answer Key

**E1 — A.** Mean of `[0.9, 0.4, 0.7, 0.2]` = 2.2/4 = 0.55; select
returns a 1×1 DataFrame, `.to_list()` → `[0.55]`.
*Distractors:* B is a mis-averaged value; C is the sum; D broadcasts
the mean to every row (not what select does).

**E2 — A.** Sum of spend = 10+20+30+40 = 100; `.item()` extracts the
scalar.
*Distractors:* B is the mean; C is the first value; D is the frame
cell without `.item()`.

**E3 — A.** `pl.col("score")` is an *expression* — a lazy description
of "the score column" that the engine executes later.
*Distractors:* B describes an eager Series; C is a DataFrame subset;
D is a list of values.

**E4 — A.** `score > 0.5` keeps alice (0.9) and carol (0.7) only.
*Distractors:* B includes bob (0.4 — not > 0.5); C drops alice; D
selects by campaign membership instead.

**E5 — A.** `.alias("cpp")` renames the whole expression. Because
alias binds tightly to the *nearest* expression, you must wrap the
division in parentheses: `(a / b).alias(...)`.
*Distractors:* B/C invent APIs or misplace the alias (C aliases only
`score`); D uses a non-existent method.

**E6 — A.** `pl.len()` counts rows → 4; `.item()` extracts it.
*Distractors:* B is the number of columns; C would need float
context; D is the cell without `.item()`.

**M1 — A.** spend/score = [10/0.9, 20/0.4, 30/0.7, 40/0.2] =
[11.111…, 50.0, 42.857…, 200.0].
*Distractors:* B is score/spend (the inverse); C is raw spend; D is
spend−score.

**M2 — A.** `rank(descending=True)` — Polars rank defaults to
*ascending*, so descending must be explicit: 0.9→1, 0.4→3, 0.7→2,
0.2→4.
*Distractors:* B is rank without ties on reversed values; C is the raw
scores; D is a different ordering permutation.

**M3 — A.** `when/then/otherwise` is the expression-level if/else:
high for 0.9 and 0.7, low for 0.4 and 0.2.
*Distractors:* B/C misplace one threshold; D would be the raw boolean
predicate, not the band labels.

**M4 — A.** Group by campaign: a has rows 1 and 4 → mean 0.55, spend
sum 50, count 2; b → 0.4/20/1; c → 0.7/30/1; `.sort("campaign")` fixes
the group order.
*Distractors:* B keeps only the first row per group; C is the
unsorted output; D swaps column meanings.

**M5 — B.** `.alias()` binds tighter than arithmetic: it attaches to
`pl.col("score")` only; the division result keeps its default name.
Parenthesize: `(a / b).alias("x")`.
*Distractors:* A is the opposite (the actual trap); C/D invent
behaviors.

**M6 — A.** Spend descending ranks: 40→1, 30→2, 20→3, 10→4 → wait,
`rank(descending=True)` gives largest = 1: spend [10,20,30,40] →
ranks [4.0, 3.0, 2.0, 1.0]. ✓
*Distractors:* B is ascending rank; C/D are the values themselves.

**M7 — A.** Sorting by score ascending: 0.2 (dan), 0.4 (bob), 0.7
(carol), 0.9 (alice).
*Distractors:* B is the original order; C/D are wrong permutations.

**M8 — A.** `with_columns` adds/overwrites columns in a **new**
DataFrame — Polars frames are immutable; nothing is mutated in place.
*Distractors:* B replaces the wrong column (adds `r`, keeps `spend`);
C is false (no views in the pandas sense); D is false (rank +
with_columns is a standard combo).

**M9 — C.** In `filter`, the predicate must be an *expression*; a bare
string `"spend" > 10` is a Python str comparison (TypeError).
*Distractors:* A is valid (literal broadcast); B is valid (column vs
aggregate); D is valid (window function).

**H1 — A.** Spend ranks descending: 40→1.0, 30→2.0, 20→3.0, 10→4.0 —
in row order: alice 10 → 4.0, bob 20 → 3.0, carol 30 → 2.0, dan 40 →
1.0.
*Distractors:* B/D are ascending-rank permutations; C swaps two
values.

**H2 — A.** `filter` keeps whole rows whose predicate is true (length
≤ n); the column-level `.filter(expr)` keeps only matching values
*inside that column*, producing a shorter Series — two different
shapes of the same word.
*Distractors:* B is false — shapes differ; C is false (both are
valid); D inverts the semantics (both are eager here).

**H3 — A.** `.over("campaign")` is a window operation: aggregate per
group, then broadcast the result back to each row of that group.
*Distractors:* B is plain `.mean()`; C is meaningless; D is false —
`over` works with any aggregate.

**H4 — A.** Expressions are composable descriptions; the engine
compiles the whole graph and executes it vectorized — that is the
performance story of Polars.
*Distractors:* B is eager semantics (not Polars); C is false
(expressions appear in filter/group_by/with_columns too); D is false
(column names are strings; expressions wrap them).

**H5 — A.** Predicates are evaluated by the engine in vectorized
fashion — no Python loop per row.
*Distractors:* B describes pandas `apply` style; C is false — Polars
is native; D is false (filters scan all rows).

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 02](03-libraries/polars/lectures/02-expressions-lecture.md) ·
[Glossary 02](03-libraries/polars/lectures/02-expressions-glossary.md) ·
[Challenge 02](03-libraries/polars/challenges/02-expressions/README.md)
