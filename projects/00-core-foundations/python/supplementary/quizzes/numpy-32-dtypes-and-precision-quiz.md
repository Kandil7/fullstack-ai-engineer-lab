# NumPy 32 — Dtypes and Precision Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1 (code-output).** What prints?
```python
import numpy as np
x = np.array([0.1, 0.2, 0.3])
print(x.dtype)
print(x.itemsize)
```

- A) `float64`, `8`
- B) `float32`, `4`
- C) `float64`, `64`
- D) `float16`, `2`

**E2 (code-output).** What prints?
```python
import numpy as np
x = np.array([1.9, -2.7])
print(x.astype(np.int64, casting="unsafe"))
```

- A) `[1 2]`
- B) `[1 -2]`
- C) `[2 -3]`
- D) raises `TypeError`

**E3.** Which dtype holds about 16 significant decimal digits?

- A) `float16`
- B) `float32`
- C) `float64`
- D) `int64`

**E4 (code-output).** What prints?
```python
import numpy as np
print(np.isclose(0.1 + 0.2, 0.3))
print(0.1 + 0.2 == 0.3)
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `True`
- D) `False`, `False`

**E5.** What does `np.uint8(255) + np.uint8(1)` evaluate to?

- A) `256`
- B) raises `OverflowError`
- C) `0`
- D) `255`

**E6 (code-output).** What prints?
```python
import numpy as np
x = np.array([1.0, np.nan, 3.0])
print(x.sum())
print(np.nan != np.nan)
```

- A) `4.0`, `False`
- B) `nan`, `False`
- C) `4.0`, `True`
- D) `nan`, `True`

---

## Medium

**M1 (code-output).** What prints? (NumPy 2.x)
```python
import numpy as np
i = np.arange(3, dtype=np.int64)
f = np.arange(3, dtype=np.float32)
print((i + f).dtype)
print((i + 1).dtype)
```

- A) `float32`, `int64`
- B) `float64`, `int64`
- C) `float64`, `float64`
- D) `float32`, `float32`

**M2 (code-output).** What prints?
```python
import numpy as np
x = np.array([1.0, np.nan, np.inf, -np.inf, 2.0])
bad = ~np.isfinite(x)
print(bad.sum())
x[bad] = 0.0
print(x)
```

- A) `3`, `[1. 0. 0. 0. 2.]`
- B) `4`, `[1. 0. 0. 0. 2.]`
- C) `3`, `[1. 0. inf 0. 2.]`
- D) `2`, `[1. 0. inf -inf 2.]`

**M3.** Which memory figure is correct for a `(1024, 1024)` float32 array?

- A) 2 MB
- B) 4 MB
- C) 8 MB
- D) 16 MB

**M4 (code-output).** What prints?
```python
import numpy as np
with np.errstate(over="ignore"):
    big = np.float64(1e308) * 10.0
print(np.isinf(big))
print(np.inf - np.inf)
```

- A) `True`, `0.0`
- B) `True`, `nan`
- C) `False`, `nan`
- D) `True`, `inf`

**M5.** Why is `x.astype(np.float32)` from a float64 array NOT a "safe" cast in the NumPy casting ladder?

- A) It loses no information; the ladder only applies to ints
- B) `safe` requires exact representability of every value; float32 cannot represent all float64 values
- C) `safe` forbids any change in itemsize
- D) float64→float32 is the `same_kind` step; float32→float64 is `safe`

**M6 (code-output).** What prints?
```python
import numpy as np
rec = np.zeros(2, dtype=[("score", "f4"), ("id", "i4")])
rec["score"] = [0.9, 0.4]
rec["id"] = [7, 3]
print(np.sort(rec, order="score")["id"])
print(rec.nbytes)
```

- A) `[7 3]`, `16`
- B) `[3 7]`, `16`
- C) `[3 7]`, `8`
- D) `[7 3]`, `8`

**M7.** Under NEP 50, which expression's result dtype is `float64`?

- A) `np.arange(3, dtype=np.int64) + 1`
- B) `np.arange(3, dtype=np.float32) + 1`
- C) `np.arange(3, dtype=np.int64) + 0.5`
- D) `np.arange(3, dtype=np.int64).astype(np.float32) + np.float32(1)`

**M8 (code-output).** What prints?
```python
import numpy as np
x = np.array([1.0, np.nan, 3.0, np.nan])
print(np.nanmean(x))
print(np.isnan(x).sum())
```

- A) `2.0`, `2`
- B) `nan`, `2`
- C) `2.0`, `4`
- D) `nan`, `4`

**M9.** A float32 embedding table holds `n` vectors of dimension `d`. About how many bytes does it use?

- A) `n * d`
- B) `n * d * 4`
- C) `n * d * 8`
- D) `n * d * 2`

---

## Hard

**H1 (code-output).** What prints? (NumPy 2.x, NEP 50)
```python
import numpy as np
a = np.arange(3, dtype=np.int64)
b = np.arange(3, dtype=np.float32)
try:
    c = a.astype(np.float32)
    print((b + c).dtype)
