"""
Challenge 44: Logging — Hidden Tests
====================================
"""

from __future__ import annotations

import importlib.util
import logging
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
import pytest


class TestLevelRank:
    def test_known_levels(self):
        assert solution.level_rank("DEBUG") == 10
        assert solution.level_rank("INFO") == 20
        assert solution.level_rank("WARNING") == 30
        assert solution.level_rank("ERROR") == 40
        assert solution.level_rank("CRITICAL") == 50

    def test_case_insensitive(self):
        assert solution.level_rank("warning") == 30

    def test_unknown_raises(self):
        with pytest.raises(ValueError):
            solution.level_rank("TRACE")


class TestShouldLog:
    def test_threshold(self):
        assert not solution.should_log("INFO", "DEBUG")
        assert solution.should_log("INFO", "INFO")
        assert solution.should_log("INFO", "WARNING")
        assert solution.should_log("WARNING", "ERROR")

    def test_boundary(self):
        assert solution.should_log("ERROR", "ERROR")
        assert not solution.should_log("ERROR", "WARNING")


class TestMakeLogger:
    def test_level_filtering(self):
        logger = solution.make_logger("challenge44.filter", "INFO")
        logger.debug("dropped")
        logger.info("kept-info")
        logger.warning("kept-warning")
        text = logger.handlers[0].stream.getvalue()
        assert "dropped" not in text, "DEBUG must be filtered at INFO threshold"
        assert "kept-info" in text and "kept-warning" in text

    def test_single_handler(self):
        logger = solution.make_logger("challenge44.single", "DEBUG")
        assert len(logger.handlers) == 1, "exactly one handler"

    def test_no_propagation(self):
        logger = solution.make_logger("challenge44.noprop", "INFO")
        assert logger.propagate is False, "must not double-emit via root"

    def test_reentrant(self):
        a = solution.make_logger("challenge44.reentrant", "INFO")
        b = solution.make_logger("challenge44.reentrant", "ERROR")
        # second call replaces handlers; no duplicates accumulate
        assert len(a.handlers) == 1 and len(b.handlers) == 1


class TestCorrelatedLogger:
    def test_prefix_on_info_and_error(self):
        log = solution.CorrelatedLogger("challenge44.corr", "rid-7ac9")
        log.info("started")
        log.error("failed")
        text = log.captured()
        assert "[rid-7ac9] started" in text, "info line must carry the ID"
        assert "[rid-7ac9] failed" in text, "error line must carry the ID"

    def test_every_line_prefixed(self):
        log = solution.CorrelatedLogger("challenge44.every", "rid-x1")
        for i in range(100):
            log.info(f"event {i}")
        lines = [ln for ln in log.captured().splitlines() if ln.strip()]
        assert len(lines) == 100
        assert all("[rid-x1] event" in ln for ln in lines), \
            "every emitted line must carry the request ID prefix"

    def test_distinct_ids_isolated(self):
        a = solution.CorrelatedLogger("challenge44.iso_a", "AAA")
        b = solution.CorrelatedLogger("challenge44.iso_b", "BBB")
        a.info("hello")
        assert "AAA" in a.captured() and "BBB" not in a.captured()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
