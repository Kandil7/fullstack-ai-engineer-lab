"""
Unit tests for NumPy examples.
Every file is executed and must exit successfully.
"""

import pytest

from tests.unit.helpers import discover_phase_files, run_py_file

NUMPY_FILES = discover_phase_files("03-libraries/numpy")


@pytest.mark.parametrize("filepath", NUMPY_FILES, ids=lambda p: p.name)
def test_numpy_example_runs(filepath):
    """Every NumPy example must execute without errors."""
    result = run_py_file(filepath, timeout=60)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )
