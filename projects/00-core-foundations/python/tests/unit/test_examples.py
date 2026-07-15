"""
Unit tests for basic Python concepts (01-41).
These tests verify that the example code runs correctly and produces expected results.
"""

import subprocess
import sys
from pathlib import Path
import pytest


class TestBasicPythonExamples:
    """Test that all basic Python example files execute without errors."""

    @pytest.fixture(autouse=True)
    def setup(self, examples_dir):
        self.examples_dir = examples_dir

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "example_file",
        [
            "01-introduction.py",
            "02-get-started.py",
            "03-syntax.py",
            "04-output.py",
            "05-comments.py",
            "06-variables.py",
            "07-data-types.py",
            "08-numbers.py",
            "09-casting.py",
            "10-strings.py",
            "11-booleans.py",
            "12-operators.py",
            "13-lists.py",
            "14-tuples.py",
            "15-sets.py",
            "16-dictionaries.py",
            "17-if-else.py",
            "18-match.py",
            "19-while-loops.py",
            "20-for-loops.py",
            "21-functions.py",
            "22-range.py",
            "23-arrays.py",
            "24-iterators.py",
            "25-modules.py",
            "26-dates.py",
            "27-math.py",
            "28-json.py",
            "29-regex.py",
            "30-try-except.py",
            "31-string-formatting.py",
            "32-none.py",
            "33-user-input.py",
            "34-classes.py",
            "35-inheritance.py",
            "36-polymorphism.py",
            "37-encapsulation.py",
            "38-file-handling.py",
            "39-pip.py",
            "40-virtualenv.py",
            "41-inner-classes.py",
        ],
    )
    def test_example_runs(self, example_file):
        """Test that each example file executes without errors."""
        file_path = self.examples_dir / example_file
        if not file_path.exists():
            pytest.skip(f"File {example_file} not found")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=self.examples_dir,
        )

        assert result.returncode == 0, f"Failed to run {example_file}: {result.stderr}"

    @pytest.mark.unit
    def test_introduction_output(self):
        """Test 01-introduction.py produces expected output."""
        file_path = self.examples_dir / "01-introduction.py"
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.examples_dir,
        )
        assert "Hello, World!" in result.stdout
        assert "Python is versatile and beginner-friendly!" in result.stdout
        assert "Five is greater than two!" in result.stdout
        assert "a = 4" in result.stdout
        assert "A = 5" in result.stdout


class TestAdvancedExamples:
    """Test advanced Python examples."""

    @pytest.fixture(autouse=True)
    def setup(self, examples_dir):
        self.examples_dir = examples_dir / "advanced"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "example_file",
        [
            "01-decorators.py",
            "02-generators.py",
            "03-context-managers.py",
            "04-async-await.py",
            "05-type-hints.py",
            "06-dataclasses.py",
            "07-enum.py",
            "08-abc.py",
            "09-functools.py",
            "10-itertools.py",
            "11-collections.py",
            "12-property.py",
            "13-slots.py",
            "14-metaclasses.py",
            "15-descriptors.py",
            "16-threading.py",
            "17-multiprocessing.py",
            "18-unit-testing.py",
            "19-logging.py",
            "20-patterns.py",
        ],
    )
    def test_advanced_example_runs(self, example_file):
        """Test that each advanced example file executes without errors."""
        file_path = self.examples_dir / example_file
        if not file_path.exists():
            pytest.skip(f"File {example_file} not found")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=self.examples_dir,
        )

        assert result.returncode == 0, f"Failed to run {example_file}: {result.stderr}"


class TestDSAExamples:
    """Test Data Structures and Algorithms examples."""

    @pytest.fixture(autouse=True)
    def setup(self, examples_dir):
        self.examples_dir = examples_dir / "dsa"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "example_file",
        [
            "01-introduction.py",
            "02-arrays.py",
            "03-stacks.py",
            "04-queues.py",
            "05-linked-lists.py",
            "06-hash-tables.py",
            "07-trees.py",
            "08-binary-trees.py",
            "09-binary-search-trees.py",
            "10-avl-trees.py",
            "11-graphs.py",
            "12-linear-search.py",
            "13-binary-search.py",
            "14-bubble-sort.py",
            "15-selection-sort.py",
            "16-insertion-sort.py",
            "17-quick-sort.py",
            "18-counting-sort.py",
            "19-radix-sort.py",
            "20-merge-sort.py",
        ],
    )
    def test_dsa_example_runs(self, example_file):
        """Test that each DSA example file executes without errors."""
        file_path = self.examples_dir / example_file
        if not file_path.exists():
            pytest.skip(f"File {example_file} not found")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=self.examples_dir,
        )

        assert result.returncode == 0, f"Failed to run {example_file}: {result.stderr}"


