# String Methods — Glossary 06 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `.str` accessor | Accessor | Vectorized string operations on a Series |
| `.str.lower()` | Method | Lowercase each cell |
| `.str.strip()` | Method | Trim whitespace per cell |
| `.str.len()` | Method | Character length per cell |
| `.str.contains()` | Method | Regex/literal membership test (filter) |
| `na=` | Argument | Policy for missing values in string tests |
| `regex=` | Argument | Literal vs regex interpretation |
| `.str.startswith()` | Method | Prefix test per cell |
| `.str.endswith()` | Method | Suffix test per cell |
| `.str.split()` | Method | Split per cell; `expand=True` -> columns |
| `.str.extract()` | Method | First regex capture per cell -> columns |
| `.str.extractall()` | Method | ALL regex captures -> MultiIndex rows |
| `.str.replace()` | Method | Vectorized regex/literal replacement |
| `.str.zfill()` | Method | Zero-pad strings (IDs) |
| vectorized | Concept | Whole-column C-speed operation |
| `astype("string")` | Cast | True pandas string dtype (vs object) |

## Detailed Definitions

### `.str` accessor
**Definition**: The namespace exposing vectorized string methods on a Series;
NaN cells propagate through as NaN.
**Example**:
```python
df["text"].str.lower()
```
**Related**: vectorized, string dtype

### `.str.lower()`
**Definition**: Lowercases every cell — the standard first step of text
cleaning.
**Related**: `.str.upper()`, `.str.strip()`

### `.str.strip()`
**Definition**: Removes leading/trailing whitespace per cell; variants
`lstrip`/`rstrip`.
**Related**: cleaning contracts

### `.str.len()`
**Definition**: Returns the character length per cell — useful for
length-based filters.
**Related**: `.str.contains()`

### `.str.contains()`
**Definition**: Tests whether each cell matches a regex (default) or literal
substring; the vectorized text filter.
**Example**:
```python
df[df["text"].str.contains("error", case=False)]
```
**Related**: `regex=`, `na=`

### `na=`
**Definition**: Argument to string-test methods deciding how missing cells are
treated; `na=False` treats them as non-matching.
**Example**:
```python
df[df["c"].str.contains("x", na=False)]
```
**Related**: `.str.contains()`, missing data

### `regex=`
**Definition**: Explicitly sets regex vs literal interpretation (default
regex for contains/replace in current pandas).
**Related**: `.str.contains()`, `.str.replace()`

### `.str.startswith()`
**Definition**: Prefix test per cell — the cheap string filter.
**Related**: `.str.endswith()`

### `.str.endswith()`
**Definition**: Suffix test per cell.
**Related**: `.str.startswith()`

### `.str.split()`
**Definition**: Splits each cell into parts; `expand=True` returns a frame of
new columns instead of a column of lists.
**Example**:
```python
df[["a", "b"]] = df["text"].str.split(",", expand=True)
```
**Related**: `.str.extract()`

### `.str.extract()`
**Definition**: Applies a regex with named groups and returns the first match
per cell as columns.
**Example**:
```python
df["code"].str.extract(r"(?P<p>[A-Z]+)-(?P<n>\d+)")
```
**Related**: `.str.extractall()`

### `.str.extractall()`
**Definition**: Returns EVERY match per cell as rows under a MultiIndex —
for multiple mentions per record.
**Related**: `.str.extract()`

### `.str.replace()`
**Definition**: Vectorized replacement, regex or literal; the core of cleaning
and redaction pipelines.
**Example**:
```python
s.str.replace(r"\s+", " ", regex=True)
```
**Related**: `regex=`

### `.str.zfill()`
**Definition**: Zero-pads strings to a width — normalizing IDs.
**Example**:
```python
s.str.zfill(8)
```
**Related**: padding

### vectorized
**Definition**: Operations over the whole column in a compiled loop rather
than per-cell Python — orders of magnitude faster.
**Related**: `.str` accessor

### `astype("string")`
**Definition**: Casts to pandas' true `string` dtype (vs `object`), giving
proper string semantics and `pd.NA`.
**Related**: string dtype, `object` dtype

## Key Concepts Summary

### The accessor contract
- `.str` = vectorized string ops; NaN propagates
- `regex=` and `na=` are always explicit decisions

### The toolkit
- Clean: lower/strip/replace
- Test: contains/startswith/endswith
- Structure: split(expand=True)/extract/extractall

### Performance
- Vectorized ops ~100x faster than Python loops on the same logic
- Regex complexity raises per-string cost — simplify patterns at corpus scale

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `.str.contains()` — ___
2. `regex=False` — ___
3. `na=False` — ___
4. `.str.extract()` — ___
5. `.str.extractall()` — ___
6. `.str.split(expand=True)` — ___
7. vectorized — ___
8. `.str.replace()` — ___

A. Literal interpretation, not regex
B. All matches per cell -> MultiIndex
C. Missing treated as non-matching
D. C-speed whole-column operation
E. Membership test for filtering
F. First regex capture -> columns
G. Split into real columns
H. Vectorized cleaning/redaction

**Answers:** 1-E, 2-A, 3-C, 4-F, 5-B, 6-G, 7-D, 8-H
