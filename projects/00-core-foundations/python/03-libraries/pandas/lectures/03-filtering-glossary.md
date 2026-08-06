# Filtering — Glossary 03 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| boolean mask | Concept | Boolean Series keeping rows where True |
| compound mask | Concept | Multiple conditions combined with `&`/`\|`/`~` |
| `.query()` | Method | String-expression filtering DSL |
| `@variable` | Syntax | References a Python variable inside `.query()` |
| `.isin()` | Method | Set-membership filter |
| `.between()` | Method | Range filter with `inclusive=` bounds |
| `.str.contains()` | Method | Vectorized regex/literal substring test |
| `.str.startswith()` | Method | Vectorized prefix filter |
| `.filter()` | Method | Select columns/rows BY NAME (items/like/regex) |
| `drop_duplicates()` | Method | Remove duplicate rows with keep rules |
| `keep=False` | Option | Drop ALL rows with a duplicated key |
| `regex=False` | Option | Treat the `.str.contains` pattern literally |
| subset | Argument | Columns considered when deduplicating |
| `&` / `\|` / `~` | Operators | Element-wise and / or / not for masks |

## Detailed Definitions

### boolean mask
**Definition**: A boolean Series aligned with the index; `df[mask]` returns
rows where the mask is True.
**Example**:
```python
df[df["score"] > 0.5]
```
**Complexity**: O(n) vectorized.
**Related**: compound mask, `.query()`

### compound mask
**Definition**: Two or more conditions combined element-wise; every comparison
must be parenthesized because `&` binds tighter than `>`.
**Example**:
```python
df[(df.a > 1) & (df.b < 2)]
```
**Related**: `&`, `|`, `~`

### `.query()`
**Definition**: Filters using a string condition supporting `and`, `or`,
`not`, `in`, and `@var` references — readable SQL-like chains.
**Example**:
```python
df.query("score > 0.5 and split in ['val', 'test']")
```
**Complexity**: O(n).
**Related**: boolean mask

### `@variable`
**Definition**: Inside `.query()`, `@name` injects the Python variable `name`
into the expression.
**Example**:
```python
t = 0.6
df.query("score > @t")
```
**Related**: `.query()`

### `.isin()`
**Definition**: Membership filter against a set/list — pandas' `in` for
Series.
**Example**:
```python
df[df["doc"].isin(["a", "c"])]
```
**Complexity**: O(n) average.
**Related**: set membership

### `.between()`
**Definition**: Range test with `inclusive="both"/"left"/"right"/"neither"`.
**Example**:
```python
df[df["score"].between(0.4, 0.8)]
```
**Related**: range filter

### `.str.contains()`
**Definition**: Vectorized test whether each string matches a regex (default)
or a literal (`regex=False`).
**Example**:
```python
df[df["doc"].str.contains("spam", regex=False)]
```
**Complexity**: O(n x len) per string.
**Related**: `.str.startswith()`

### `.str.startswith()`
**Definition**: Vectorized prefix test — the cheap string filter.
**Related**: `.str.contains()`

### `.filter()`
**Definition**: Selects columns (or index labels) by NAME: `items=`,
`like=` (substring), or `regex=`. Not a value filter.
**Example**:
```python
df.filter(regex="^score")
```
**Related**: name-based selection

### `drop_duplicates()`
**Definition**: Removes duplicate rows considering `subset` columns; `keep`
chooses first/last/None.
**Example**:
```python
df.drop_duplicates(subset=["doc"], keep=False)
```
**Complexity**: O(n) hashing.
**Related**: `keep=False`

### `keep=False`
**Definition**: `drop_duplicates` option removing EVERY row whose key is
duplicated — only singletons remain; for suspicious duplicates.
**Related**: `drop_duplicates()`

### `regex=False`
**Definition**: Makes `.str.contains` treat the pattern as a literal
substring instead of a regular expression.
**Related**: `.str.contains()`

### subset
**Definition**: The column list that defines "duplicate" for
`drop_duplicates`; omit to consider all columns.
**Related**: `drop_duplicates()`

### `&` / `|` / `~`
**Definition**: Element-wise boolean operators on Series; the only way to
combine masks (`and`/`or` raise on Series).
**Related**: compound mask

## Key Concepts Summary

### The grammar
- `&`/`|`/`~` element-wise; parenthesize every comparison
- `.query()` for readable multi-condition strings
- `.isin`/`.between` for membership and ranges

### Value vs name filtering
- Value filters: masks, `.query`, `.str.*`
- Name filters: `.filter(items/like/regex)`
- They solve different problems; do not conflate

### Dedup discipline
- `keep="first"/"last"` — benign duplicates
- `keep=False` — remove every duplicated row (suspect data)

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `.query()` — ___
2. `@threshold` — ___
3. `.isin()` — ___
4. `.between()` — ___
5. `.filter(like=...)` — ___
6. `keep=False` — ___
7. `regex=False` — ___
8. compound mask — ___

A. Literal substring search
B. Python variable inside query
C. String-condition filter DSL
D. Set-membership filter
E. Name-based (substring) column selection
F. Range filter
G. Drop every row with a duplicated key
H. `&`/`|`-combined conditions

**Answers:** 1-C, 2-B, 3-D, 4-F, 5-E, 6-G, 7-A, 8-H
