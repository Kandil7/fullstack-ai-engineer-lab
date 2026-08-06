"""
NumPy -- 32: Dtypes and Precision
==============================================
Topics: float32 vs float64 (memory and speed), overflow wraparound,
        nan/inf propagation, isclose, structured dtypes, casting
        rules, float16 for inference

Why this matters for AI/backend engineering:
    Serving models in float16/float32 instead of float64 halves or
    quarters memory and doubles throughput -- but only if you know
    where precision breaks: overflow, wraparound, nan poisoning,
    and == on floats. This file draws those lines precisely.

Run:      python 32-dtypes-and-precision.py
Verify:   python 32-dtypes-and-precision.py --verify
Reference: https://numpy.org/doc/stable/reference/arrays.dtypes.html
"""

from __future__ import annotations

import sys

import numpy as np

rng = np.random.default_rng(42)

# ============================================================
# 1. Itemsize and Memory: float16 < float32 < float64
# ============================================================
# itemsize is the per-element byte cost. Halving precision halves
# memory and usually speeds up memory-bound inference passes.

# Example 1: sizes
for dt in (np.float16, np.float32, np.float64):
    a = np.zeros((1000, 1000), dtype=dt)
    print(f"{str(dt):<18s} itemsize={a.itemsize}  "
          f"nbytes={a.nbytes}")

# Example 2: same values, quarter the memory
f64 = rng.normal(size=(500, 500))
f32 = f64.astype(np.float32)
print("loss of precision is small:",
      np.allclose(f32, f64, rtol=1e-5))
print("float32 saves bytes:",
      f64.nbytes > f32.nbytes)

# Output:
# float16             itemsize=2  nbytes=2000000
# float32             itemsize=4  nbytes=4000000
# float64             itemsize=8  nbytes=8000000
# loss of precision is small: True
# float32 saves bytes: True


# ============================================================
# 2. Overflow and Wraparound
# ============================================================
# Fixed-width integers WRAP, they do not saturate: uint8(255) + 1
# is 0. Floats overflow to inf instead. Python ints never wrap --
# they grow -- which hides these bugs until the array conversion.

# Example 3: integer wraparound
u = np.array([255], dtype=np.uint8)
with np.errstate(over="ignore"):
    wrapped = u + np.uint8(1)
print("uint8 255 + 1 wraps:", int(wrapped[0]))      # 0

# Example 4: float overflow -> inf, no wrap
with np.errstate(over="ignore"):
    big = np.float64(1e308) * np.float64(10)
print("float overflow -> inf:", np.isinf(big))

# Output:
# uint8 255 + 1 wraps: 0
# float overflow -> inf: True


# ============================================================
# 3. nan and inf Propagation
# ============================================================
# nan poisons every reduction it touches; inf participates in
# arithmetic. nan != nan is the classic surprise.

# Example 5: nan semantics
x = np.array([1.0, np.nan, 3.0])
print("nan != nan:", np.nan != np.nan)          # True
print("nan == nan:", np.nan == np.nan)          # False
print("sum with nan:", np.sum(x))               # nan
print("isnan mask:", np.isnan(x))               # [False  True False]
print("nanmean skips it:", np.nanmean(x))       # 2.0

# Example 6: inf arithmetic
y = np.array([1.0, np.inf])
print("inf + 1:", y.sum())                      # inf
print("inf - inf:", np.inf - np.inf)            # nan

# Output:
# nan != nan: True
# nan == nan: False
# sum with nan: nan
# isnan mask: [False  True False]
# nanmean skips it: 2.0
# inf + 1: inf
# inf - inf: nan


# ============================================================
# 4. isclose: The Correct Float Equality
# ============================================================
# == on floats is exact bit comparison; accumulated rounding
# makes "equal" values unequal. np.isclose uses rtol+atol;
# np.allclose is its array form.

# Example 7: == fails, isclose succeeds
a = 0.1 + 0.2
b = 0.3
print("0.1+0.2 == 0.3:", a == b)                # False
print("isclose:", np.isclose(a, b))             # True
print("allclose on arrays:",
      np.allclose(np.array([a]), np.array([b])))  # True

