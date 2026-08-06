# Dtypes and Precision — Glossary 32

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `astype` | Function | Explicit cast to a new dtype — always a copy |
| `atol` | Parameter | Absolute tolerance in `isclose` for near-zero values |
| Casting ladder | Concept | safe → same_kind → unsafe ordering in `astype` |
| `float16` | Dtype | 2-byte half precision, ~3 significant digits |
| `float32` | Dtype | 4-byte single precision, ~7 significant digits |
| `float64` | Dtype | 8-byte double precision, ~16 significant digits |
| `inf` | Value | Overflow result; behaves like a huge number |
| `isclose` | Function | Tolerance-based float equality (rtol + atol) |
| Itemsize | Attribute | Bytes per element (`float64` = 8) |
| `nan` | Value | Not-a-number; `nan != nan`, poisons reductions |
| `nanmean` | Function | Mean that skips `nan` values |
| NEP 50 | Spec | Python scalars are weak; array dtypes dominate promotion |
| Overflow | Concept | Ints wrap; floats go to `inf` |
| Precision budget | Pattern | Measuring error before downcasting for serving |
| Promotion | Concept | Result dtype of mixed-dtype arithmetic |
| Structured dtype | Dtype | Named typed fields packed into one buffer |
| Wraparound | Concept | Fixed-width ints cycling past their max (255+1→0) |

## Detailed Definitions

### `astype`
**Definition**: Returns a new array cast to `dtype`. Always a copy;
the casting ladder (safe/same_kind/unsafe) governs what is allowed.

**Example**:
```python
import numpy as np

x = np.array([1.9, -2.7])
print(x.astype(np.int64, casting="unsafe"))   # [ 1 -2] truncates
print(x.astype(np.float32).dtype)             # float32
```

**Complexity**: O(n) copy.
**Related**: Casting ladder, Itemsize

---

### `atol`
**Definition**: Absolute tolerance term in `np.isclose`:
`|a - b| <= atol + rtol * |b|`. Necessary near zero, where relative
tolerance is meaningless.

**Example**:
```python
import numpy as np

print(np.isclose(1e-12, 0.0, rtol=1e-5))            # False
print(np.isclose(1e-12, 0.0, rtol=1e-5, atol=1e-12))  # True
```

**Complexity**: O(1) per comparison.
**Related**: `isclose`, `float64`

---

### Casting ladder
**Definition**: The allowed-conversion ordering in `astype`:
`safe` (no data loss), `same_kind` (float64→float32), `unsafe`
(float→int, truncating). Float→int raises with `safe`.

**Example**:
```python
import numpy as np

x = np.array([1.9])
try:
    x.astype(np.int64, casting="safe")
except TypeError:
    print("safe rejected")
print(x.astype(np.int64, casting="unsafe"))       # [1]
```

**Complexity**: O(n) copy when it succeeds.
**Related**: `astype`, Promotion

---

### `float16`
**Definition**: 2-byte half precision: ~3 significant decimal
digits, range to ±65504. The serving/quantization dtype — memory
halves versus float32, error must be budgeted.

**Example**:
```python
import numpy as np

w = np.random.default_rng(0).normal(size=(4, 4))
h = w.astype(np.float16)
print(h.itemsize)                                 # 2
err = np.abs(h.astype(np.float64) - w) / (np.abs(w) + 1e-12)
print(round(float(err.max()), 4))                 # worst-case error
```

**Complexity**: O(n) cast.
**Related**: `float32`, Precision budget

---

### `float32`
**Definition**: 4-byte single precision: ~7 significant digits.
The standard ML storage dtype — half the memory of float64 with
adequate precision for most aggregates.

**Example**:
```python
import numpy as np

f64 = np.random.default_rng(1).normal(size=(500, 500))
f32 = f64.astype(np.float32)
print(f64.nbytes, "->", f32.nbytes)               # 2000000 -> 1000000
print(np.allclose(f32, f64, rtol=1e-5))           # True
```

**Complexity**: O(n) cast.
**Related**: `float64`, `float16`

---

### `float64`
**Definition**: 8-byte double precision: ~16 significant digits.
The NumPy default and the safe choice for conditioning-sensitive
math (solves, inverses, near-cancellation sums).

**Example**:
```python
import numpy as np

x = np.array([0.1, 0.2, 0.3])
print(x.dtype)                                    # float64
print(x.itemsize)                                 # 8
```

**Complexity**: —.
**Related**: `float32`, Itemsize

---

### `inf`
**Definition**: Infinity — the float overflow result. Behaves like
a huge number in arithmetic; `inf - inf` is `nan`.

**Example**:
```python
import numpy as np

with np.errstate(over="ignore"):
    big = np.float64(1e308) * 10.0
print(np.isinf(big))                              # True
print(np.inf - np.inf)                            # nan
```

**Complexity**: —.
**Related**: Overflow, `nan`

---

### `isclose`
**Definition**: Tolerance-based float equality: True when
`|a - b| <= atol + rtol * |b|`. The only correct way to compare
floats; `==` is bit-exact and fails on `0.1 + 0.2`.

**Example**:
```python
import numpy as np

a = 0.1 + 0.2
print(a == 0.3)                                   # False
print(np.isclose(a, 0.3))                         # True
print(np.allclose(np.array([a]), np.array([0.3])))  # True
```

**Complexity**: O(n) for arrays.
**Related**: `atol`, `float64`

---

### Itemsize
**Definition**: Bytes per element fixed by the dtype: 8/4/2 for
float64/32/16, 1 for int8 and bool. Memory = size × itemsize.

