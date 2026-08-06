"""
Challenge 21: Concurrency Comparison — Hidden Tests
====================================================
Runs against starter.py by default; set CHALLENGE_MODULE=solution to
verify the reference implementation.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))  # so spawned workers can import the module


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


target = _load(os.environ.get("CHALLENGE_MODULE", "starter"))


class TestChooseModel:
    def test_few_io_calls_use_threads(self):
        assert target.choose_model("io", 10) == "threads"

    def test_many_io_calls_use_async(self):
        assert target.choose_model("io", 10_000) == "async"

    def test_cpu_uses_processes(self):
        assert target.choose_model("cpu", 1) == "processes"
        assert target.choose_model("cpu", 1_000_000) == "processes"

    def test_unknown_workload_raises(self):
        with pytest.raises(ValueError):
            target.choose_model("gpu", 5)

    def test_boundary_is_exclusive(self):
        assert target.choose_model("io", 100) == "threads"


class TestIoOverlap:
    def test_overlaps_fast(self):
        elapsed = target.run_io_overlap(8, 0.05)
        assert elapsed > 0
        assert elapsed < 8 * 0.05 * 0.6, (
            f"sequential took {elapsed:.3f}s; overlap must beat 0.24s"
        )

    def test_overlaps_more(self):
        elapsed = target.run_io_overlap(16, 0.05)
        assert elapsed < 16 * 0.05 * 0.6, (
            f"sequential took {elapsed:.3f}s; overlap must beat 0.48s"
        )


class TestCpuWorker:
    def test_correct_small(self):
        assert target._cpu_worker(5) == 30  # 0+1+4+9+16

    def test_correct_medium(self):
        assert target._cpu_worker(1000) == sum(i * i for i in range(1000))

    def test_worker_is_module_level(self):
        assert "<locals>" not in target._cpu_worker.__qualname__, (
            "worker must be module-level: nested functions break Windows spawn"
        )


class TestCpuParallel:
    def test_parallel_beats_sequential(self):
        sequential = target.run_cpu_sequential(4, 10_000_000)
        parallel = target.run_cpu_parallel(4, 10_000_000)
        assert parallel < sequential * 0.85, (
            f"parallel {parallel:.2f}s vs sequential {sequential:.2f}s: "
            "threads would be ~equal under the GIL; processes must win"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
