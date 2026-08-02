"""
Unit tests for Machine Learning examples.
Every file is executed and must exit successfully (sklearn optional).
"""

import pytest

sklearn = pytest.importorskip("sklearn")

from tests.unit.helpers import discover_phase_files, run_py_file

ML_FILES = discover_phase_files("07-machine-learning")


@pytest.mark.parametrize("filepath", ML_FILES, ids=lambda p: p.name)
def test_ml_example_runs(filepath):
    """Every ML example must execute without errors."""
    result = run_py_file(filepath, timeout=180)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )
