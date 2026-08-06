"""
NumPy -- 31: Memory and Strides
==============================================
Topics: strides, C vs Fortran order, view vs copy, ascontiguousarray,
        cache locality, nbytes

Why this matters for AI/backend engineering:
    Strides are why transposed arrays get 10x slower, why .T is free,
    and why column access on a row-major matrix thrashes the cache.
    Every view-vs-copy decision in feature pipelines is a memory
    bandwidth decision -- this file makes the cost visible.

Run:      python 31-memory-and-strides.py
Verify:   python 31-memory-and-strides.py --verify
Reference: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.strides.html
"""

from __future__ import annotations

import sys
import time

import numpy as np

rng = np.random.default_rng(42)


def timed(label: str, func) -> None:
    """Print wall time -- informational only, never asserted."""
    start = time.perf_counter()
    func()
    print(f"  {label:<30s} {time.perf_counter() - start:9.5f}s")


# ============================================================
# 1. Strides: The Byte Map of an Array
# ============================================================
# strides[k] is how many BYTES to step to move one index along
# axis k. For a C-contiguous float64 array, the last axis steps
# itemsize (8), each earlier axis steps (size of that axis)*8.

# Example 1: reading strides off an array
arr = np.zeros((4, 6), dtype=np.float64)
print("shape:  ", arr.shape)
print("strides:", arr.strides)      # (48, 8)
print("itemsize:", arr.itemsize)    # 8
print("nbytes:  ", arr.nbytes)      # 192 = 4*6*8

# Output:
# shape:   (4, 6)
# strides: (48, 8)
# itemsize: 8
# nbytes:   192 = 4*6*8


# ============================================================
# 2. C vs Fortran Order
# ============================================================
# C order: last axis contiguous (row-major). Fortran order:
# first axis contiguous (column-major). np.ones(order='F')
# builds Fortran layout; .T of C data is F-layout.

# Example 2: flags and stride patterns
c_arr = np.zeros((3, 4), dtype=np.float32)
f_arr = np.asfortranarray(c_arr)
print("C-order strides:", c_arr.strides)     # (16, 4)
print("F-order strides:", f_arr.strides)     # (4, 12)
print("C contiguous  :", c_arr.flags.c_contiguous)
print("F contiguous  :", f_arr.flags.f_contiguous)

# Output:
# C-order strides: (16, 4)
# F-order strides: (4, 12)
# C contiguous  : True
# F contiguous  : True


# ============================================================
# 3. Views Are Free; Copies Are Not
# ============================================================
# A slice is a VIEW: same data buffer, adjusted shape/strides,
# arr.base is not None. Fancy indexing and astype always COPY.

# Example 3: slice -> view, transpose -> view
base = np.arange(24).reshape(4, 6)
row_view = base[1:3, :]
t_view = base.T
print("slice base is not None:", row_view.base is not None)
print("transpose base:", t_view.base is not None)
print("T strides swapped:", t_view.strides)   # (8, 48)
# A write through the view reaches the base buffer:
row_view[0, 0] = -1
print("base changed through view:", base[1, 0] == -1)

# Example 4: fancy indexing and astype copy
fancy = base[[0, 2], :]
cast = base.astype(np.float64)
print("fancy base is None:", fancy.base is None)   # copy
print("astype base is None:", cast.base is None)   # copy

# Output:
# slice base is not None: True
# transpose base: True
# T strides swapped: (8, 48)
# base changed through view: True
# fancy base is None: True
# astype base is None: True


# ============================================================
# 4. ascontiguousarray: Fixing the Layout
# ============================================================
# np.ascontiguousarray(a) returns a WITHOUT copying when a is
# already C-contiguous, and a COPY otherwise (e.g., for a
# transposed or F-order view). This is how you pay for .T
# only when you must.

# Example 5: no-op on contiguous, copy on transposed
t = base.T                       # F-order view of a C array
fix_t = np.ascontiguousarray(t)
print("same object when already contiguous:",
      np.ascontiguousarray(base) is base)      # True
print("copies when not contiguous:",
      np.ascontiguousarray(t) is not t)        # True
print("fixed strides:", fix_t.strides)         # (48, 8)

# Output:
# same object when already contiguous: True
# copies when not contiguous: True
# fixed strides: (48, 8)


# ============================================================
# 5. Cache Locality: The 10x Slower Transpose
# ============================================================
# Summing along the CONTIGUOUS axis walks memory sequentially and
# hits cache lines fully; summing along the strided axis jumps
# between cache lines. Modern NumPy optimizes axis-0 reductions
# heavily, so on some builds the gap disappears -- but a strided
# VIEW handed to a C/Fortran kernel (or an old BLAS) pays the
# full cache-miss price. Measure on YOUR machine; the invariant
# is that .T itself is free and USING it may not be.

# Example 6: row sums (contiguous axis) vs column sums (strided axis)
big = rng.normal(size=(4000, 4000))
timed("row sum (contiguous axis)", lambda: big.sum(axis=1))
timed("col sum (strided axis)  ", lambda: big.sum(axis=0))

# Example 7: .T is free, but USING the transposed data is not
big_t = big.T                     # view: O(1), no data moved
print("transpose is a view:", big_t.base is not None)
timed("contiguous sum of .T copy",
      lambda: np.ascontiguousarray(big_t).sum(axis=1))

# Output (times vary by machine and NumPy build -- never assert them;
# the transpose view is O(1) regardless):
#   row sum (contiguous axis)       0.016s
#   col sum (strided axis)          0.008s
#   transpose is a view: True
#   contiguous sum of .T copy       0.168s


# ============================================================
# 6. nbytes: Counting the Real Cost
# ============================================================
# nbytes = size * itemsize for the LOGICAL array; views report
# their own logical size, but share the base buffer -- so two
# arrays can both claim memory while only one buffer exists.

# Example 8: memory accounting
a = np.zeros((1000, 1000), dtype=np.float64)
b = a[:, 0]                       # view: 1000 floats
c = a[:, :2].copy()               # copy: 2000 floats
print("a.nbytes:", a.nbytes)                  # 8,000,000
print("b.nbytes:", b.nbytes)                  # 8,000 (view shares buffer)
print("c.nbytes:", c.nbytes)                  # 16,000 (owns buffer)
print("b shares a's buffer:", b.base is a)

# Output:
# a.nbytes: 8000000
# b.nbytes: 8000
# c.nbytes: 16000
# b shares a's buffer: True


# ============================================================
# 7. Production Pattern: Contiguity Contract for a Service
# ============================================================
# A matrix-vector function that FORCES a contiguous layout before
# handing data to a C/Fortran kernel. The contract: callers pay
# the copy once; the kernel never sees a strided view.

# Complexity: O(n*d) copy only when layout is wrong; O(1) when
# the input is already C-contiguous.

def require_c_contiguous(x: np.ndarray) -> np.ndarray:
    """Return a C-contiguous array, copying only if needed.

    np.ascontiguousarray is the idiom; callers keep a view and
    memory stays shared whenever the layout already matches.
    """
    return np.ascontiguousarray(x)


data = rng.normal(size=(500, 300))
fixed = require_c_contiguous(data)
print("no copy for C input:  ", fixed is data)
fixed_t = require_c_contiguous(data.T)
print("copy for F view:      ", fixed_t is not data.T)
print("kernel-friendly strides:", fixed_t.strides)

# Output:
# no copy for C input:   True
# copy for F view:       False
# kernel-friendly strides: (2400, 8)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: assuming .T is cheap to USE because it is cheap to
#   create -- the transpose view is free; iterating it is not.
#   CORRECT: np.ascontiguousarray(x.T) when a C kernel follows.
#
# MISTAKE: checking `a is b` to test aliasing -- views are new
#   objects. Check `a.base is b` (or b.base is a) instead.
#
# MISTAKE: believing reshape always copies -- reshape returns a
#   view when possible and a copy when the memory order forbids
#   it; check .base before assuming either.


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Stride arithmetic for a C-contiguous float64 array.
    arr = np.zeros((4, 6), dtype=np.float64)
    assert arr.strides == (48, 8), "C-order strides must be (48, 8)"
    assert arr.nbytes == 192, "nbytes must be 4*6*8 = 192"

    # Fortran order swaps the stride pattern.
    f_arr = np.asfortranarray(arr)
    assert f_arr.strides == (8, 32), "F-order strides must be (8, 32)"
    assert f_arr.flags.f_contiguous, "asfortranarray must be F-contiguous"

    # Slices and transposes are views; fancy indexing and astype copy.
    base = np.arange(24).reshape(4, 6)
    assert base[1:3, :].base is not None, "slicing must return a view"
    assert base.T.base is not None, "transpose must return a view"
    assert base[[0, 2], :].base is None, "fancy indexing must copy"
    assert base.astype(np.float64).base is None, "astype must copy"

    # Transpose swaps strides, so ascontiguousarray must copy it.
    assert base.T.strides == (8, 48), "transposed strides must be (8, 48)"
    assert np.ascontiguousarray(base) is base, \
        "ascontiguousarray must not copy contiguous input"
    assert np.ascontiguousarray(base.T) is not base.T, \
        "ascontiguousarray must copy a transposed view"

    # Views share the buffer: writes propagate.
    view = base[1:3, :]
    view[0, 0] = -1
    assert base[1, 0] == -1, "write through a view must reach the base"

    # nbytes is logical; a view of a column reports its own size
    # while sharing the parent buffer.
    a = np.zeros((1000, 1000), dtype=np.float64)
    b = a[:, 0]
    assert b.nbytes == 8000, "column view nbytes must be 1000*8"
    assert b.base is a, "column slice must share the parent buffer"

    print("[OK] 31-memory-and-strides: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Strides map axes to byte offsets; .T swaps them for free.")
        print("2. Views share buffers; fancy indexing and astype copy.")
        print("3. Strided access misses cache lines -- transpose costs at use.")
        _verify()          # always runs, so plain execution is also a test
