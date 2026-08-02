"""
01-core-python — 45: testing with pytest
==========================================
Topics: test discovery, plain assert, pytest.raises,
        @pytest.mark.parametrize, fixtures and scope, tmp_path, monkeypatch,
        unittest.mock (Mock, patch, side_effect), coverage, AAA structure,
        what not to test

Why this matters for AI/backend engineering:
    Testing a chunking function's boundaries; mocking an LLM API so
    tests are free and deterministic; golden-file tests for prompt templates.

Run:      python 45-testing-with-pytest.py
Verify:   python 45-testing-with-pytest.py --verify
Reference: https://docs.pytest.org/
"""

from __future__ import annotations

import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile

# ============================================================
# 1. Test Discovery & Basic Assertions
# ============================================================
# Complexity: O(1) per test

# Example 1: Simple test with plain assert
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

# Example 2: Assertion introspection (pytest shows values on failure)
def test_add_detailed():
    result = add(2, 3)
    assert result == 5, f"Expected 5, got {result}"

# ============================================================
# 2. Exception Testing with pytest.raises
# ============================================================

# Example 3: Testing exceptions
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_by_zero_with_exception_obj():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "zero" in str(exc_info.value).lower()

# ============================================================
# 3. Parametrized Tests
# ============================================================

# Example 4: @pytest.mark.parametrize
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

# Multiple parameters
@pytest.mark.parametrize("a,b,op,expected", [
    (2, 3, "add", 5),
    (5, 3, "sub", 2),
    (4, 5, "mul", 20),
    (10, 2, "div", 5),
])
def test_calculator(a, b, op, expected):
    ops = {"add": lambda x, y: x + y, "sub": lambda x, y: x - y,
           "mul": lambda x, y: x * y, "div": lambda x, y: x / y}
    assert ops[op](a, b) == expected

# ============================================================
# 4. Fixtures
# ============================================================

# Example 5: Basic fixture
@pytest.fixture
def sample_data():
    return {"users": ["alice", "bob"], "count": 2}

def test_fixture_usage(sample_data):
    assert sample_data["count"] == 2
    assert "alice" in sample_data["users"]

# Example 6: Fixture with scope
@pytest.fixture(scope="session")
def expensive_resource():
    """Expensive setup run once per session."""
    print("\n[SETUP] Creating expensive resource...")
    yield {"connection": "db_conn"}
    print("[TEARDOWN] Cleaning up...")

def test_with_session_fixture(expensive_resource):
    assert expensive_resource["connection"] == "db_conn"

# Example 7: Fixture with parameters
@pytest.fixture(params=["small", "medium", "large"])
def dataset_size(request):
    return request.param

def test_dataset_processing(dataset_size):
    assert dataset_size in ["small", "medium", "large"]

# Example 8: tmp_path fixture (built-in)
def test_file_operations(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

# Example 9: monkeypatch fixture (built-in)
def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("MY_VAR", "test_value")
    import os
    assert os.getenv("MY_VAR") == "test_value"
    monkeypatch.delenv("MY_VAR")
    assert os.getenv("MY_VAR") is None

# ============================================================
# 5. unittest.mock
# ============================================================

# Example 10: Mock basics
def test_mock_basics():
    mock = Mock()
    mock.return_value = 42
    assert mock() == 42
    assert mock.call_count == 1
    mock.assert_called_once()

# Example 11: Mock with side_effect
def test_mock_side_effect():
    mock = Mock(side_effect=[1, 2, 3])
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3
    # After exhausted, returns last value
    assert mock() == 3

# Example 12: Mock with exception
def test_mock_exception():
    mock = Mock(side_effect=ValueError("boom"))
    with pytest.raises(ValueError, match="boom"):
        mock()

# Example 13: patch decorator
def external_api_call():
    import requests
    return requests.get("https://api.example.com/data")

@patch("requests.get")
def test_patch_decorator(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    # This would normally call external_api_call()
    # But we're demonstrating the patch
    assert mock_get is not None

# Example 14: patch as context manager
def test_patch_context_manager():
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "test_value"
        import os
        assert os.getenv("MY_VAR") == "test_value"
    # Patch reverted after context

# Example 15: patch.object for methods
class Service:
    def fetch_data(self):
        return "real data"

def test_patch_object():
    service = Service()
    with patch.object(service, "fetch_data", return_value="mocked"):
        assert service.fetch_data() == "mocked"
    assert service.fetch_data() == "real data"

# Example 16: autospec for safer mocks
def test_autospec():
    with patch("os.path.join", autospec=True) as mock_join:
        mock_join.return_value = "/mocked/path"
        import os
        result = os.path.join("a", "b")
        assert result == "/mocked/path"
        # mock_join only accepts args that os.path.join accepts

# ============================================================
# 6. Coverage & What Not to Test
# ============================================================

# Coverage: run with `pytest --cov=my_module`
# 
# What NOT to test:
# - Standard library functions (trust Python)
# - Third-party library internals (trust the library)
# - Getters/setters without logic
# - Private methods (test public API instead)
# - Implementation details that change often
#
# What TO test:
# - Business logic
# - Edge cases (empty, None, boundaries)
# - Error handling
# - Integration points (with mocks)
# - Regression tests for bugs

# ============================================================
# 7. AAA Structure (Arrange, Act, Assert)
# ============================================================

def test_aaa_structure():
    # Arrange
    user_data = {"name": "Alice", "email": "alice@example.com"}
    expected_email = "alice@example.com"
    
    # Act
    result = user_data.get("email")
    
    # Assert
    assert result == expected_email

# ============================================================
# 8. Running Tests
# ============================================================
# 
# Run all: pytest
# Run specific file: pytest test_file.py
# Run specific test: pytest test_file.py::test_name
# Verbose: pytest -v
# Coverage: pytest --cov=my_module
# Parallel: pytest -n auto (pytest-xdist)
# Stop on first failure: pytest -x
# Run failed first: pytest --lf

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: Testing implementation details
#   assert mock.called  # Brittle
# CORRECT:
#   assert result == expected  # Test behavior
#
# MISTAKE: Over-mocking
#   mock everything
# CORRECT:
#   Mock only external dependencies (I/O, network, time)
#
# MISTAKE: Shared mutable state in fixtures
#   @pytest.fixture
#   def data(): return []  # Mutable!
# CORRECT:
#   @pytest.fixture
#   def data(): return []  # Or use scope="function" (default)

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    """Run internal tests."""
    # Test basic functions
    assert add(2, 3) == 5
    assert divide(10, 2) == 5
    
    # Test exceptions
    try:
        divide(1, 0)
        assert False
    except ValueError:
        pass
    
    # Test mock
    m = Mock(return_value=42)
    assert m() == 42
    m.assert_called_once()
    
    # Test patch
    with patch("os.getenv", return_value="test"):
        import os
        assert os.getenv("KEY") == "test"
    
    # Test parametrize logic
    for a, b, expected in [(1, 2, 3), (0, 0, 0), (-1, 1, 0)]:
        assert add(a, b) == expected
    
    print("[OK] 45-testing-with-pytest: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. pytest discovers test_*.py files automatically")
        print("2. Use plain assert — pytest shows values on failure")
        print("3. pytest.raises for exception testing")
        print("4. @pytest.mark.parametrize for multiple test cases")
        print("5. Fixtures for setup/teardown (scope: function/class/module/session)")
        print("6. Mock for isolating units; patch for replacing dependencies")
        print("7. AAA structure: Arrange, Act, Assert")
        print("8. Run with: pytest -v --cov=my_module")
        _verify()