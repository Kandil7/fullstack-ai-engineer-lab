"""
Unit tests for Phase 2 advanced Python examples.
The exercise files are flat, self-contained scripts, so each is executed and
must exit successfully (same contract as the smoke runner).
"""

import pytest

from tests.unit.helpers import discover_phase_files, run_py_file

PHASE2_FILES = discover_phase_files("02-advanced-python")


@pytest.mark.parametrize("filepath", PHASE2_FILES, ids=lambda p: p.name)
def test_advanced_example_runs(filepath):
    """Every advanced example must execute without errors."""
    result = run_py_file(filepath, timeout=120)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )
