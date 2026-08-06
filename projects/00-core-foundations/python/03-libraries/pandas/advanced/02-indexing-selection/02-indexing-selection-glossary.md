# Indexing & Selection — Glossary 02 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `.loc` | Accessor | Label-based selection; end label INCLUSIVE |
| `.iloc` | Accessor | Position-based selection; end position EXCLUSIVE |
| boolean mask | Concept | Boolean Series selecting rows where True |
| chained assignment | Bug | `df[mask]["col"] = x` — sets on a copy, silently lost |
| `&` / `\|` / `~` | Operators | Element-wise and / or / not for masks |
| `.isin()` | Method | Set-membership filter |
| `.between()` | Method | Inclusive-by-default range filter |
| `.query()` | Method | String-expression filtering DSL |
| `.copy()` | Method | Explicit detachment of a sub-frame |
| SettingWithCopyWarning | Warning | pandas flagging ambiguous chained mutation |
| label | Concept | Index value identifying a row |
| position | Concept | Integer offset of a row |
| `.at` / `.iat` | Accessors | Fast scalar access by label / position |
| `.xs()` | Method | Cross-section selection on MultiIndex |

## Detailed Definitions

### `.loc`
**Definition**: Label-based row (and column) accessor. Slices are inclusive of
the end label — the opposite of Python's half-open convention.
**Example**:
```python
df.loc["r1":"r3"]     # includes label 'r3'
```
**Complexity**: O(1) average (index hash lookup).
**Related**: `.iloc`, label

### `.iloc`
**Definition**: Position-based accessor; slicing is half-open like lists.
**Example**:
```python
df.iloc[1:3]     # positions 1, 2 only
```
**Complexity**: O(1).
**Related**: `.loc`, position

### boolean mask
**Definition**: A boolean Series aligned to the index; `df[mask]` returns the
rows where the mask is True.
**Example**:
```python
df[df["score"] > 0.7]
```
**Complexity**: O(n) vectorized.
**Related**: `&`, `|`, `~`

### chained assignment
**Definition**: Selecting then assigning in two steps; the first step returns
a copy, so the assignment is silently lost (or warns).
**Example**:
```python
# WRONG
df[df.a > 1]["flag"] = 1
```
**Related**: `SettingWithCopyWarning`, `.loc` setting

### `&` / `|` / `~`
**Definition**: Element-wise boolean operators for masks. Not `and`/`or`
(those require Python booleans and raise on Series).
**Example**:
```python
df[(df.a > 1) & (df.b < 2)]
```
**Related**: boolean mask

### `.isin()`
**Definition**: Filters rows whose value is in a given set — the pandas
spelling of `value in set`.
**Example**:
```python
df[df["doc"].isin(["a", "c"])]
```
**Complexity**: O(n) average.
**Related**: set membership

### `.between()`
**Definition**: Range filter on a Series; `inclusive=` controls the bounds
(default both).
**Example**:
```python
df[df["score"].between(0.4, 0.9)]
```
**Related**: boolean mask

### `.query()`
**Definition**: Selects rows using a string expression — readable compound
filters without mask parens.
**Example**:
```python
df.query("score > 0.7 and doc != 'b'")
```
**Complexity**: O(n).
**Related**: boolean mask

### `.copy()`
**Definition**: Returns a detached copy; mutating it never affects the
original. The fix for the chained-assignment class of bugs.
**Related**: chained assignment

### SettingWithCopyWarning
**Definition**: pandas' warning that an operation may be acting on a copy —
a signal to restructure into a single `.loc` statement or `.copy()`.
**Related**: chained assignment

### label
**Definition**: The index value that names a row; the key for `.loc`.
**Related**: `.loc`, `.at`

### position
**Definition**: The integer offset of a row; the key for `.iloc`.
**Related**: `.iloc`, `.iat`

### `.at` / `.iat`
**Definition**: Fast scalar accessors (single value) by label/position —
faster than `.loc`/`.iloc` for one cell.
**Example**:
```python
df.at["r1", "score"] = 1.0
```
**Related**: `.loc`, `.iloc`

### `.xs()`
**Definition**: Cross-section selection on a MultiIndex — pulls a whole level
slice without re-indexing.
**Related**: MultiIndex (topic 18)

## Key Concepts Summary

### The selector families
- `.loc` — labels, inclusive
- `.iloc` — positions, exclusive
- `df[bool_series]` — masks, the workhorse

### The mask rules
- `&`/`|`/`~`, never `and`/`or`
- Parentheses around each comparison
- `.isin`, `.between`, `.query` for readable compound filters

### Mutation discipline
- One `.loc` statement for set-by-mask
- `.copy()` before detaching and mutating
- Chained assignment is the classic silent-data-loss bug

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `.loc` — ___
2. `.iloc` — ___
3. boolean mask — ___
4. chained assignment — ___
5. `.isin()` — ___
6. `.query()` — ___
7. `.copy()` — ___
8. `&` — ___

A. Element-wise and for masks
B. Label-based, inclusive selection
C. Sets on a copy — silent data loss
D. Position-based, exclusive selection
E. Detached frame safe to mutate
F. String-expression filter DSL
G. Set-membership filter
H. Rows where a boolean Series is True

**Answers:** 1-B, 2-D, 3-H, 4-C, 5-G, 6-F, 7-E, 8-A
