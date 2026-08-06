# 03-libraries/pandas (advanced) — 06: String Methods

## Topic Overview

The `.str` accessor exposes vectorized string operations on a Series: `.str.upper()`,
`.str.contains()`, `.str.split()`, `.str.extract()`, `.str.replace()`, and
more — with regex support throughout. Vectorized means the whole column is
processed in C-speed loops instead of a Python `for` over cells.

For AI engineers, string methods are the text-preprocessing layer: cleaning
scraped corpus text, extracting entities with `.str.extract`, tokenizing with
`.str.split`, and filtering by patterns with `.str.contains`. Text features
are the raw material of every NLP/RAG pipeline, and vectorized ops are what
make 10M-row cleaning feasible at all.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use the `.str` accessor for case, strip, length, and padding ops
2. Test and filter with `.str.contains()` (regex/literal)
3. Split and expand with `.str.split(expand=True)`
4. Extract captures with `.str.extract()` / `extractall()`
5. Replace with `.str.replace()` (regex-aware)
6. Handle NaN in string columns (ops return NaN, not errors)
7. Choose vectorized ops over Python loops for text cleaning

## Prerequisites

| Need | Where |
|------|-------|
| Regex | `01-core-python/29-regex.py` lecture |
| Filtering | `03-filtering-lecture.md` |
| Missing data | `04-missing-data-lecture.md` |

## 1. The Basics — Case, Strip, Length

```python
df["text"].str.upper()
df["text"].str.strip()
df["text"].str.len()           # per-cell length
df["text"].str.pad(width=10, side="right")
df["text"].str.zfill(8)        # zero-pad (IDs!)
```

Key property: missing values propagate — `NaN.str.upper()` is `NaN`, never an
error. This is the vectorized-contract you can rely on.

## 2. Testing and Filtering — `.str.contains`

```python
df[df["text"].str.contains("error", case=False)]
df[df["text"].str.contains(r"\d{3}-\d{4}", regex=True)]   # phone pattern
df[df["text"].str.contains("a.b", regex=False)]           # literal "a.b"
df[df["text"].str.startswith("http")]
df[df["text"].str.endswith(".py")]
```

`contains` defaults to regex — always decide whether you mean regex or literal
(`regex=False`). Add `na=False` when the column has missing values you want
treated as "does not match" instead of NaN.

## 3. Splitting — `.str.split`

```python
parts = df["text"].str.split(",")                # list of parts per cell
first, rest = df["text"].str.split(",", n=1, expand=True)
cols = df["text"].str.split(r"\s+", expand=True) # whitespace tokenize
```

`expand=True` turns the split into real columns — the fastest way to split a
"name,age" column into two. `n=` caps the splits; regex splits on `\s+` handle
ragged whitespace.

## 4. Extracting — `.str.extract`

```python
df["code"].str.extract(r"(?P<prefix>[A-Z]{2})-(?P<num>\d+)")
# prefix   num
# AB       123

df["text"].str.extractall(r"@(\w+)")   # every mention per cell -> MultiIndex
```

`extract` pulls named groups into columns; `extractall` finds every match per
cell (all @-mentions) returning a MultiIndex frame. This is the regex
workhorse for structured fields hiding inside text.

## 5. Replacing — `.str.replace`

```python
df["text"].str.replace(r"\s+", " ", regex=True)    # collapse whitespace
df["text"].str.replace("Mr.", "Mister", regex=False)
df["text"].str.replace(r"\d+", "#NUM#")            # redact numbers
```

`replace` is regex by default (note: pandas 3.x will default to literal —
pass `regex=` explicitly to be future-proof). PII redaction pipelines are
built from chains of these.

## 6. Production Pattern — Cleaning Pipeline as Function

```python
def clean_text_series(s: pd.Series) -> pd.Series:
    """One reviewed cleaning contract for corpus text."""
    return (
        s.astype("string")
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"[^\w\s]", "", regex=True)   # strip punctuation
        .str.strip()
    )
```

A single named function is the cleaning contract — applied at intake, reviewed
once, reused everywhere. Ad-hoc cleaning scattered across notebooks is how
train/test skew creeps in.

## Common Mistakes to Avoid

### Mistake 1: `.str.contains` with regex intent mismatch

```python
# WRONG — "a.b" matches "axb" too (regex dot)
df[df.c.str.contains("a.b")]
# CORRECT — literal intent
df[df.c.str.contains("a.b", regex=False)]
```

### Mistake 2: Missing `na=` handling

```python
# WRONG — NaN rows drop out of the filter silently as NaN
df[df.c.str.contains("x")]
# CORRECT — decide the NaN policy
df[df.c.str.contains("x", na=False)]
```

### Mistake 3: Python loop instead of vectorized ops

```python
# WRONG — 10M-row for loop is minutes of Python
clean = [re.sub(r"\s+", " ", t.lower()) for t in df["text"]]
# CORRECT — vectorized
clean = df["text"].str.lower().str.replace(r"\s+", " ", regex=True)
```

### Mistake 4: Forgetting `expand=True` and getting a column of lists

```python
# WRONG — a column of lists; painful downstream
df["parts"] = df["text"].str.split(",")
# CORRECT — real columns
df[["a", "b"]] = df["text"].str.split(",", expand=True)
```

## Best Practices

1. Use `.str` for anything that would otherwise be a Python loop over cells
2. Always state `regex=` intent explicitly on contains/replace
3. Handle NaN explicitly (`na=False` on contains; propagate elsewhere)
4. Prefer `extract` with named groups over manual slicing
5. Keep cleaning in one named function — the reviewable contract
6. Use `expand=True` for splits into columns

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `.str.upper()` | O(n x len) | vectorized, C-speed |
| `.str.contains(regex)` | O(n x pattern) | vectorized regex |
| `.str.split(expand=True)` | O(n x parts) | allocates columns |
| `.str.extract` | O(n x pattern) | named groups -> columns |
| `extractall` | O(n x matches) | one row per match |
| `.str.replace` | O(n x len) | vectorized |
| Python-loop cleaning | O(n) but Python speed | ~100x slower |

**At scale:** vectorized ops keep 10M-row cleaning in seconds; the same in a
Python loop is minutes-to-hours. When regex complexity explodes (nested,
backtracking-heavy patterns), the vectorized call is still one call — but
per-string cost rises, so simplify patterns for big corpora.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| `.str.extract` | pulling structured fields from scraped text |
| `.str.contains` | filtering eval docs, PII scans |
| `.str.replace` | redacting numbers/PII before logging or training |
| `.str.split` | naive tokenization for frequency features |
| `clean_text_series` | the corpus-cleaning contract used by RAG ingestion |
| vectorized ops | making 10M-doc cleaning feasible |

**Scale note:** RAG ingestion pipelines clean millions of chunks before
embedding. A cleaning contract written once and vectorized is the difference
between a pipeline that runs in minutes and one that never finishes.

## Practice Exercises

### Exercise 1: Entity Extraction (Easy)
From a `code` column of `"AB-123"`, `"CD-45"` shape, extract prefix and number
columns with `.str.extract` named groups.

### Exercise 2: Filter with NaN Policy (Medium)
Filter a text column for rows containing the literal substring `"a.b"`,
treating missing values as non-matching (`na=False`), and confirm the count.

### Exercise 3: Cleaning Contract (Hard)
Write `clean_text_series` (lower, strip, collapse whitespace, strip
punctuation) and verify on a mixed column that punctuation is removed, NaN
stays NaN, and the result is `string` dtype.

## Summary

| Concept | Description |
|---------|-------------|
| `.str` accessor | vectorized string ops on a Series |
| `.str.contains` | regex/literal membership filter with `na=` |
| `.str.split(expand=True)` | column splits without lists |
| `.str.extract` | named-group regex extraction to columns |
| `.str.replace` | vectorized cleaning/redaction |
| NaN propagation | missing stays missing, never errors |
| cleaning contract | one named, reviewed function |

String methods are the text layer of pandas: vectorized, regex-powered, and
NaN-safe. Master them and the corpus-cleaning half of every NLP/RAG pipeline
becomes a few reviewed functions.

## Quick Reference

| Task | Idiom |
|------|-------|
| Lowercase | `s.str.lower()` |
| Length | `s.str.len()` |
| Contains (literal) | `s.str.contains("x", regex=False, na=False)` |
| Starts with | `s.str.startswith("p")` |
| Split to columns | `s.str.split(",", expand=True)` |
| Extract groups | `s.str.extract(r"(?P<a>\d+)-(?P<b>\d+)")` |
| All matches | `s.str.extractall(r"@(\w+)")` |
| Replace regex | `s.str.replace(r"\s+", " ", regex=True)` |

## Next Steps

Next: **[07-datetime](07-datetime-lecture.md)** — timestamps and resampling.
Continues in: **[09-genai — 08 document processing](../../../../09-genai/lectures/08-document-processing-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/text.html
