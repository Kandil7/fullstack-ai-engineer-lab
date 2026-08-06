"""Challenge 32: Dtype Decisions — reference solution.

Every tier is a dtype-range or precision-budget decision, fully
vectorized. No Python loops anywhere.
"""

import numpy as np

_INT_DTYPES = (np.int8, np.int16, np.int32, np.int64)


def int_downcast(values: np.ndarray) -> np.ndarray:
    """Cast `values` to the smallest int dtype that holds it safely."""
    if values.dtype.kind not in "iu":
        raise ValueError(f"expected an integer array, got {values.dtype}")
    lo, hi = int(values.min()), int(values.max())
    if lo >= np.iinfo(np.int8).min and hi <= np.iinfo(np.int8).max:
        return values.astype(np.int8)
    if lo >= np.iinfo(np.int16).min and hi <= np.iinfo(np.int16).max:
        return values.astype(np.int16)
    if lo >= np.iinfo(np.int32).min and hi <= np.iinfo(np.int32).max:
        return values.astype(np.int32)
    if lo >= np.iinfo(np.int64).min and hi <= np.iinfo(np.int64).max:
        return values.astype(np.int64)
    raise ValueError("values overflow int64")


def sanitize(X: np.ndarray, fill: float) -> tuple[np.ndarray, int]:
    """Replace nan/inf with `fill`; return (cleaned, n_bad)."""
    bad = ~np.isfinite(X)
    cleaned = X.copy()
    cleaned[bad] = fill
    return cleaned, int(bad.sum())


def serving_cast(weights: np.ndarray, budget: float) -> np.ndarray:
    """Cast to float16 iff worst-case relative error <= budget."""
    if weights.dtype == np.float16:
        return weights
    half = weights.astype(np.float16)
    err = half.astype(weights.dtype)          # back-cast, reuse buffer
    np.abs(err - weights, out=err)            # |round(x) - x|
    denom = np.abs(weights)                   # second buffer for |x| + eps
    denom += 1e-30
    np.divide(err, denom, out=err)
    if float(err.max()) <= budget:
        return half
    return weights
