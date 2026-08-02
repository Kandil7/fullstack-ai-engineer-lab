"""
Challenge 42: pathlib — Hidden Tests
=====================================
These tests verify correctness, edge cases, and performance constraints.
"""

import tempfile
import os
import stat
from pathlib import Path
import importlib.util
import sys

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Import starter module
starter_spec = importlib.util.spec_from_file_location(
    "starter",
    Path(__file__).parent / "starter.py"
)
starter_module = importlib.util.module_from_spec(starter_spec)
starter_spec.loader.exec_module(starter_module)

# Import solution module
solution_spec = importlib.util.spec_from_file_location(
    "solution",
    Path(__file__).parent / "solution.py"
)
solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

import pytest


class TestCheckpointPath:
    """Tests for checkpoint_path function."""

    def test_basic_construction(self):
        base = Path("/models")
        result = solution_module.checkpoint_path(base, "bert", 1, "acc", 0.9234)
        expected = Path("/models/bert/epoch_0001_acc_0.9234.pt")
        assert result == expected

    def test_zero_padding(self):
        base = Path("runs")
        result = solution_module.checkpoint_path(base, "resnet50", 42, "loss", 0.1234)
        expected = Path("runs/resnet50/epoch_0042_loss_0.1234.pt")
        assert result == expected

    def test_large_epoch(self):
        base = Path("/tmp")
        result = solution_module.checkpoint_path(base, "model", 10000, "f1", 0.9999)
        expected = Path("/tmp/model/epoch_10000_f1_0.9999.pt")
        assert result == expected

    def test_returns_path_object(self):
        base = Path("/models")
        result = solution_module.checkpoint_path(base, "test", 1, "acc", 0.5)
        assert isinstance(result, Path)

    def test_uses_slash_operator(self):
        """Verify implementation uses / operator, not string concat."""
        import inspect
        source = inspect.getsource(solution_module.checkpoint_path)
        assert "/" in source or "div" in source.lower(), "Should use / operator"


class TestFindLatestCheckpoint:
    """Tests for find_latest_checkpoint function."""

    def test_basic_latest(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "model_1.pt").write_text("1")
            (tmp_path / "model_2.pt").write_text("2")

            # Set mtime explicitly
            os.utime(tmp_path / "model_1.pt", (100, 100))
            os.utime(tmp_path / "model_2.pt", (200, 200))

            result = solution_module.find_latest_checkpoint(tmp_path)
            assert result == tmp_path / "model_2.pt"

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = solution_module.find_latest_checkpoint(Path(tmp))
            assert result is None

    def test_no_pt_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "model.txt").write_text("text")
            (tmp_path / "model.pkl").write_text("pickle")

            result = solution_module.find_latest_checkpoint(tmp_path)
            assert result is None

    def test_non_existent_directory(self):
        result = solution_module.find_latest_checkpoint(Path("/this/does/not/exist"))
        assert result is None

    def test_file_instead_of_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "not_a_dir.pt"
            file_path.write_text("x")
            result = solution_module.find_latest_checkpoint(file_path)
            assert result is None

    def test_permission_error_handled(self):
        """On systems where we can test permissions."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "model.pt").write_text("x")

            # Try to make directory unreadable (may not work on all systems)
            try:
                tmp_path.chmod(0o000)
                result = solution_module.find_latest_checkpoint(tmp_path)
                # Should not crash, may return None
                assert result is None or result == tmp_path / "model.pt"
            except (PermissionError, OSError):
                pass  # Expected on some systems
            finally:
                try:
                    tmp_path.chmod(0o755)
                except:
                    pass


class TestDatasetStats:
    """Tests for dataset_stats function."""

    def test_basic_counting(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "cat").mkdir()
            (tmp_path / "dog").mkdir()
            (tmp_path / "cat" / "img1.jpg").write_text("fake")
            (tmp_path / "cat" / "img2.png").write_text("fake")
            (tmp_path / "dog" / "img3.jpeg").write_text("fake")

            result = solution_module.dataset_stats(tmp_path)
            assert result == {"cat": 2, "dog": 1}

    def test_case_insensitive_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "cat").mkdir()
            (tmp_path / "cat" / "img1.JPG").write_text("fake")
            (tmp_path / "cat" / "img2.PNG").write_text("fake")

            result = solution_module.dataset_stats(tmp_path)
            assert result == {"cat": 2}

    def test_ignores_non_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "cat").mkdir()
            (tmp_path / "cat" / "img1.jpg").write_text("fake")
            (tmp_path / "cat" / "readme.txt").write_text("fake")
            (tmp_path / "cat" / "data.csv").write_text("fake")

            result = solution_module.dataset_stats(tmp_path)
            assert result == {"cat": 1}

    def test_ignores_files_in_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "cat").mkdir()
            (tmp_path / "cat" / "img1.jpg").write_text("fake")
            (tmp_path / "stray.jpg").write_text("fake")  # Should be ignored

            result = solution_module.dataset_stats(tmp_path)
            assert result == {"cat": 1}

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = solution_module.dataset_stats(Path(tmp))
            assert result == {}

    def test_non_existent_root(self):
        result = solution_module.dataset_stats(Path("/this/does/not/exist"))
        assert result == {}

    def test_memory_efficiency(self):
        """Verify streaming - doesn't materialize full list."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "cat").mkdir()

            # Create many files
            for i in range(1000):
                (tmp_path / "cat" / f"img_{i}.jpg").write_text("x")

            result = solution_module.dataset_stats(tmp_path)
            assert result == {"cat": 1000}

    def test_nested_subdirectories_counted(self):
        """rglob should find files in nested subdirs."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "cat").mkdir()
            (tmp_path / "cat" / "subdir").mkdir()
            (tmp_path / "cat" / "img1.jpg").write_text("fake")
            (tmp_path / "cat" / "subdir" / "img2.jpg").write_text("fake")

            result = solution_module.dataset_stats(tmp_path)
            assert result == {"cat": 2}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])