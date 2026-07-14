# Lecture 20: Testing FastAPI Applications

## Overview

Testing is a critical part of building reliable FastAPI applications. This lecture covers comprehensive testing strategies, including unit tests, integration tests, end-to-end tests, and testing with databases. You'll learn how to use pytest, TestClient, and mock external dependencies effectively.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write unit tests for FastAPI route handlers
2. Use pytest fixtures for test setup and teardown
3. Test database operations with isolated test databases
4. Mock external dependencies and services
5. Write integration tests for complete workflows
6. Use async testing with pytest-asyncio
7. Implement test coverage reporting
8. Follow testing best practices

---

## Key Concepts

### 1. Testing Pyramid

```
        /\
       /  \        E2E Tests (Few)
      /    \       - Full system tests
     /------\      - Slow, expensive
    /        \     Integration Tests (Some)
   /          \    - Component interaction
  /------------\   - Database, APIs
 /              \  Unit Tests (Many)
/                \ - Individual functions
----------------   - Fast, isolated
```

### 2. Test Configuration

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.database import get_db, Base

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create test tables
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
```

---

## Code Examples

### Example 1: Basic Route Testing

```python
# test_routes.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_create_user_invalid_email():
    response = client.post(
        "/users/",
        json={
            "email": "invalid-email",
            "username": "testuser",
            "password": "secret123"
        }
    )
    assert response.status_code == 422  # Validation error

def test_read_user():
    # First create a user
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123"
        }
    )
    user_id = response.json()["id"]
    
    # Then read it
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_read_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
```

### Example 2: Database Testing with Fixtures

```python
# test_database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
from app import models, crud, schemas
from app.main import app
from fastapi.testclient import TestClient

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_create_and_read_user(client, db_session):
    # Create user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "secret123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    
    # Verify in database
    user_id = response.json()["id"]
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    assert db_user is not None
    assert db_user.email == "test@example.com"

def test_database_rollback_on_error(client, db_session):
    # Try to create duplicate user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "secret123"
    }
    
    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)
    
    # Second request should fail
    assert response.status_code == 400
    
    # Verify only one user exists
    count = db_session.query(models.User).count()
    assert count == 1
```

### Example 3: Async Testing

```python
# test_async.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import get_async_db, Base

# Async test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_async.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True
)

