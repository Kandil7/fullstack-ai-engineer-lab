"""
Challenge 52: Memory & Performance — Reference Solution
=========================================================
"""

from __future__ import annotations

from pathlib import Path


def embedding_ram_bytes(rows: int, dim: int, dtype_bits: int = 32) -> int:
    """Total bytes for a rows x dim matrix: rows * dim * (dtype_bits // 8).

    Why this approach: the whiteboard formula — each element is
    dtype_bits // 8 bytes; the matrix is a dense rectangle.
    """
    return rows * dim * (dtype_bits // 8)


def streaming_stats(path: Path) -> tuple[float, float]:
    """Return (mean, population variance) of the numbers in the file.

    Why this approach: Welford's online algorithm keeps only the count,
    running mean, and sum of squared deviations — O(1) memory, one
    pass. Collecting the values would be O(n) memory (~32 MB for 1M
    floats) and would fail the tracemalloc ceiling.
    """
    n = 0
    mean = 0.0
    m2 = 0.0
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x = float(line)
            n += 1
            delta = x - mean
            mean += delta / n
            m2 += delta * (x - mean)
    if n == 0:
        return 0.0, 0.0
    return mean, m2 / n


def corpus_stats(path: Path) -> dict:
    """One pass over a token-per-line corpus.

    Why this approach: each line is stripped of its trailing newline
    and processed immediately — the histogram dict is bounded by the
    max token length, so memory is O(max_len), not O(n). A naive
    `list(path.open())` materializes every token (~70 MB for 1M lines)
    and fails the 50 MiB ceiling.
    """
    lines = 0
    total_chars = 0
    longest = 0
    histogram: dict[int, int] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            token = line.rstrip("\r\n")
            length = len(token)
            lines += 1
            total_chars += length
            if length > longest:
                longest = length
            histogram[length] = histogram.get(length, 0) + 1
    return {
        "lines": lines,
        "total_chars": total_chars,
        "longest": longest,
        "histogram": histogram,
    }


def embedding_budget(
    ram_bytes: int,
    model_bytes: int,
    index_bytes: int,
    dim: int,
    dtype_bits: int = 32,
) -> int:
    """Largest embedding batch (rows) fitting in remaining RAM, or 0.

    Why this approach: available = ram - model - index; the per-row
    cost is dim * (dtype_bits // 8); floor division answers "how many
    whole rows fit" — the batch-size-before-OOM calculation.
    """
    available = ram_bytes - model_bytes - index_bytes
    if available <= 0:
        return 0
    return available // (dim * (dtype_bits // 8))
