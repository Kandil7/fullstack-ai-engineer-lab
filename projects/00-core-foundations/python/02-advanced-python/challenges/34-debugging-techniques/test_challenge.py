"""
Challenge 34: Debugging Techniques — Hidden Tests
=================================================
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
import pytest  # noqa: E402


# ============================================================
# Bronze: Full-Stack Logging
# ============================================================

def test_capture_success_returns_empty():
    assert solution.capture(lambda: None) == ""


def test_capture_failure_returns_full_traceback():
    tb = solution.capture(lambda: 1 / 0)
    assert tb.startswith("Traceback (most recent call last):")
    assert "ZeroDivisionError" in tb


def test_capture_never_raises():
    assert isinstance(solution.capture(lambda: (_ for _ in ()).throw(
        ValueError("boom"))), str)


def test_capture_includes_frames():
    def inner():
        raise KeyError("k")

    def outer():
        inner()

    tb = solution.capture(outer)
    assert "inner" in tb and "outer" in tb, "all frames must be in the stack"


def test_format_exception_text():
    exc = ValueError("chunk index out of range")
    text = solution.format_exception_text(exc)
    assert "ValueError" in text
    assert "chunk index out of range" in text


# ============================================================
# Silver: Boundary-Asserting Pipeline
# ============================================================

def test_pipeline_normal():
    pipe = solution.DebugPipeline()
    # stable sort by length: "a" and "b" tie, original order preserved
    assert pipe.run([" a ", "b", "a"]) == ["a", "b"]


def test_pipeline_sorts_by_length():
    pipe = solution.DebugPipeline()
    assert pipe.run(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]


def test_pipeline_catches_empty_after_strip():
    pipe = solution.DebugPipeline()
    with pytest.raises(AssertionError, match="stage-1"):
        pipe.run([" ok ", ""])


def test_pipeline_catches_non_string():
    pipe = solution.DebugPipeline()
    with pytest.raises(AssertionError, match="stage-1"):
        pipe.run(["x", None])


def test_pipeline_dedup_preserves_order():
    pipe = solution.DebugPipeline()
    # equal lengths -> stable sort keeps first-seen order
    assert pipe.run(["b", "a", "b", "a", "c"]) == ["b", "a", "c"]


# ============================================================
# Gold: Repro Harness
# ============================================================

def test_repro_same_seed_identical():
    a = solution.make_repro(42)(["a", "b", "c", "d", "e"])
    b = solution.make_repro(42)(["a", "b", "c", "d", "e"])
    assert a == b, "same seed must reproduce identically"


def test_repro_different_seeds_differ():
    a = solution.make_repro(1)(["a", "b", "c", "d", "e"])
    b = solution.make_repro(2)(["a", "b", "c", "d", "e"])
    assert a != b, "different seeds must (almost surely) differ"


def test_repro_is_permutation():
    items = ["a", "b", "c", "d", "e"]
    out = solution.make_repro(7)(items)
    assert sorted(out) == sorted(items), "shuffle must be a permutation"


def test_repro_does_not_mutate_input():
    items = ["a", "b", "c"]
    solution.make_repro(3)(items)
    assert items == ["a", "b", "c"], "shuffle must copy before shuffling"


# ============================================================
# Gold: Config Bisect
# ============================================================

def _bound(n: int) -> int:
    return math.ceil(math.log2(n)) + 1


def test_bisect_middle():
    configs = [f"c{i}" for i in range(100)]
    idx, probes = solution.bisect_bad(configs, 42)
    assert idx == 42
    assert probes <= _bound(100), f"{probes} > {_bound(100)}"


def test_bisect_first_bad():
    configs = [f"c{i}" for i in range(64)]
    idx, probes = solution.bisect_bad(configs, 0)
    assert idx == 0
    assert probes <= _bound(64)


def test_bisect_last_bad():
    configs = [f"c{i}" for i in range(64)]
    idx, probes = solution.bisect_bad(configs, 63)
    assert idx == 63
    assert probes <= _bound(64)


def test_bisect_odd_size():
    configs = [f"c{i}" for i in range(57)]
    idx, probes = solution.bisect_bad(configs, 31)
    assert idx == 31
    assert probes <= _bound(57)


def test_bisect_logarithmic_growth():
    # doubling n must add at most ~1 probe
    _, probes_small = solution.bisect_bad([f"c{i}" for i in range(128)], 50)
    _, probes_large = solution.bisect_bad(
        [f"c{i}" for i in range(10_000)], 5_000)
    assert probes_large <= _bound(10_000)
    assert probes_large <= probes_small + 8, "log growth: ~1 probe per doubling"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
