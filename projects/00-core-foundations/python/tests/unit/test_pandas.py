"""
Unit tests for pandas examples.
Every exercise is executed and must exit successfully. The two case studies
(23/24) need optional dependencies (statsmodels/pyarrow/category_encoders)
and are compile-checked instead.
"""

import pytest

from tests.unit.helpers import (
    PROJECT_ROOT,
    PANDAS_CASE_STUDY_SKIP,
    compile_check,
    discover_phase_files,
    run_py_file,
)

PANDAS_FILES = discover_phase_files("03-libraries/pandas", skip=PANDAS_CASE_STUDY_SKIP)
PANDAS_DIR = PROJECT_ROOT / "03-libraries" / "pandas"
CASE_STUDIES = sorted(
    f for f in PANDAS_DIR.glob("*.py")
    if f.name in PANDAS_CASE_STUDY_SKIP and f.is_file()
)


@pytest.mark.parametrize("filepath", PANDAS_FILES, ids=lambda p: p.name)
def test_pandas_example_runs(filepath):
    """Every pandas exercise must execute without errors."""
    result = run_py_file(filepath, timeout=120)
    assert result.returncode == 0, (
        f"{filepath.name} failed:\n{result.stderr[-500:]}"
    )


@pytest.mark.parametrize("filepath", CASE_STUDIES, ids=lambda p: p.name)
def test_pandas_case_study_compiles(filepath):
    """Case studies must at least parse (deps: statsmodels/pyarrow/category_encoders)."""
    assert compile_check(filepath), f"{filepath.name} failed to compile"
