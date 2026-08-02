"""
Unit tests for Data Structures & Algorithms examples.
Every file is executed and must exit successfully.
"""

import pytest

from tests.unit.helpers import discover_phase_files, run_py_file

DSA_FILES = discover_phase_files("06-data-structures-algorithms")


@pytest.mark.parametrize("filepath", DSA_FILES, ids=lambda p: p.name)
def test_dsa_example_runs(filepath):
    """Every DSA example must execute without errors (and without hanging)."""
    result = run_py_file(filepath, timeout=120)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )
