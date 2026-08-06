# Method Chaining — Glossary 39 (pandas)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| chain | Concept | One expression of transforms; each call returns the next input |
| `.query()` | Method | SQL-style string filter, `@var` for external values |
| `.assign()` | Method | Adds columns to a NEW frame; callables see intermediate state |
| `.pipe()` | Method | Calls `f(frame)` and returns whatever `f` returns |
| callable | Concept | A lambda/function passed to `.assign` that receives the frame |
| `SettingWithCopyWarning` | Warning | Fires on writes through multiple selections; the write may vanish |
| `.loc` | Accessor | Label-based selection; the single-selection way to write |
| view | Concept | An object sharing memory with its parent (slices, shallow copies) |
| copy (deep) | Concept | Fully independent frame; default of `.copy()` |
| copy (shallow) | Concept | Shares data blocks with the parent; writes propagate |
| `inplace=True` | Anti-pattern | Returns None, cannot chain, saves nothing |
| `@var` | Syntax | `.query()` reference to an enclosing-scope variable |
| `.str.contains`-style vectorization | Concept | C-speed ops that make chains fast |
| mutation | Concept | Changing a frame in place; chains avoid it by returning new frames |
| intermediate frame | Concept | The frame state at a given link in a chain |

## Detailed Definitions

### `.assign()`
**Definition**: Returns a new frame with columns added or overwritten. Values
can be scalars, Series, or callables; callables receive the frame *as it
exists at that point in the chain* — after earlier filters and assigns.
**Example**:
```python
df.assign(total=df["price"] * df["qty"],
          rank=lambda d: d["total"].rank())
```
**Complexity**: O(n) per new column.
**Related**: chain, callable

### `@var`
**Definition**: In `.query()`, prefix a name with `@` to reference a Python
variable from the enclosing scope instead of a column.
**Example**:
```python
min_spend = 100.0
df.query("spend > @min_spend")
```
**Related**: `.query()`

### callable
**Definition**: A function (usually a `lambda d: ...`) passed to `.assign()`
or `.pipe()`. `.assign` calls it with the current frame so the new column
reflects filtered/intermediate state, not the original frame.
**Example**:
```python
df.query("plan == 'free'").assign(rank=lambda d: d["spend"].rank())
```
**Related**: `.assign()`, intermediate frame

### chain
**Definition**: A sequence of method calls where each returns the object the
next consumes. Enforces "every step returns a new frame", which prevents
hidden mutation and makes pipelines read top-to-bottom.
**Related**: intermediate frame, mutation

### copy (deep)
**Definition**: `.copy()` default: a fully independent frame. Mutating it
never affects the original.
**Example**:
```python
safe = df.copy()
safe.iloc[0, 0] = 999   # df untouched
```
**Complexity**: O(n) time and space.
**Related**: copy (shallow), view

### copy (shallow)
**Definition**: `.copy(deep=False)`: shares the underlying data blocks.
Cheap to create, but a write through it propagates to the parent — only
safe for read-only reuse.
**Example**:
```python
tmp = df.copy(deep=False)
tmp.iloc[0, 0] = 999    # df changes too
```
**Related**: copy (deep), view

### `inplace=True`
**Definition**: The parameter on dropna/fillna/sort_values that claims to
avoid copies. It returns None, cannot be used in a chain, and pandas still
allocates internally — an anti-pattern.
**Example**:
```python
# WRONG
df.query("x > 0").dropna(inplace=True).assign(y=1)   # NoneType error
# CORRECT
df.query("x > 0").dropna().assign(y=1)
```
**Related**: chain, mutation

### intermediate frame
**Definition**: The frame produced by one link of a chain and consumed by the
next. `.assign` callables see the intermediate frame; precomputed Series see
the original — the root of the rank-bug.
**Related**: chain, callable

### `.loc`
**Definition**: Label-based row/column selection. The canonical safe write:
one selection, one assignment, no ambiguity, no warning.
**Example**:
```python
df.loc[df["a"] > 1, "flag"] = 1
```
**Related**: `SettingWithCopyWarning`

### mutation
**Definition**: Changing a frame in place. Chains avoid mutation by
returning new frames; mutations through views/copies are where silent data
corruption starts.
**Related**: chain, copy (shallow)

### `.pipe()`
**Definition**: Calls `pipe(f)(frame)` as `f(frame)` and returns `f`'s
result — the way to insert custom (or third-party) functions into a chain.
**Example**:
```python
df.pipe(drop_missing).pipe(flag_high, "spend", 100.0)
```
**Related**: chain, callable

### `.query()`
**Definition**: Filters with a SQL-like string expression; `and`, `or`,
`not` are keywords; `@var` imports enclosing variables; column names are
bare identifiers.
**Example**:
```python
df.query("spend > @min_spend and city == 'SF'")
```
**Complexity**: O(n).
**Related**: `@var`

### `SettingWithCopyWarning`
**Definition**: Emitted when a value is set through a chain of selections
(`df[mask]["col"] = x`, or `sub = df.iloc[:2]; sub["col"] = x`). pandas
cannot prove view-vs-copy, so it warns; the write is often silently lost.
The fix is a single `.loc` selection.
**Example**:
```python
# warning: sub may be a copy; df is unchanged
sub = df[df["a"] > 1]
sub["flag"] = 1
```
**Related**: `.loc`, copy (deep), view

### view
**Definition**: An object that shares memory with its parent — produced by
slicing (`df.iloc[:2]`) and shallow copies. Reads are cheap; writes are
ambiguous and warned about.
**Related**: `SettingWithCopyWarning`, copy (shallow)

## Key Concepts Summary

### The chain contract
- Every link returns a new frame — no hidden mutation
- Read top-to-bottom; each line is one reviewed transform
- `pipe` keeps custom steps named and testable

### The assign trap
- Callables see the intermediate frame
- Precomputed Series rank the ORIGINAL frame — silently wrong after filters
- Rule: when order matters, use a callable

### The write rule
- Never `df[mask]["col"] = x` — warn + vanish
- Always `df.loc[mask, "col"] = x` — one selection, guaranteed

### Copy semantics
- `.copy()` default: deep, independent
- `.copy(deep=False)`: shares blocks, writes propagate
- `inplace=True`: returns None, cannot chain, saves nothing

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `.pipe()` — ___
2. callable — ___
3. `SettingWithCopyWarning` — ___
4. `@var` — ___
5. copy (shallow) — ___
6. intermediate frame — ___
7. `.loc` write — ___
8. `inplace=True` — ___

A. Shares data blocks; writes reach the parent
B. Reference to an outside variable in `.query()`
C. The frame state at one link of a chain
D. Plugs a named function into a chain
E. Fires on multi-selection writes; the value may vanish
F. Function that sees the frame at this point in the chain
G. Returns None and cannot chain
H. The single-selection safe way to write

**Answers:** 1-D, 2-F, 3-E, 4-B, 5-A, 6-C, 7-H, 8-G
