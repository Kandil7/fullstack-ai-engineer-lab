"""
Challenge 22: Asyncio Advanced — Hidden Tests
==============================================
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


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


target = _load(os.environ.get("CHALLENGE_MODULE", "starter"))


class TestRunLimited:
    def test_caps_at_limit(self):
        completed, max_seen = target.run_limited(8, 3)
        assert completed == 8
        assert max_seen == 3, f"max in-flight was {max_seen}, expected 3"

    def test_larger_limit(self):
        completed, max_seen = target.run_limited(20, 5)
        assert completed == 20
        assert max_seen == 5

    def test_limit_larger_than_calls(self):
        completed, max_seen = target.run_limited(5, 10)
        assert completed == 5
        assert max_seen == 5, "cannot exceed the number of calls"

    def test_limit_one(self):
        completed, max_seen = target.run_limited(3, 1)
        assert completed == 3
        assert max_seen == 1


class TestPipeline:
    def test_bounded_small_queue(self):
        processed, max_observed = target.pipeline(["a"] * 20, 2)
        assert processed == 20
        assert max_observed == 2, (
            f"queue grew to {max_observed}: unbounded list, no backpressure"
        )

    def test_bounded_larger_queue(self):
        processed, max_observed = target.pipeline(["a"] * 10, 5)
        assert processed == 10
        assert max_observed == 5

    def test_queue_bigger_than_items(self):
        processed, max_observed = target.pipeline(["a"] * 3, 10)
        assert processed == 3
        assert max_observed == 3

    def test_empty(self):
        processed, max_observed = target.pipeline([], 2)
        assert processed == 0
        assert max_observed == 0


class TestRunBatch:
    def test_middle_failure(self):
        completed, cancelled = target.run_batch(5, 2)
        assert completed == 2
        assert cancelled == 2, (
            f"cancelled {cancelled}: gather-based batches cancel nothing"
        )

    def test_first_failure(self):
        completed, cancelled = target.run_batch(3, 0)
        assert completed == 0
        assert cancelled == 2

    def test_last_failure(self):
        completed, cancelled = target.run_batch(4, 3)
        assert completed == 3
        assert cancelled == 0

    def test_larger_batch(self):
        completed, cancelled = target.run_batch(7, 4)
        assert completed == 4
        assert cancelled == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