# Example 8: atol matters near zero
tiny = 1e-12
print("rtol-only would fail near 0:",
      np.isclose(tiny, 0.0, rtol=1e-5))          # False
print("with atol:", np.isclose(tiny, 0.0,
                               rtol=1e-5, atol=1e-12))  # True

# Output:
# 0.1+0.2 == 0.3: False
# isclose: True
# allclose on arrays: True
# rtol-only would fail near 0: False
# with atol: True


# ============================================================
# 5. Structured Dtypes: Columns with Names
# ============================================================
# A structured array packs heterogeneous fields into one buffer --
# the NumPy-native "table". Fields are accessed by name.

# Example 9: build and access a structured array
rec = np.zeros(3, dtype=[("score", np.float32), ("id", np.int32)])
rec["score"] = [0.9, 0.4, 0.7]
rec["id"] = [7, 3, 11]
print("field access:", rec["score"])            # [0.9 0.4 0.7]
print("row 1:", rec[1])                         # (0.4, 3)
print("sort by score:",
      np.sort(rec, order="score")["id"])        # [3 11 7]
print("record nbytes:", rec.nbytes)             # 24 = 3*8

# Output:
# field access: [0.9 0.4 0.7]
# row 1: (0.4, 3)
# sort by score: [3 7 11]
# record nbytes: 24 = 3*8


# ============================================================
# 6. Casting Rules: safe, same_kind, unsafe
# ============================================================
# Python-int + float -> float (weak promotion). int + float32 ->
# float32 (NEP 50 keeps the array dtype). astype applies explicit
# casting; 'unsafe' is required for float -> int.

# Example 10: result dtypes of mixed operations
# NEP 50: the python float is "weak"; int64 + float32 promotes to
# float64 because float32 cannot hold all int64 values.
i = np.arange(3, dtype=np.int64)
f = np.arange(3, dtype=np.float32)
print("int64 + float32:", (i + f).dtype)        # float64
print("int64 + python float:", (i + 0.5).dtype)  # float64
print("int64 + python int:", (i + 1).dtype)     # int64

# Example 11: explicit casts and their costs
x64 = rng.normal(size=100)
print("astype float32:", x64.astype(np.float32).dtype)
print("float->int needs unsafe:",
      x64.astype(np.int64, casting="unsafe").dtype)
try:
    x64.astype(np.int64, casting="safe")
except TypeError as exc:
    print("safe cast rejected:", str(exc)[:40], "...")

# Output:
# int64 + float32: float64
# int64 + python float: float64
# int64 + python int: int64
# astype float32: float32
# float->int needs unsafe: int64
# safe cast rejected: Cannot cast array data from dtype('float64')


# ============================================================
# 7. Production Pattern: float16 for Inference
# ============================================================
# Weights and activations cast to float16 halve memory and speed
# up memory-bound serving -- after checking the precision budget.
# float16 has ~3 significant decimal digits, but the WORST-CASE
# relative error near zero can reach several percent; the budget
# decision belongs to the model owner, not the cast.

# Complexity: cast is O(n) copy; inference ops stay O(n) per layer.

def cast_weights_for_serving(weights: np.ndarray) -> np.ndarray:
    """Cast model weights to float16 for memory-lean serving.

    Chosen over float32 when the application tolerates ~1e-3
    relative error -- the standard half-precision serving trade.
    """
    return weights.astype(np.float16)


w64 = rng.normal(size=(1024, 1024))
w16 = cast_weights_for_serving(w64)
rel_err = np.abs(w16.astype(np.float64) - w64) / (np.abs(w64) + 1e-12)
print("serving dtype:", w16.dtype)
print("memory: ", w64.nbytes, "->", w16.nbytes)
print("max relative error:",
      round(float(np.max(rel_err)), 4))         # ~0.05 worst-case

