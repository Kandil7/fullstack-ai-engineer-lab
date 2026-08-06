"""
Challenge 40: Memory Optimization — Starter
============================================
Fill in the bodies. Do not change signatures or docstrings.
"""

from __future__ import annotations

import pandas as pd


def measure_deep(frame: pd.DataFrame) -> int:
    """Total honest memory usage of the frame, including object payloads."""
    raise NotImplementedError


def optimize_dtypes(frame: pd.DataFrame) -> pd.DataFrame:
    """New frame with downcast ints/floats and low-cardinality categories.

    Integers preserved exactly; floats within float32 rounding.
    """
    raise NotImplementedError


def streamed_mean(csv_text: str, col: str, chunksize: int) -> float:
    """Mean of a CSV column without materializing the whole file."""
    raise NotImplementedError
