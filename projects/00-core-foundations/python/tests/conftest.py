"""
Test configuration and fixtures for Python Core Foundations tests.
"""

import sys
from pathlib import Path
import pytest

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test configuration
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def examples_dir():
    """Return the examples directory."""
    return PROJECT_ROOT


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "data: marks tests that require data files")
    config.addinivalue_line("markers", "network: marks tests that require network access")
    config.addinivalue_line("markers", "django: marks tests that require Django")
    config.addinivalue_line("markers", "fastapi: marks tests that require FastAPI")
    config.addinivalue_line("markers", "ml: marks tests that require ML libraries")
    config.addinivalue_line("markers", "db: marks tests that require database")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on file location."""
    for item in items:
        # Add markers based on test file location
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)

        # Add markers based on test name patterns
        if "django" in item.name.lower() or "drf" in item.name.lower():
            item.add_marker(pytest.mark.django)
        if "fastapi" in item.name.lower():
            item.add_marker(pytest.mark.fastapi)
        if "ml" in item.name.lower() or "sklearn" in item.name.lower():
            item.add_marker(pytest.mark.ml)
        if (
            "database" in item.name.lower()
            or "db_" in item.name.lower()
            or "mongo" in item.name.lower()
            or "mysql" in item.name.lower()
        ):
            item.add_marker(pytest.mark.db)
