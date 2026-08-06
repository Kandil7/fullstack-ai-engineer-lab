# Glossary: Testing Concepts in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Assertion | Statement that verifies a condition in tests | Test, pytest |
| Async Test | Test for asynchronous code | pytest-asyncio, AsyncClient |
| Coverage | Percentage of code executed by tests | pytest-cov, Report |
| Fixtures | Reusable test setup/teardown code | pytest, Setup |
| Integration Test | Tests combining multiple components | Unit Test, E2E |
| Mock | Simulated object for testing | Patch, MagicMock |
| Parameterized | Test with multiple input sets | pytest.mark.parametrize |
| Pytest | Python testing framework | Test, Fixture |
| TestClient | FastAPI client for testing routes | Client, Request |
| Unit Test | Test for individual function/method | Integration Test |
| E2E Test | End-to-end system test | Integration Test |
| Regression Test | Tests preventing new bugs | Test Suite |
| Test Suite | Collection of tests | pytest, Coverage |
| Test Database | Isolated database for testing | Fixture, Cleanup |
| Dependency Override | Replace FastAPI dependencies in tests | Mock, Patch |

---

## Detailed Definitions

### Assertion

**Definition**: A statement that checks if a condition is true. If false, the test fails.

**Code Example**:
```python
def test_user_creation():
    response = client.post("/users/", json={...})
    
    # Basic assertions
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    
    # Assertions with messages
    assert "id" in response.json(), "Response should contain user ID"
    
    # Comparing complex objects
    expected = {"email": "test@example.com", "username": "testuser"}
    assert response.json() == expected
    
    # Checking collections
    assert len(response.json()["items"]) > 0
    
    # Exception testing
    with pytest.raises(HTTPException) as exc_info:
        get_user(user_id=999)
    assert exc_info.value.status_code == 404
```

**Related Terms**: Test, pytest, Fail

---

### Async Test

**Definition**: A test for asynchronous code, using pytest-asyncio to handle async/await.

**Code Example**:
```python
import pytest
import pytest_asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/async-route")
        assert response.status_code == 200

@pytest_asyncio.fixture
async def async_db():
    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_async_database_operation(async_db):
    user = User(username="testuser")
    async_db.add(user)
    await async_db.commit()
    
    result = await async_db.execute(select(User))
    users = result.scalars().all()
    assert len(users) == 1
```

**Related Terms**: pytest-asyncio, AsyncClient, Await

---

### Coverage

**Definition**: The percentage of code executed by tests, measured by coverage tools.

**Code Example**:
```bash
# Install coverage tools
pip install pytest-cov

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Generate HTML report
pytest --cov=app --cov-report=html

# Coverage configuration (.coveragerc)
[run]
source = app
omit = 
    app/tests/*
    app/migrations/*

[report]
fail_under = 80
show_missing = True

# Run with minimum coverage
pytest --cov=app --cov-fail-under=80
```

**Python Coverage Example**:
```python
# app/utils.py
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price"""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount percent")
    return price * (1 - discount_percent / 100)

# test_utils.py
def test_calculate_discount_valid():
    assert calculate_discount(100, 10) == 90.0
    assert calculate_discount(100, 50) == 50.0

def test_calculate_discount_invalid():
    with pytest.raises(ValueError):
        calculate_discount(100, -10)
    with pytest.raises(ValueError):
        calculate_discount(100, 110)
```

**Related Terms**: pytest-cov, Report, Measure

---

### Fixtures

**Definition**: Reusable test setup and teardown functions that provide test data and resources.

**Code Example**:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Simple fixture
@pytest.fixture
def sample_user():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "secret123"
    }

# Fixture with setup and teardown
@pytest.fixture
def db_session():
    # Setup
    engine = create_engine("sqlite:///./test.db")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = Session()
    yield session
    
    # Teardown
    session.close()
    Base.metadata.drop_all(bind=engine)

# Scoped fixtures (shared across tests)
@pytest.fixture(scope="module")
def shared_client():
    """Client shared across all tests in module"""
    with TestClient(app) as client:
        yield client

