"""
Exercise 20: Testing FastAPI Applications

Master testing strategies for FastAPI apps.
Topics: unit tests, integration tests, test clients, fixtures, mocking, coverage.

Prerequisites:
- pytest basics
- FastAPI routing (exercise 01-04)
- HTTP methods and status codes

Estimated time: 60-80 minutes
"""

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import List
import pytest
import json

app = FastAPI(title="Testing Exercises")

# ============================================================
# Sample Application to Test
# ============================================================
# This is the application you'll write tests for

items_db: dict = {}

class Item(BaseModel):
    name: str
    price: float
    description: str = ""

class ItemResponse(Item):
    id: str

@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    item_id = str(len(items_db) + 1)
    items_db[item_id] = item.dict()
    return {"id": item_id, **item.dict()}

@app.get("/items", response_model=List[ItemResponse])
async def list_items():
    return [{"id": k, **v} for k, v in items_db.items()]

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id]}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}


# ============================================================
# Exercise 20.1: Basic Test Setup
# ============================================================
"""
Problem:
    Set up a basic testing infrastructure for the FastAPI app above.

Requirements:
    1. Create a pytest fixture that provides a TestClient
    2. Create a fixture that clears the database before each test
    3. Write tests for each endpoint:
       - test_create_item (happy path)
       - test_create_item_invalid_data (missing required field)
       - test_list_items_empty
       - test_get_item_exists
       - test_get_item_not_found
       - test_delete_item

Hints:
    - Use @pytest.fixture for fixtures
    - Use TestClient(app) as the test client
    - Use client.post("/items", json={...}) for POST requests
    - Use client.get("/items") for GET requests
    - Use client.delete("/items/1") for DELETE requests
    - Assert status codes: assert response.status_code == 201
    - Assert response body: assert response.json()["name"] == "Widget"

Fixture skeleton:
    @pytest.fixture
    def client():
        items_db.clear()
        return TestClient(app)

Test case skeleton:
    def test_create_item(client):
        response = client.post("/items", json={
            "name": "Widget",
            "price": 9.99,
            "description": "A useful widget"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Widget"
        assert data["price"] == 9.99
        assert "id" in data
"""

# TODO: Write your tests below


# ============================================================
# Exercise 20.2: Testing Pydantic Models
# ============================================================
"""
Problem:
    Write tests that verify Pydantic model validation.

Test cases to implement:
    1. test_item_valid_data - All fields provided
    2. test_item_missing_name - Name is required
    3. test_item_missing_price - Price is required
    4. test_item_price_string_auto_coerce - "9.99" -> 9.99
    5. test_item_extra_fields_ignored - Extra fields are dropped
    6. test_item_description_optional - Description defaults to ""

Hints:
    - Use Item(**data) to test model creation directly
    - Use pytest.raises(ValidationError) for expected failures
    - from pydantic import ValidationError
    - Model validation happens at instantiation, not in the endpoint

Test case skeleton:
    def test_item_valid_data():
        item = Item(name="Widget", price=9.99, description="A widget")
        assert item.name == "Widget"
        assert item.price == 9.99

    def test_item_missing_name():
        with pytest.raises(ValidationError) as exc_info:
            Item(price=9.99)
        assert "name" in str(exc_info.value)

    def test_item_price_string_coercion():
        item = Item(name="Test", price="19.99")
        assert item.price == 19.99
        assert isinstance(item.price, float)
"""

# TODO: Write your tests below


# ============================================================
# Exercise 20.3: Testing Error Handling
# ============================================================
"""
Problem:
    Test various error scenarios thoroughly.

Test cases:
    1. test_404_not_found - GET /items/nonexistent returns 404
    2. test_422_validation_error - POST /items with wrong types
    3. test_422_missing_body - POST /items with no body
    4. test_200_empty_list - GET /items returns [] initially
    5. test_delete_twice_fails - Delete same item twice
    6. test_error_response_format - Verify error JSON structure

Hints:
    - Client methods raise for status by default, use client.get(..., allow_redirects=True) or handle
    - Actually, TestClient doesn't raise by default - response.status_code works
    - Validation errors return 422 with detail: [{loc, msg, type}]
    - 404 errors return {"detail": "Item not found"}
    - Test the response.json() structure for errors

Expected error formats:
    404: {"detail": "Item not found"}
    422: {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}
"""