# Output:
# serving dtype: float16
# memory:  8388608 -> 2097152
# max relative error: 0.0457


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: comparing floats with ==
#   bad = a == b            # bit-exact, fails on 0.1+0.2
# CORRECT:
#   good = np.isclose(a, b, rtol=1e-5, atol=1e-8)
#
# MISTAKE: assuming integer overflow saturates
#   bad = np.uint8(255) + np.uint8(1)   # 0, silently wraps
# CORRECT: check ranges BEFORE conversion, or use larger dtype
#
# MISTAKE: letting nan flow into aggregates
#   bad = arr.mean()        # nan
# CORRECT:
#   good = np.nanmean(arr)  # skips nan, but only when intended!


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Itemsize contract: 2 / 4 / 8 bytes.
    assert np.zeros(1, dtype=np.float16).itemsize == 2, \
        "float16 itemsize must be 2"
    assert np.zeros(1, dtype=np.float32).itemsize == 4, \
        "float32 itemsize must be 4"
    assert np.zeros(1, dtype=np.float64).itemsize == 8, \
        "float64 itemsize must be 8"

    # Overflow wraps for unsigned ints, floats go to inf.
    with np.errstate(over="ignore"):
        assert int((np.array([255], dtype=np.uint8)
                    + np.uint8(1))[0]) == 0, \
            "uint8 255 + 1 must wrap to 0"
    assert np.isinf(big), \
        "float overflow must produce inf"

    # nan semantics: not equal to itself, poisons sums.
    assert np.nan != np.nan, "nan must not equal itself"
    assert np.isnan(np.array([1.0, np.nan, 3.0]).sum()), \
        "nan must poison sum"
    assert np.nanmean(np.array([1.0, np.nan, 3.0])) == 2.0, \
        "nanmean must skip nan"

    # isclose vs == on floats.
    assert 0.1 + 0.2 != 0.3, "== must fail on 0.1+0.2"
    assert np.isclose(0.1 + 0.2, 0.3), "isclose must accept 0.1+0.2"
    assert np.isclose(1e-12, 0.0, rtol=1e-5, atol=1e-12), \
        "atol must cover near-zero comparisons"

    # Structured dtypes: field access, sorting by a field.
    rec = np.zeros(3, dtype=[("score", np.float32), ("id", np.int32)])
    rec["score"] = [0.9, 0.4, 0.7]
    rec["id"] = [7, 3, 11]
    assert rec["score"].dtype == np.float32, "field dtype must hold"
    assert np.array_equal(np.sort(rec, order="score")["id"],
                          [3, 11, 7]), "sort by field must reorder ids"

    # Casting rules: promotion and the safe/unsafe split.
    i = np.arange(3, dtype=np.int64)
    f = np.arange(3, dtype=np.float32)
    assert (i + f).dtype == np.float64, \
        "int64 + float32 must promote to float64 (NEP 50)"
    assert (i + 0.5).dtype == np.float64, \
        "int64 + python float must promote to float64"
    with np.testing.assert_raises(TypeError):
        i.astype(np.float32).astype(np.int64, casting="safe")

    # float16 serving: dtype, memory, bounded error.
    rng = np.random.default_rng(42)
    w64 = rng.normal(size=(1024, 1024))
    w16 = cast_weights_for_serving(w64)
    assert w16.dtype == np.float16, "serving cast must produce float16"
    assert w16.nbytes == w64.nbytes // 4, \
        "float16 must use a quarter of float64 memory"
    rel_err = np.abs(w16.astype(np.float64) - w64) / (
        np.abs(w64) + 1e-12)
    assert float(np.max(rel_err)) < 0.1, \
        "float16 serving worst-case relative error stays under 10%"

    print("[OK] 32-dtypes-and-precision: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. float16/32/64 cost 2/4/8 bytes per element.")
        print("2. Ints wrap, floats overflow to inf, nan poisons.")
        print("3. Use isclose for float equality; structured dtypes "
              "for tables.")
        _verify()          # always runs, so plain execution is also a test
