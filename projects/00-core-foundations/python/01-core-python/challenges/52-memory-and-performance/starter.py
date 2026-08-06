"""
Challenge 52: Memory & Performance — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from pathlib import Path


def embedding_ram_bytes(rows: int, dim: int, dtype_bits: int = 32) -> int:
    """Total bytes for a rows x dim matrix: rows * dim * (dtype_bits // 8)."""
    raise NotImplementedError


def streaming_stats(path: Path) -> tuple[float, float]:
    """Return (mean, population variance) of the numbers in the file
    (one per line, blanks skipped). Single pass, O(1) memory."""
    raise NotImplementedError


def corpus_stats(path: Path) -> dict:
    """One pass over a token-per-line corpus. Return dict with keys:
    lines, total_chars, longest, histogram (token length -> count)."""
    raise NotImplementedError


def embedding_budget(
    ram_bytes: int,
    model_bytes: int,
    index_bytes: int,
    dim: int,
    dtype_bits: int = 32,
) -> int:
    """Largest embedding batch (rows) fitting in remaining RAM, or 0."""
    raise NotImplementedError
