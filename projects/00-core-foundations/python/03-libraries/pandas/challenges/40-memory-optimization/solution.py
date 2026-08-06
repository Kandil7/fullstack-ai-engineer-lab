"""
Challenge 40: Memory Optimization — Reference Solution
========================================================
Why this approach:
- measure_deep: memory_usage(deep=True) is the only honest count for
  object columns; .sum() gives the frame total.
- optimize_dtypes: pd.to_numeric with downcast picks the smallest
  dtype per column; the 10% cardinality heuristic decides category;
  booleans are left alone. A copy() keeps the input untouched.
- streamed_mean: chunked read + accumulate sum/count; peak memory is
  one chunk plus the StringIO buffer — never the full frame.
"""

from __future__ import annotations

import io

import numpy as np
import pandas as pd


def measure_deep(frame: pd.DataFrame) -> int:
    """Total honest memory usage of the frame, including object payloads."""
    return int(frame.memory_usage(deep=True).sum())


def optimize_dtypes(frame: pd.DataFrame) -> pd.DataFrame:
    """New frame with downcast ints/floats and low-cardinality categories.

    Integers preserved exactly; floats within float32 rounding.
    """
    out = frame.copy()
    for col in out.columns:
        col_type = out[col].dtype
        if pd.api.types.is_integer_dtype(col_type):
            out[col] = pd.to_numeric(out[col], downcast="integer")
        elif pd.api.types.is_float_dtype(col_type):
            out[col] = pd.to_numeric(out[col], downcast="float")
        elif pd.api.types.is_bool_dtype(col_type):
            continue
        elif pd.api.types.is_object_dtype(col_type):
            if out[col].nunique() / len(out) < 0.1:
                out[col] = out[col].astype("category")
    return out


def streamed_mean(csv_text: str, col: str, chunksize: int) -> float:
    """Mean of a CSV column without materializing the whole file."""
    total = 0.0
    count = 0
    for chunk in pd.read_csv(io.StringIO(csv_text), chunksize=chunksize):
        total += float(chunk[col].sum())
        count += int(chunk[col].count())
    if count == 0:
        return float("nan")
    return total / count