async_test_session = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest_asyncio.fixture
async def setup_database():
    """Create test tables"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client(setup_database):
    """Create async test client"""
    async def override_get_async_db():
        async with async_test_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    app.dependency_overrides[get_async_db] = override_get_async_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_async_create_user(async_client):
    response = await async_client.post(
        "/users/",
        json={
            "email": "async@example.com",
            "username": "asyncuser",
            "password": "secret123"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "async@example.com"

@pytest.mark.asyncio
async def test_async_read_users(async_client):
    # Create multiple users
    for i in range(3):
        await async_client.post(
            "/users/",
            json={
                "email": f"user{i}@example.com",
                "username": f"user{i}",
                "password": "secret123"
            }
        )
    
    # Read all users
    response = await async_client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 3
```

### Example 4: Mocking External Services

```python
# test_with_mocks.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.email import send_email
from app.services.payment import process_payment

def test_send_welcome_email():
    with patch("app.services.email.send_email") as mock_send:
        mock_send.return_value = {"status": "sent"}
        
        result = send_email(
            to="user@example.com",
            subject="Welcome!",
            body="Welcome to our platform!"
        )
        
        assert result["status"] == "sent"
        mock_send.assert_called_once()

@pytest.mark.asyncio
async def test_process_payment_success():
    with patch("app.services.payment.process_payment") as mock_payment:
        mock_payment.return_value = {
            "status": "success",
            "transaction_id": "txn_123"
        }
        
        result = await process_payment(
            amount=99.99,
            currency="USD",
            card_token="tok_visa"
        )
        
        assert result["status"] == "success"
        assert result["transaction_id"] == "txn_123"

def test_payment_failure_handling():
    with patch("app.services.payment.process_payment") as mock_payment:
        mock_payment.side_effect = Exception("Payment gateway error")
        
        with pytest.raises(Exception) as exc_info:
            process_payment(amount=99.99)
        
        assert "Payment gateway error" in str(exc_info.value)

# Mocking FastAPI dependencies
def test_with_mocked_auth():
    def override_get_current_user():
        return {"id": 1, "email": "mock@example.com", "is_superuser": True}
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    response = client.get("/admin/users")
    assert response.status_code == 200
    
    app.dependency_overrides.clear()
```

### Example 5: Parameterized Testing

```python
# test_parameterized.py
import pytest

@pytest.mark.parametrize("email,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("@example.com", False),
    ("user@", False),
    ("user.name@example.com", True),
    ("user+tag@example.com", True),
])
def test_validate_email(email, expected):
    from app.utils import validate_email
    assert validate_email(email) == expected

@pytest.mark.parametrize("password,expected", [
    ("short", False),
    ("alllowercase123", False),
    ("ALLUPPERCASE123", False),
    ("NoNumbers!", False),
    ("NoSpecialChars123", False),
    ("ValidPass123!", True),
    ("AnotherValid@456", True),
])
def test_validate_password_strength(password, expected):
    from app.utils import validate_password_strength
    assert validate_password_strength(password) == expected

@pytest.mark.parametrize("age", [
    -1,
    0,
    150,
    151,
])
def test_invalid_age(age):
    with pytest.raises(ValueError):
        create_user(age=age)

# Fixture with parameters
@pytest.fixture(params=["sqlite", "postgresql"])
def db_engine(request):
    if request.param == "sqlite":
        return create_engine("sqlite:///./test.db")
    else:
        return create_engine("postgresql://test:test@localhost/testdb")

def test_with_multiple_databases(db_engine):
    # Test runs twice - once for each database
    Base.metadata.create_all(bind=db_engine)
    # ... test code
    Base.metadata.drop_all(bind=db_engine)
```

### Example 6: Integration Tests

```python
# test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Integration test with real database
INTEGRATION_DATABASE_URL = "postgresql://test:test@localhost/testdb"

integration_engine = create_engine(INTEGRATION_DATABASE_URL)
IntegrationSession = sessionmaker(bind=integration_engine)

@pytest.fixture(scope="module")
def integration_client():
    """Integration test client"""
    Base.metadata.create_all(bind=integration_engine)
    
    def override_get_db():
        db = IntegrationSession()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=integration_engine)

def test_complete_user_workflow(integration_client):
    """Test complete user registration and profile update"""
    
    # 1. Register user
    response = integration_client.post(
        "/users/",
        json={
            "email": "integration@example.com",
            "username": "integrationuser",
            "password": "securepass123"
        }
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # 2. Login
    response = integration_client.post(
        "/auth/login",
        data={
            "username": "integration@example.com",
            "password": "securepass123"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # 3. Update profile with auth
    headers = {"Authorization": f"Bearer {token}"}
    response = integration_client.put(
        f"/users/{user_id}/profile",
        headers=headers,
        json={"bio": "Integration test user"}
    )
    assert response.status_code == 200
    
    # 4. Verify update
    response = integration_client.get(
        f"/users/{user_id}",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["profile"]["bio"] == "Integration test user"
```

---

## Common Mistakes to Avoid

### 1. Not Isolating Tests

```python
# BAD: Tests depend on each other
def test_create_user():
    response = client.post("/users/", json={...})
    assert response.status_code == 201

def test_read_user():
    # This depends on test_create_user running first!
    response = client.get("/users/1")
    assert response.status_code == 200

# GOOD: Each test is independent
def test_read_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
```

### 2. Not Cleaning Up Database

```python
# BAD: Database state leaks between tests
@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    # No cleanup!

# GOOD: Proper cleanup
@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
```

### 3. Testing Implementation Details

```python
# BAD: Testing internal implementation
def test_user_creation_implementation():
    with patch("app.crud.create_user") as mock_create:
        mock_create.return_value = {"id": 1}
        response = client.post("/users/", json={...})
        mock_create.assert_called_once()  # Implementation detail

# GOOD: Testing behavior
def test_user_creation_success():
    response = client.post("/users/", json={...})
    assert response.status_code == 201
    assert "id" in response.json()
```

---

## Best Practices

1. **Use Fixtures**: Set up test data consistently
2. **Isolate Tests**: Each test should be independent
3. **Clean Up**: Always clean database after tests
4. **Mock External Services**: Don't call real APIs in tests
5. **Test Edge Cases**: Include error scenarios
6. **Use Parameterized Tests**: Test multiple inputs
7. **Keep Tests Fast**: Slow tests discourage running
8. **Test Behavior, Not Implementation**: Focus on what, not how
9. **Use Meaningful Names**: Descriptive test function names
10. **Maintain Test Coverage**: Aim for 80%+ coverage

---

## Test Coverage

```bash
# Install pytest-cov
pip install pytest-cov

# Run with coverage
pytest --cov=app --cov-report=html

# Coverage report
# - Name                    Stmts   Miss  Cover
# ------------------------------------------------
# app/__init__.py               2      0   100%
# app/main.py                  45      5    89%
# app/routes/users.py          60     10    83%
# app/crud.py                  40      3    93%
# ------------------------------------------------
# TOTAL                       147     18    88%
```

---

## Practice Exercises

### Exercise 1: Unit Tests
Write unit tests for a user registration endpoint:
- Test successful registration
- Test duplicate email handling
- Test invalid input validation
- Test password hashing

### Exercise 2: Database Tests
Create tests for a blog application:
- Test creating posts with tags
- Test querying posts by author
- Test deleting posts with cascading comments
- Test database transactions

### Exercise 3: Integration Tests
Write integration tests for an e-commerce workflow:
- User registration and login
- Adding items to cart
- Checkout process
- Order confirmation email

---

## Summary

- Testing is essential for reliable applications
- Use pytest fixtures for consistent test setup
- Isolate tests to prevent interference
- Mock external services for speed
- Test both success and error scenarios
- Maintain good test coverage
- Use async testing for async endpoints

**Next Lecture**: We'll explore async patterns in FastAPI for building high-performance applications.
