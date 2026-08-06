"""
Challenge 27: Packaging and Distribution — Hidden Tests
========================================================
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

MANIFEST = """
[project]
name = "rag_utils"
version = "1.2.0"
requires-python = ">=3.10"
dependencies = ["numpy>=1.26,<3", "pydantic>=2.5"]

[project.optional-dependencies]
dev = ["pytest>=8.0"]
qdrant = ["qdrant-client>=1.9"]

[project.scripts]
rag-index = "rag_utils.indexer:main"
"""


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


target = _load(os.environ.get("CHALLENGE_MODULE", "starter"))


class TestParseVersion:
    def test_plain(self):
        assert target.parse_version("1.2.0")[:3] == (1, 2, 0)

    def test_rc_suffix(self):
        assert target.parse_version("1.2.0rc1") == (1, 2, 0, 1)

    def test_zero_padding(self):
        assert target.parse_version("1.26")[:3] == (1, 26, 0)

    def test_final_after_rc(self):
        assert target.parse_version("1.2.0")[3] > target.parse_version("1.2.0rc1")[3]


class TestCompare:
    def test_rc_before_final(self):
        assert target.compare_versions("1.2.0rc1", "1.2.0") == -1

    def test_major_dominates(self):
        assert target.compare_versions("2.0.0", "1.9.9") == 1

    def test_numeric_not_lexicographic(self):
        assert target.compare_versions("1.10.0", "1.9.9") == 1, (
            "string compare gives '1.10.0' < '1.9.9' — compare int tuples"
        )

    def test_zero_padding_equal(self):
        assert target.compare_versions("1.26", "1.26.0") == 0

    def test_equal(self):
        assert target.compare_versions("1.2.0", "1.2.0") == 0


class TestMatchesRequirement:
    def test_bounded_range_in(self):
        assert target.matches_requirement(">=1.26,<3", "1.26.0") is True

    def test_bounded_range_out(self):
        assert target.matches_requirement(">=1.26,<3", "3.0.0") is False

    def test_exact_with_padding(self):
        assert target.matches_requirement("==2.0", "2.0.0") is True

    def test_lt(self):
        assert target.matches_requirement("<2", "1.9.9") is True
        assert target.matches_requirement("<2", "2.0.0") is False

    def test_gt_rc(self):
        assert target.matches_requirement(">1.2.0rc1", "1.2.0") is True


class TestLatestCompatible:
    def test_skips_newer_major(self):
        assert target.latest_compatible(
            ["1.9.9", "1.10.0", "2.0.0rc1"], ">=1.9,<2"
        ) == "1.10.0"

    def test_final_beats_rc(self):
        assert target.latest_compatible(
            ["1.0.0", "1.2.0rc1", "1.2.0"], ">=1.1"
        ) == "1.2.0"

    def test_none_matches(self):
        assert target.latest_compatible(["1.0.0"], ">=2.0") is None

    def test_empty_available(self):
        assert target.latest_compatible([], ">=1.0") is None


class TestPyprojectInfo:
    def test_name_version(self):
        info = target.pyproject_info(MANIFEST)
        assert info["name"] == "rag_utils"
        assert info["version"] == "1.2.0"

    def test_requires_python(self):
        assert target.pyproject_info(MANIFEST)["requires_python"] == ">=3.10"

    def test_dependencies(self):
        deps = target.pyproject_info(MANIFEST)["dependencies"]
        assert deps == ["numpy>=1.26,<3", "pydantic>=2.5"]

    def test_extras(self):
        extras = target.pyproject_info(MANIFEST)["extras"]
        assert extras["dev"] == ["pytest>=8.0"]
        assert extras["qdrant"] == ["qdrant-client>=1.9"]

    def test_scripts(self):
        scripts = target.pyproject_info(MANIFEST)["scripts"]
        assert scripts == {"rag-index": "rag_utils.indexer:main"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