**Example**:
```python
import numpy as np

for dt in (np.float64, np.float32, np.float16, np.int8):
    print(dt.__name__, np.zeros(1, dtype=dt).itemsize)
# float64 8
# float32 4
# float16 2
# int8 1
```

**Complexity**: —.
**Related**: `float64`, `nbytes`

---

### `nan`
**Definition**: Not-a-number. Not equal to anything, including
itself; poisons reductions (`sum`, `mean`, `max` return `nan`).
Detect with `np.isnan`.

**Example**:
```python
import numpy as np

x = np.array([1.0, np.nan, 3.0])
print(np.nan != np.nan)                           # True
print(np.isnan(x))                                # [False  True False]
print(x.sum())                                    # nan
```

**Complexity**: —.
**Related**: `nanmean`, `inf`

---

### `nanmean`
**Definition**: Mean that skips `nan` values — one of the `np.nan*`
family (`nansum`, `nanmax`, ...). Use deliberately when missingness
is expected and counted.

**Example**:
```python
import numpy as np

x = np.array([1.0, np.nan, 3.0])
print(np.nanmean(x))                              # 2.0
print(np.isnan(x).sum())                          # 1 -- counted
```

**Complexity**: O(n), builds a mask.
**Related**: `nan`, Masking

---

### NEP 50
**Definition**: NumPy Enhancement Proposal 50 (NumPy 2.0): Python
scalars are "weak" types — array dtypes dominate promotion.
Consequence: `int64 + float32` → `float64` (float32 cannot hold all
int64 values).

**Example**:
```python
import numpy as np

i = np.arange(3, dtype=np.int64)
f = np.arange(3, dtype=np.float32)
print((i + f).dtype)       # float64
print((i + 1).dtype)       # int64 -- python int stays weak
```

**Complexity**: —.
**Related**: Promotion, Casting ladder

---

### Overflow
**Definition**: Value beyond the dtype's range. Integers **wrap**
silently (`uint8 255 + 1 → 0`); floats overflow to `inf` with a
warning.

**Example**:
```python
import numpy as np

with np.errstate(over="ignore"):
    print(int((np.array([255], dtype=np.uint8) + np.uint8(1))[0]))
# 0 -- wrapped
```

**Complexity**: —.
**Related**: Wraparound, `inf`

---

### Precision budget
**Definition**: The practice of measuring downcast error on real
data before adopting a smaller dtype — the float16 serving decision
is made on evidence, not defaults.

**Example**:
```python
import numpy as np

w = np.random.default_rng(2).normal(size=(1024, 1024))
h = w.astype(np.float16)
rel = np.abs(h.astype(np.float64) - w) / (np.abs(w) + 1e-12)
print(round(float(rel.max()), 4))     # worst-case relative error
```

**Complexity**: O(n) measurement.
**Related**: `float16`, `isclose`

---

### Promotion
**Definition**: The dtype of a mixed-dtype operation's result.
Array dtypes dominate weak python scalars (NEP 50); the widest
"kind-compatible" array dtype usually wins.

**Example**:
```python
import numpy as np

i = np.arange(3, dtype=np.int64)
print((i + 0.5).dtype)     # float64
print((i + 1).dtype)       # int64
```

**Complexity**: —.
**Related**: NEP 50, Casting ladder

---

### Structured dtype
**Definition**: A dtype with named, typed fields —
`[("score", "f4"), ("id", "i4")]` — packing a record table into one
buffer. Field access and field-sorted `np.sort` work by name.

**Example**:
```python
import numpy as np

rec = np.zeros(3, dtype=[("score", np.float32), ("id", np.int32)])
rec["score"] = [0.9, 0.4, 0.7]
rec["id"] = [7, 3, 11]
print(np.sort(rec, order="score")["id"])      # [ 3 11  7]
print(rec.nbytes)                             # 24
```

**Complexity**: O(n log n) for `order=` sort.
**Related**: Itemsize, `astype`

---

### Wraparound
**Definition**: Fixed-width integers cycling past their range:
`np.uint8(255) + 1 == 0`. Silent — the classic counter bug.

**Example**:
```python
import numpy as np

c = np.array([127], dtype=np.int8)
print(int((c + np.int8(1))[0]))               # -128 -- wrapped
```

**Complexity**: —.
**Related**: Overflow, `inf`

## Key Concepts Summary

### Sizes and budgets
- float16/32/64 → 2/4/8 bytes; memory = size × itemsize.
- float32 is the ML default; float16 is serving quantization.

### The sharp edges
- Ints wrap; floats overflow to `inf`.
- `nan != nan`; reductions get poisoned.
- `==` on floats is bit-exact; use `isclose`.

### The contracts
- Casting ladder: safe / same_kind / unsafe.
- NEP 50: python scalars are weak in promotion.
- Structured dtypes: named fields, field sorting.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Wraparound — ___
2. `nan` — ___
3. `isclose` — ___
4. Itemsize — ___
5. NEP 50 — ___
6. Precision budget — ___

**Answers:**
1. b, 2. f, 3. a, 4. e, 5. c, 6. d

a. Tolerance-based float equality (rtol + atol)
b. Fixed-width ints cycling past their max
c. Python scalars are weak; array dtypes dominate
d. Measuring downcast error before adopting smaller dtypes
e. Bytes per element, fixed by the dtype
f. Not-a-number; not equal to itself, poisons reductions

---

**Related docs:** [NumPy dtypes](https://numpy.org/doc/stable/reference/arrays.dtypes.html) ·
[`np.isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) ·
[NEP 50 scalar promotion](https://numpy.org/neps/nep-0050-scalar-promotion.html) ·
[Back to lecture](32-dtypes-and-precision-lecture.md)
