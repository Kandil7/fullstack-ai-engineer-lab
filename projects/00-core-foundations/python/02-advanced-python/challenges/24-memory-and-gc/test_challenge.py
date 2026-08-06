"""
Challenge 24: Memory Management and GC — Hidden Tests
=====================================================
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


class TestCollectCycle:
    def test_two_node_cycle(self):
        assert target.collect_cycle(2) == 2

    def test_five_node_cycle(self):
        assert target.collect_cycle(5) == 5

    def test_self_cycle(self):
        assert target.collect_cycle(1) == 1

    def test_ten_node_cycle(self):
        assert target.collect_cycle(10) == 10


class TestSlotsRatio:
    def test_slots_win_at_scale(self):
        ratio = target.slots_ratio(10_000)
        assert ratio >= 1.5, (
            f"ratio {ratio:.2f}: got sizeof-only ~1.0? __dict__ must be included"
        )

    def test_ratio_is_finite(self):
        ratio = target.slots_ratio(1_000)
        assert ratio == ratio  # not NaN
        assert ratio > 0


class TestWeakCacheTrap:
    def test_temp_is_evicted_instantly(self):
        trap_len, alive_len, after_del_len = target.weak_cache_trap()
        assert trap_len == 0, (
            f"trap_len {trap_len}: temporaries must be evicted at line end"
        )

    def test_owned_entry_lives(self):
        _, alive_len, _ = target.weak_cache_trap()
        assert alive_len == 1

    def test_owner_death_evicts(self):
        _, _, after_del_len = target.weak_cache_trap()
        assert after_del_len == 0


class TestTracer:
    def test_totals_agree(self):
        total_m, _ = target.sum_materialized(100_000)
        total_s, _ = target.sum_streamed(100_000)
        assert total_m == total_s == sum(range(100_000))

    def test_materialized_peaks_higher(self):
        _, peak_m = target.sum_materialized(100_000)
        _, peak_s = target.sum_streamed(100_000)
        assert peak_m >= peak_s * 10, (
            f"materialized peak {peak_m} vs streamed {peak_s}: "
            "materializing the list must dominate the peak"
        )

    def test_peak_is_plausible(self):
        _, peak_m = target.sum_materialized(100_000)
        assert peak_m > 1_000_000, "a 100k-int list must be megabytes"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
