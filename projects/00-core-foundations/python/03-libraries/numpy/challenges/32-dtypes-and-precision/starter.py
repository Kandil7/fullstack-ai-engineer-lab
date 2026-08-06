"""Challenge 32: Dtype Decisions — starter template.

Implement the three functions below. Read README.md for the
behavior contract and I/O tables.
"""

import numpy as np

_INT_DTYPES = (np.int8, np.int16, np.int32, np.int64)


def int_downcast(values: np.ndarray) -> np.ndarray:
    """Cast `values` to the smallest int dtype that holds it safely.

    Raises ValueError if values are not integer-valued or overflow
    int64.
    """
    raise NotImplementedError


def sanitize(X: np.ndarray, fill: float) -> tuple[np.ndarray, int]:
    """Replace nan/inf with `fill`; return (cleaned, n_bad)."""
    raise NotImplementedError


def serving_cast(weights: np.ndarray, budget: float) -> np.ndarray:
    """Cast to float16 iff worst-case relative error <= budget.

    Return the input unchanged otherwise. Never re-cast float16.
    """
    raise NotImplementedError