except TypeError:
    print("TypeError")
print((a + 0.5).dtype)
```

- A) `float32`, `float64`
- B) `float64`, `float64`
- C) `TypeError`, `float64`
- D) `float32`, `float32`

**H2.** An inference model must be served with weights that have worst-case relative error below 1e-3. Measured float16 error on your weights is 4.9e-4. Which claim is correct?

- A) Casting to float16 is safe for these weights
- B) Casting to float16 is unsafe; you must stay at float64
- C) float16 error is scale-independent, so any weights cast at 4.9e-4
- D) The measurement is wrong — float16 error is always ≤ 1e-5

**H3 (code-output).** What prints?
```python
import numpy as np
w = np.array([127.0, 128.0, 1e10], dtype=np.float32)
h = w.astype(np.float16)
print(h)
```

- A) `[127. 128. 10000000000.]`
- B) `[127. 128. inf]`
- C) `[127. 128. nan]`
- D) `[127. 127. inf]`

**H4.** Your array `x` has dtype float64, contains `nan` values, and is 100 MB. You must compute the per-column mean, ignoring `nan`s, in under 25 MB of additional memory. What is the right move?

- A) `np.nanmean(x, axis=0)` — one mask + one reduction
- B) `np.mean(x[np.isfinite(x)].reshape(-1, x.shape[1]), axis=0)` — wrong, reshape misaligns
- C) `x[np.isnan(x)] = 0.0; x.mean(axis=0)` — fast but biases toward zero
- D) Convert to float16 first, then `np.nanmean` — saves memory with no precision risk

**H5.** Why is `float16` dangerous for cosine similarity over embedding vectors whose components can be as small as 1e-3?

- A) float16 cannot store 1e-3 at all
- B) Relative error is fine, but the cosine formula overflows to `inf`
- C) float16 normal range starts at ~6.1e-5; components near 1e-3 round with relative error up to ~2^-11, but subnormal values near 6.1e-5 and below can carry relative error ≥ 1% — a few such components per vector corrupt rankings
- D) Cosine similarity requires float64 by definition; float16 is not allowed

---

## Answer Key

**E1 — B.** `x` is created from Python floats → `float64`; `itemsize` is 8 bytes.
*Distractors:* A misreads `dtype` as `float32`; C confuses itemsize with total bits (64 bits ≠ 64 bytes); D invents float16 defaults.

**E2 — B.** `unsafe` allows float→int; NumPy truncates toward zero: 1.9→1, -2.7→-2.
*Distractors:* A rounds instead of truncating; C rounds half-away; D describes `casting="safe"`, which rejects this.

**E3 — C.** float64 ≈ 16 digits; float32 ≈ 7; float16 ≈ 3.
*Distractors:* A/B are the reduced-precision dtypes; D stores integers exactly, not significant digits.

**E4 — B.** `isclose` uses tolerance; `==` is bit-exact and 0.1+0.2 ≠ 0.3 in binary.
*Distractors:* A is the classic bug; C/D reverse the two behaviors.

**E5 — C.** uint8 wraps: 255+1 = 0 (mod 256), silently.
*Distractors:* A assumes promotion to a wider int (NEP 50 keeps the array dtype); B expects a Python-style OverflowError; D is `255` unchanged.

**E6 — D.** `nan` poisons `sum`; `nan != nan` is True (nan is not equal to anything).
*Distractors:* A/B assume nan behaves like a value; C assumes sum skips nan (that's `nansum`/`nanmean`).

**M1 — B.** NEP 50: float32 cannot represent all int64 values, so `int64 + float32 → float64`. Python int `1` is weak → stays int64.
*Distractors:* A uses pre-NEP 50 float32 result; C promotes the Python int; D applies float32 to both.

**M2 — A.** `isfinite` flags nan, inf, -inf (3 values); masking + assignment replaces all three with 0.0.
*Distractors:* B miscounts the bad values (thinks 4); C replaces only nan (leaves inf); D only counts nan values (2) and replaces nothing else.

**M3 — B.** 1024×1024 = 2^20 elements × 4 bytes = 4 MB.
*Distractors:* A is float16; C is float64; D doubles again.

**M4 — B.** Overflow → `inf`; `inf - inf` is `nan`.
*Distractors:* A treats inf as a real number; C misreads overflow; D confuses inf arithmetic with nan arithmetic.

**M5 — B.** "safe" means no data loss — every value must be exactly representable. float32 has fewer mantissa bits, so it's only `same_kind`.
*Distractors:* A misunderstands the ladder; C has no basis (itemsize changes are normal); D states the correct definition but labels it as the question's reason.

**M6 — B.** `order="score"` sorts records by field; ids follow scores [0.4, 0.9] → [3, 7]. nbytes = 2 records × (4+4) = 16.
*Distractors:* A ignores the sort; C uses one record's fields only; D combines both mistakes.

**M7 — C.** int64 + Python float 0.5 → float64 (weak scalar promotes to the array's kind-compatible wide type). 
*Distractors:* A stays int64; B: float32 + weak 1 → float32 (weak scalar adopts array dtype); D is float32 (both arrays float32).

**M8 — A.** `nanmean` skips nans: (1+3)/2 = 2.0; isnan counts 2.
*Distractors:* B/D assume nan poisons nanmean; C counts all 4 elements as nan.

**M9 — B.** 4 bytes per element (float32); n·d elements.
*Distractors:* A is the element count; C is float64; D is float16.

**H1 — A.** `a.astype(np.float32)` is explicit, so `b + c` is float32 (both float32). NEP 50 changes *implicit* promotion, not explicit casts. Then `int64 + 0.5 → float64`.
*Distractors:* B ignores the explicit cast; C expects a TypeError that never happens (safe cast exists, float32→float32 is fine); D would require int64+0.5 to stay float32 — impossible.

**H2 — A.** 4.9e-4 < 1e-3, and float16 error is relative — the budget is met. This is the precision-budget decision.
*Distractors:* B ignores the measured number; C is almost right but overclaims (error *is* scale-dependent near subnormals); D is false — float16 rounds at ~5e-4 relative for normal values.

**H3 — B.** float16 max is 65504; 1e10 overflows to `inf`. 127.0 and 128.0 are exactly representable.
*Distractors:* A pretends float16 holds 1e10; C invents nan; D claims 128 loses precision (it doesn't — it's a power of two).

**H4 — A.** `np.nanmean` builds one bool mask (~12.5 MB for 100 MB of float64) plus the reduction output — well under 25 MB of additional memory, and exact. It is the right call under the cap.
*Distractors:* B reshapes a flattened masked array — wrong shape and loses the nan-skip structure; C is the memory-safe shortcut but biases the mean toward zero (zeros are not "missing"); D halves memory but float16 subnormals near zero carry large relative error — unacceptable for means of small values.

**H5 — C.** float16 normals start at ~2^-14 ≈ 6.1e-5. At 1e-3 the relative rounding error is bounded by ~2^-11 ≈ 4.9e-4 — tolerable for ranking, but any component below ~6.1e-5 becomes subnormal, and subnormal relative error grows without bound as values approach zero. A few such components per vector can flip cosine rankings.
*Distractors:* A is false (1e-3 is normal); B is false (no overflow — cosine outputs stay ≤ 1); D is false — cosine is computed in float32/64 from float16 embeddings routinely; the question is precision, not legality.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 32](03-libraries/numpy/lectures/32-dtypes-and-precision-lecture.md) ·
[Glossary 32](03-libraries/numpy/lectures/32-dtypes-and-precision-glossary.md) ·
[Challenge 32](03-libraries/numpy/challenges/32-dtypes-and-precision/README.md)
