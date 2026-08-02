"""
Unit tests for Phase 8 MLOps examples.
Every file is executed and must exit successfully. The exercises are
self-verifying (each ends with a _verify() block that runs on plain
execution), so a clean run is the assertion.
"""

import os
import subprocess
import sys

import pytest

from tests.unit.helpers import PROJECT_ROOT, discover_phase_files, run_py_file

MLOPS_FILES = discover_phase_files("08-mlops")


@pytest.mark.unit
@pytest.mark.parametrize("filepath", MLOPS_FILES, ids=lambda p: p.name)
def test_mlops_example_runs(filepath):
    """Every MLOps exercise must execute without errors (self-verifying)."""
    result = run_py_file(filepath, timeout=120)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )


@pytest.mark.unit
def test_mlops_verify_mode():
    """Each exercise must also pass in --verify mode."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    for filepath in MLOPS_FILES:
        result = subprocess.run(
            [sys.executable, str(filepath), "--verify"],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_ROOT), env=env,
        )
        assert result.returncode == 0, (
            f"{filepath.name} --verify failed:\n{result.stderr[-500:]}"
        )
