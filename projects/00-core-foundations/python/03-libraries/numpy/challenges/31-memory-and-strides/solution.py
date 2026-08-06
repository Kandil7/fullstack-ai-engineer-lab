"""
Challenge 31: Memory Contracts — Reference
============================================
Why these implementations:
- column_view: a plain slice is the zero-copy way to reach one
  column; NumPy keeps the shared buffer, so writes propagate.
- ensure_contiguous: np.ascontiguousarray IS the contract --
  identity for C input, one copy otherwise. Never hand-roll a
  contiguity check when the standard library function exists.
- downcast_when_safe: guard the dtype FIRST. Returning X itself
  on the float32 path is the entire point -- astype would
  silently duplicate 20 MB that the serving process already owns.
"""

from __future__ import annotations

import numpy as np


def column_view(X: np.ndarray, j: int) -> np.ndarray:
    """Return a VIEW of column j -- no copy, shared buffer.

    X[:, j] is a basic slice: shape (n,), stride = itemsize of a
    row -- expressible as (slice, int), so NumPy returns a view
    instead of a copy. That is the whole trick.
    """
    return X[:, j]


def ensure_contiguous(x: np.ndarray) -> np.ndarray:
    """Return C-contiguous data: same object when already so,
    otherwise a C-contiguous copy of the same values.

    np.ascontiguousarray checks flags.c_contiguous internally:
    identity fast path, copy slow path. Reimplementing that check
    by hand invites layout bugs (transposes, F order, strided
    views); the ufunc-level function covers all of them.
    """
    return np.ascontiguousarray(x)


def downcast_when_safe(X: np.ndarray) -> np.ndarray:
    """Return float32 data with zero copying when X is already
    float32, and a single float32 cast otherwise.

    The dtype guard must come before any conversion: astype on
    float32 input would allocate a full duplicate for nothing.
    One astype call, one copy -- nothing else.
    """
    if X.dtype == np.float32:
        return X
    return X.astype(np.float32)