# TODO: Write your tests below


# ============================================================
# Exercise 20.4: Parameterized Tests
# ============================================================
"""
Problem:
    Use pytest parametrize to test multiple scenarios efficiently.

Tasks:
    1. Test creating items with various valid names
    2. Test that price validation rejects negative values
    3. Test listing items after creating N items

Parameterized examples:
    @pytest.mark.parametrize("name,price", [
        ("Widget", 9.99),
        ("Gadget", 19.99),
        ("Doohickey", 4.99),
        ("Thingamajig", 99.99),
    ])
    def test_create_various_items(client, name, price):
        response = client.post("/items", json={"name": name, "price": price})
        assert response.status_code == 201
        assert response.json()["name"] == name
        assert response.json()["price"] == price

    @pytest.mark.parametrize("invalid_price", [-1, -0.01, -100])
    def test_negative_prices_rejected(client, invalid_price):
        response = client.post("/items", json={
            "name": "Bad Item",
            "price": invalid_price
        })
        assert response.status_code in [400, 422]

Hints:
    - @pytest.mark.parametrize("var_name", [val1, val2, ...])
    - Multiple params: @pytest.mark.parametrize("a,b", [(1,2), (3,4)])
    - You may need to modify the Item model to reject negative prices first
"""

# TODO: Write your tests below


# ============================================================
# Exercise 20.5: Integration Tests with Fixtures
# ============================================================
"""
Problem:
    Build a comprehensive test suite using pytest fixtures and markers.

Requirements:
    1. Create fixtures for:
       - Fresh client (cleared DB)
       - Pre-populated DB with sample items
       - Auth token (mock)
    2. Use pytest markers to categorize tests
    3. Test complete user workflows (create -> read -> update -> delete)
    4. Test concurrent operations (bonus)

Fixture examples:
    @pytest.fixture
    def populated_client(client):
        """Client with pre-populated data"""
        client.post("/items", json={"name": "Widget", "price": 9.99})
        client.post("/items", json={"name": "Gadget", "price": 19.99})
        return client

    @pytest.fixture
    def auth_headers():
        """Mock authentication headers"""
        token = "test-token-12345"
        return {"Authorization": f"Bearer {token}"}

Marker usage:
    @pytest.mark.slow
    def test_complex_workflow(populated_client):
        ...

    @pytest.mark.integration
    def test_full_crud_cycle(client):
        ...

Workflow test:
    def test_full_crud_workflow(client):
        # Create
        resp = client.post("/items", json={"name": "Test", "price": 5.0})
        assert resp.status_code == 201
        item_id = resp.json()["id"]

        # Read
        resp = client.get(f"/items/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Test"

        # List (should contain our item)
        resp = client.get("/items")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # Delete
        resp = client.delete(f"/items/{item_id}")
        assert resp.status_code == 200

        # Verify deleted
        resp = client.get(f"/items/{item_id}")
        assert resp.status_code == 404
"""

# TODO: Write your tests below


# ============================================================
# Running Tests
# ============================================================
"""
To run your tests:
    cd projects/00-core-foundations/python/fastapi/exercises
    pytest 20-testing.py -v

Useful pytest commands:
    pytest -v                    # Verbose output
    pytest -k "test_create"      # Run tests matching pattern
    pytest -x                    # Stop on first failure
    pytest --tb=short            # Shorter tracebacks
    pytest -m "not slow"         # Skip slow tests
    pytest --cov=.               # Coverage report (pip install pytest-cov)

Coverage targets:
    - Aim for >80% line coverage
    - Focus on endpoint logic and error paths
    - Don't test third-party library internals
"""
