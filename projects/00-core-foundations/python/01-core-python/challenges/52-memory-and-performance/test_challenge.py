"""
Challenge 52: Memory & Performance — Tests

Runs against starter.py by default (functions raise NotImplementedError
and must FAIL). Set CHALLENGE_USE_SOLUTION=1 to validate solution.py
(expect ALL PASS).
"""

from __future__ import annotations

import importlib.util
import os
import tracemalloc
from pathlib import Path

import pytest

_DIR = Path(__file__).parent
_TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"

_spec = importlib.util.spec_from_file_location("mod52", _DIR / f"{_TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def _call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except NotImplementedError:
        pytest.fail("Not implemented yet")


# ------------------------------------------------------------------ data


@pytest.fixture(scope="module")
def big_ints_file(tmp_path_factory) -> Path:
    """1..1_000_000, one per line (written in chunks)."""
    p = tmp_path_factory.mktemp("data") / "ints.txt"
    n = 1_000_000
    with p.open("w", encoding="utf-8") as f:
        for start in range(1, n + 1, 50_000):
            f.write("".join(f"{i}\n" for i in range(start, start + 50_000)))
    return p


@pytest.fixture(scope="module")
def big_tokens_file(tmp_path_factory) -> Path:
    """tok-1 .. tok-1_000_000 (variable token length 8..13 chars)."""
    p = tmp_path_factory.mktemp("data") / "tokens.txt"
    n = 1_000_000
    with p.open("w", encoding="utf-8") as f:
        for start in range(1, n + 1, 50_000):
            f.write(
                "".join(f"tok-{i}\n" for i in range(start, start + 50_000))
            )
    return p


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "data.txt"
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------- Bronze


def test_ram_float32_1m_x_768():
    assert _call(mod.embedding_ram_bytes, 1_000_000, 768, 32) == 3_072_000_000


def test_ram_float16_half():
    assert _call(mod.embedding_ram_bytes, 1_000_000, 768, 16) == 1_536_000_000


def test_ram_float64_double():
    assert _call(mod.embedding_ram_bytes, 1_000_000, 768, 64) == 6_144_000_000


def test_ram_zero_rows():
    assert _call(mod.embedding_ram_bytes, 0, 768, 32) == 0


def test_ram_default_dtype_is_32():
    assert _call(mod.embedding_ram_bytes, 100, 10) == 100 * 10 * 4


# ---------------------------------------------------------------- Silver


def test_stats_known_dataset(tmp_path):
    p = _write(tmp_path, "2\n4\n4\n4\n5\n5\n7\n9\n")
    mean, var = _call(mod.streaming_stats, p)
    assert mean == pytest.approx(5.0)
    assert var == pytest.approx(4.0)  # sum((x-mean)^2)/n = 32/8


def test_stats_three_values(tmp_path):
    p = _write(tmp_path, "1\n2\n3\n")
    mean, var = _call(mod.streaming_stats, p)
    assert mean == pytest.approx(2.0)
    assert var == pytest.approx(2.0 / 3.0)


def test_stats_single_value(tmp_path):
    p = _write(tmp_path, "10\n")
    mean, var = _call(mod.streaming_stats, p)
    assert (mean, var) == (10.0, 0.0)


def test_stats_blank_lines_skipped(tmp_path):
    p = _write(tmp_path, "\n\n5\n\n")
    mean, var = _call(mod.streaming_stats, p)
    assert (mean, var) == (5.0, 0.0)


def test_stats_empty_file(tmp_path):
    p = _write(tmp_path, "")
    assert _call(mod.streaming_stats, p) == (0.0, 0.0)


def test_stats_million_values_streaming(big_ints_file):
    """1..1e6: mean = (n+1)/2, population variance = (n^2 - 1)/12.
    Streaming peak must stay under 2 MiB (materialized: ~32 MB)."""
    n = 1_000_000
    tracemalloc.start()
    mean, var = _call(mod.streaming_stats, big_ints_file)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert mean == pytest.approx((n + 1) / 2, rel=1e-9)
    assert var == pytest.approx((n * n - 1) / 12, rel=1e-6)
    assert peak < 2 * 1024 * 1024, (
        f"peak {peak / 1024 / 1024:.1f} MiB >= 2 MiB ceiling — "
        "did you materialize the values?"
    )


# ------------------------------------------------------------------ Gold


def test_corpus_stats_small(tmp_path):
    p = _write(tmp_path, "abc\na\nabc\nxy\n")
    assert _call(mod.corpus_stats, p) == {
        "lines": 4,
        "total_chars": 9,
        "longest": 3,
        "histogram": {3: 2, 1: 1, 2: 1},
    }


def test_corpus_stats_blank_line_counts_as_token(tmp_path):
    p = _write(tmp_path, "abc\n\na\n")
    assert _call(mod.corpus_stats, p)["histogram"] == {3: 1, 0: 1, 1: 1}


def test_corpus_stats_million_tokens_streaming(big_tokens_file):
    """Tokens tok-1..tok-1_000_000: length = 4 + len(str(i)) -> 5 chars
    for 1..9, 6 for 10..99, ... 11 for 1_000_000. Streaming peak
    < 50 MiB (a materialized token list is ~65 MB)."""
    expected_hist = {
        5: 9,
        6: 90,
        7: 900,
        8: 9_000,
        9: 90_000,
        10: 900_000,
        11: 1,
    }
    expected_chars = sum(l * c for l, c in expected_hist.items())
    tracemalloc.start()
    stats = _call(mod.corpus_stats, big_tokens_file)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert stats["lines"] == 1_000_000
    assert stats["total_chars"] == expected_chars
    assert stats["longest"] == 11
    assert stats["histogram"] == expected_hist
    assert sum(stats["histogram"].values()) == stats["lines"]
    assert peak < 50 * 1024 * 1024, (
        f"peak {peak / 1024 / 1024:.1f} MiB >= 50 MiB ceiling — "
        "did you materialize the tokens?"
    )


def test_budget_32gb_768_float32():
    assert _call(mod.embedding_budget, 32_000_000_000, 8_000_000_000, 4_000_000_000, 768, 32) == 6_510_416


def test_budget_float16_doubles_batch():
    assert _call(mod.embedding_budget, 32_000_000_000, 8_000_000_000, 4_000_000_000, 768, 16) == 13_020_833


def test_budget_no_room():
    assert _call(mod.embedding_budget, 8_000_000_000, 8_000_000_000, 4_000_000_000, 768, 32) == 0