# Fixture with dependencies
@pytest.fixture
def authenticated_client(client, db_session):
    """Client with authenticated user"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Login and get token
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "secret123"
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client
```

**Related Terms**: pytest, Setup, Teardown

---

### Integration Test

**Definition**: Tests that verify multiple components working together, including database, external services, and multiple endpoints.

**Code Example**:
```python
@pytest.mark.integration
def test_complete_user_registration_flow(client, db):
    """Integration test for user registration workflow"""
    
    # Step 1: Register user
    response = client.post("/users/", json={
        "email": "new@example.com",
        "username": "newuser",
        "password": "SecurePass123!"
    })
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Step 2: Verify email sent
    with patch("app.services.email.send_email") as mock_email:
        client.post(f"/users/{user_id}/verify-email")
        mock_email.assert_called_once()
    
    # Step 3: Login
    response = client.post("/auth/login", data={
        "username": "new@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Step 4: Access protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
```

**Related Terms**: Unit Test, E2E Test, System Test

---

### Mock

**Definition**: A simulated object that replaces real dependencies during testing.

**Code Example**:
```python
from unittest.mock import Mock, patch, AsyncMock, MagicMock

# Basic mock
def test_with_mock():
    mock_service = Mock()
    mock_service.get_user.return_value = {"id": 1, "name": "Test"}
    
    result = mock_service.get_user(1)
    assert result["name"] == "Test"
    mock_service.get_user.assert_called_once()

# Patch decorator
def test_with_patch():
    with patch("app.services.external_api.fetch_data") as mock_fetch:
        mock_fetch.return_value = {"data": "test"}
        
        result = fetch_and_process()
        assert result == "processed"
        mock_fetch.assert_called_once()

# Async mock
@pytest.mark.asyncio
async def test_async_mock():
    with patch("app.services.async_service.process") as mock_process:
        mock_process.return_value = AsyncMock(return_value={"status": "ok"})
        
        result = await async_process()
        assert result["status"] == "ok"

# Mock class
class MockDatabase:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)
        return len(self.users)
    
    def get_user(self, user_id):
        return next((u for u in self.users if u["id"] == user_id), None)

def test_with_mock_database():
    db = MockDatabase()
    db.add_user({"id": 1, "name": "Test"})
    
    user = db.get_user(1)
    assert user["name"] == "Test"
```

**Related Terms**: Patch, MagicMock, Stub

---

### Parameterized

**Definition**: Running the same test with different input values.

**Code Example**:
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double(input, expected):
    assert double(input) == expected

@pytest.mark.parametrize("email", [
    "test@example.com",
    "user.name@domain.co.uk",
    "user+tag@example.com",
])
def test_valid_emails(email):
    assert validate_email(email) is True

@pytest.mark.parametrize("email", [
    "invalid",
    "@example.com",
    "user@",
    "",
])
def test_invalid_emails(email):
    assert validate_email(email) is False

# Multiple parameters
@pytest.mark.parametrize("username,password,expected", [
    ("user1", "Pass123!", True),
    ("user2", "short", False),
    ("", "Pass123!", False),
])
def test_user_creation(username, password, expected):
    result = validate_user(username, password)
    assert result == expected

# Fixture with params
@pytest.fixture(params=["sqlite", "postgresql"])
def database(request):
    if request.param == "sqlite":
        return create_engine("sqlite:///test.db")
    else:
        return create_engine("postgresql://localhost/testdb")
```

**Related Terms**: pytest.mark, Input, Output

---

### Pytest

**Definition**: A Python testing framework that makes it easy to write simple and scalable tests.

**Code Example**:
```python
# Basic test structure
def test_addition():
    assert 1 + 1 == 2

# Test with fixtures
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"

# Test classes (optional)
class TestUser:
    def test_create_user(self):
        user = User("test")
        assert user.name == "test"
    
    def test_user_email(self):
        user = User("test@example.com")
        assert user.email == "test@example.com"

# Markers
@pytest.mark.slow
def test_expensive_operation():
    # This test is marked as slow
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Not supported on Windows"
)
def test_linux_only():
    pass

# Conftest.py for shared fixtures
# conftest.py
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
```

**Related Terms**: Test, Fixture, Marker

---

### TestClient

**Definition**: FastAPI's client for simulating HTTP requests in tests without running a server.

**Code Example**:
```python
from fastapi.testclient import TestClient
from app.main import app

# Create client
client = TestClient(app)

# GET request
def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# POST request
def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser"
        }
    )
    assert response.status_code == 201

# Request with headers
def test_authenticated_request():
    headers = {"Authorization": "Bearer token123"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200

# Request with query params
def test_search_users():
    response = client.get("/users/", params={"search": "test"})
    assert response.status_code == 200

# Request with files
def test_upload_file():
    files = {"file": ("test.txt", b"content", "text/plain")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200

# Async client (for async endpoints)
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/async-route")
        assert response.status_code == 200
```

**Related Terms**: Client, Request, Response

---

### Unit Test

**Definition**: Tests that verify individual functions, methods, or classes in isolation.

**Code Example**:
```python
# Unit test for a utility function
def test_calculate_average():
    from app.utils import calculate_average
    
    assert calculate_average([1, 2, 3]) == 2.0
    assert calculate_average([10]) == 10.0
    assert calculate_average([]) == 0.0

# Unit test for a class
class TestShoppingCart:
    def setup_method(self):
        self.cart = ShoppingCart()
    
    def test_add_item(self):
        self.cart.add_item("apple", 1.0, 2)
        assert len(self.cart.items) == 1
        assert self.cart.total == 2.0
    
    def test_remove_item(self):
        self.cart.add_item("apple", 1.0, 2)
        self.cart.remove_item("apple")
        assert len(self.cart.items) == 0
    
    def test_calculate_total(self):
        self.cart.add_item("apple", 1.0, 2)
        self.cart.add_item("banana", 0.5, 4)
        assert self.cart.calculate_total() == 4.0

# Unit test with mocking
def test_user_registration():
    with patch("app.crud.create_user") as mock_create:
        mock_create.return_value = User(id=1, email="test@example.com")
        
        user = register_user("test@example.com", "password123")
        
        assert user.email == "test@example.com"
        mock_create.assert_called_once()
```

**Related Terms**: Function, Class, Method

---

### Dependency Override

**Definition**: FastAPI's mechanism to replace dependencies during testing.

**Code Example**:
```python
from app.main import app
from app.database import get_db
from app.auth import get_current_user

# Override database dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Override authentication dependency
def override_get_current_user():
    return {"id": 1, "email": "test@example.com", "is_superuser": True}

app.dependency_overrides[get_current_user] = override_get_current_user

# Use in test
def test_admin_endpoint():
    response = client.get("/admin/users")
    assert response.status_code == 200

# Clear overrides after test
app.dependency_overrides.clear()

# Context manager for temporary overrides
@pytest.fixture
def admin_user():
    def override():
        return {"id": 1, "is_superuser": True}
    
    app.dependency_overrides[get_current_user] = override
    yield
    app.dependency_overrides.clear()
```

**Related Terms**: Mock, Patch, Dependency Injection

---

### Regression Test

**Definition**: Tests that verify previously developed software still works after changes.

**Code Example**:
```python
# Regression test for bug fix
def test_user_email_uniqueness():
    """Regression: Bug #123 - Duplicate emails were allowed"""
    client.post("/users/", json={
        "email": "test@example.com",
        "username": "user1"
    })
    
    response = client.post("/users/", json={
        "email": "test@example.com",  # Same email
        "username": "user2"
    })
    
    # Should reject duplicate email
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