class TestNumPyExamples:
    """Test NumPy examples."""

    @pytest.fixture(autouse=True)
    def setup(self, examples_dir):
        self.examples_dir = examples_dir / "numpy"

    @pytest.mark.unit
    @pytest.mark.data
    @pytest.mark.parametrize(
        "example_file",
        [
            "01-introduction.py",
            "02-getting-started.py",
            "03-creating-arrays.py",
            "04-array-indexing.py",
            "05-array-slicing.py",
            "06-data-types.py",
            "07-copy-vs-view.py",
            "08-array-shape.py",
            "09-array-reshape.py",
            "10-array-iterating.py",
            "11-array-join.py",
            "12-array-split.py",
            "13-array-search.py",
            "14-array-sort.py",
            "15-array-filter.py",
            "16-random-intro.py",
            "17-data-distribution.py",
            "18-random-permutation.py",
            "19-ufunc-intro.py",
            "20-ufunc-create.py",
            "21-ufunc-arithmetic.py",
            "22-ufunc-rounding.py",
            "23-ufunc-logs.py",
            "24-ufunc-summations.py",
            "25-ufunc-products.py",
            "26-ufunc-differences.py",
            "27-ufunc-trigonometric.py",
            "28-ufunc-set-operations.py",
        ],
    )
    def test_numpy_example_runs(self, example_file):
        """Test that each NumPy example file executes without errors."""
        file_path = self.examples_dir / example_file
        if not file_path.exists():
            pytest.skip(f"File {example_file} not found")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=self.examples_dir,
        )

        assert result.returncode == 0, f"Failed to run {example_file}: {result.stderr}"


class TestPandasExamples:
    """Test Pandas examples."""

    @pytest.fixture(autouse=True)
    def setup(self, examples_dir):
        self.examples_dir = examples_dir / "pandas"

    @pytest.mark.unit
    @pytest.mark.data
    @pytest.mark.parametrize(
        "example_file",
        [
            "01-introduction.py",
            "02-getting-started.py",
            "03-series.py",
            "04-dataframes.py",
            "05-load-data.py",
            "06-reading-json.py",
            "07-data-viewing.py",
            "08-data-selecting.py",
            "09-data-loc.py",
            "10-data-drop.py",
            "11-rename-columns.py",
            "12-iterating.py",
            "13-clearing-data.py",
            "14-data-new-column.py",
            "15-statistics.py",
            "16-scatter-plot.py",
            "17-histogram.py",
            "18-pie-chart.py",
            "19-bar-chart.py",
            "20-merge.py",
            "21-concat.py",
            "22-groupby.py",
            "23-corr.py",
            "24-plotting.py",
        ],
    )
    def test_pandas_example_runs(self, example_file):
        """Test that each Pandas example file executes without errors."""
        file_path = self.examples_dir / example_file
        if not file_path.exists():
            pytest.skip(f"File {example_file} not found")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=self.examples_dir,
        )

        assert result.returncode == 0, f"Failed to run {example_file}: {result.stderr}"


class TestPracticeProblems:
    """Test practice problems."""

    @pytest.fixture(autouse=True)
    def setup(self, examples_dir):
        self.examples_dir = examples_dir

    @pytest.mark.unit
    def test_practice_all_imports(self):
        """Test that practice_all.py can be imported."""
        file_path = self.examples_dir / "practice_all.py"
        result = subprocess.run(
            [sys.executable, "-c", "import practice_all; print('OK')"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.examples_dir,
        )
        assert result.returncode == 0

    @pytest.mark.unit
    def test_practice_no_solutions_imports(self):
        """Test that practice_no_solutions.py can be imported."""
        file_path = self.examples_dir / "practice_no_solutions.py"
        result = subprocess.run(
            [sys.executable, "-c", "import practice_no_solutions; print('OK')"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.examples_dir,
        )
        assert result.returncode == 0
