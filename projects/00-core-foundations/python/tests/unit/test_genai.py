"""
Unit tests for Phase 9 GenAI examples.
Every file is executed and must exit successfully. The exercises are
self-contained and deterministic (mock LLM/embedding functions; no network
calls), so a clean run is the assertion.
"""

import os
import subprocess
import sys

import pytest

from tests.unit.helpers import PROJECT_ROOT, discover_phase_files, run_py_file

GENAI_FILES = discover_phase_files("09-genai")


@pytest.mark.unit
@pytest.mark.parametrize("filepath", GENAI_FILES, ids=lambda p: p.name)
def test_genai_example_runs(filepath):
    """Every GenAI exercise must execute without errors (self-verifying)."""
    result = run_py_file(filepath, timeout=120)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )


@pytest.mark.unit
def test_genai_verify_mode():
    """Each exercise must also pass in --verify mode."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    for filepath in GENAI_FILES:
        result = subprocess.run(
            [sys.executable, str(filepath), "--verify"],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_ROOT), env=env,
        )
        assert result.returncode == 0, (
            f"{filepath.name} --verify failed:\n{result.stderr[-500:]}"
        )