# Regression test for data integrity
def test_order_total_calculation():
    """Regression: Bug #456 - Discount not applied correctly"""
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.add_item("item2", 50.0, 2)
    
    total = cart.calculate_total(discount=10)
    
    # Should be (100 + 100) * 0.9 = 180
    assert total == 180.0
```

**Related Terms**: Bug Fix, Verification

---

### Test Suite

**Definition**: A collection of tests organized to test different aspects of the application.

**Code Example**:
```python
# tests/
# ├── __init__.py
# ├── conftest.py          # Shared fixtures
# ├── test_users.py        # User-related tests
# ├── test_products.py     # Product-related tests
# ├── test_orders.py       # Order-related tests
# └── integration/         # Integration tests
#     ├── __init__.py
#     ├── test_user_flow.py
#     └── test_payment.py

# Running the suite
# Run all tests
pytest

# Run specific file
pytest tests/test_users.py

# Run with markers
pytest -m "not slow"

# Run with coverage
pytest --cov=app

# Run in parallel
pytest -n auto

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

**Related Terms**: pytest, Test, Suite

---

## Test Markers

```python
import pytest

# Custom markers
@pytest.mark.slow
def test_expensive_operation():
    pass

@pytest.mark.integration
def test_database_operation():
    pass

@pytest.mark.e2e
def test_full_workflow():
    pass

# Register markers in pytest.ini or pyproject.toml
# [tool.pytest.ini_options]
# markers = [
#     "slow: marks tests as slow",
#     "integration: marks integration tests",
#     "e2e: marks end-to-end tests",
# ]
```

---

## Test Configuration

```python
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]

# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def client(test_session):
    def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

---

## Common Assertions

```python
# Status codes
assert response.status_code == 200
assert response.status_code == 201
assert response.status_code == 400
assert response.status_code == 404
assert response.status_code == 422

# Response body
assert response.json() == {"key": "value"}
assert response.json()["field"] == "expected"
assert "key" in response.json()
assert len(response.json()["items"]) > 0

# Headers
assert response.headers["content-type"] == "application/json"
assert "authorization" in response.headers

# Exceptions
with pytest.raises(HTTPException) as exc_info:
    some_function()
assert exc_info.value.status_code == 404

# Collections
assert item in collection
assert len(collection) == expected_length

# Types
assert isinstance(response.json(), dict)
assert isinstance(response.json()["items"], list)
```

---

## Summary

Understanding testing concepts is crucial for building reliable FastAPI applications. Key takeaways:

1. **Pytest**: Use as your testing framework
2. **Fixtures**: Create reusable test setup
3. **TestClient**: Simulate HTTP requests
4. **Mocks**: Isolate external dependencies
5. **Coverage**: Measure test completeness
6. **Parameterization**: Test multiple inputs
7. **Integration Tests**: Test component interaction
8. **Regression Tests**: Prevent new bugs

**Next**: Move to the async lecture to learn about asynchronous programming patterns.
