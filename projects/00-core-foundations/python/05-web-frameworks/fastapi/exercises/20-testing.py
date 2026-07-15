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
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import pytest

app = FastAPI(title="Testing Exercises")

# ============================================================
# Sample Application to Test
# ============================================================

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
    items_db[item_id] = item.model_dump()
    return {"id": item_id, **item.model_dump()}

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

@pytest.fixture
def client():
    """Fixture that provides a TestClient with a clean database."""
    items_db.clear()
    return TestClient(app)


@pytest.fixture
def populated_client(client):
    """Client with pre-populated data."""
    client.post("/items", json={"name": "Widget", "price": 9.99, "description": "A widget"})
    client.post("/items", json={"name": "Gadget", "price": 19.99, "description": "A gadget"})
    client.post("/items", json={"name": "Doohickey", "price": 4.99, "description": "A doohickey"})
    return client


def test_create_item_happy_path(client):
    """Test creating an item with valid data."""
    response = client.post("/items", json={
        "name": "Widget",
        "price": 9.99,
        "description": "A useful widget"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget"
    assert data["price"] == 9.99
    assert data["description"] == "A useful widget"
    assert "id" in data


def test_create_item_missing_required_field(client):
    """Test creating an item without a required field returns 422."""
    response = client.post("/items", json={"price": 9.99})
    assert response.status_code == 422


def test_list_items_empty(client):
    """Test listing items when database is empty."""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_get_item_exists(client):
    """Test getting an item that exists."""
    create_resp = client.post("/items", json={"name": "Widget", "price": 9.99})
    item_id = create_resp.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Widget"


def test_get_item_not_found(client):
    """Test getting a non-existent item returns 404."""
    response = client.get("/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_item(client):
    """Test deleting an existing item."""
    create_resp = client.post("/items", json={"name": "Temp", "price": 1.0})
    item_id = create_resp.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}
    # Verify it's gone
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404


# ============================================================
# Exercise 20.2: Testing Pydantic Models
# ============================================================

def test_item_valid_data():
    """Test Item model with all fields provided."""
    item = Item(name="Widget", price=9.99, description="A widget")
    assert item.name == "Widget"
    assert item.price == 9.99
    assert item.description == "A widget"


def test_item_missing_name():
    """Test Item model rejects missing name."""
    with pytest.raises(ValidationError) as exc_info:
        Item(price=9.99)
    assert "name" in str(exc_info.value)


def test_item_missing_price():
    """Test Item model rejects missing price."""
    with pytest.raises(ValidationError) as exc_info:
        Item(name="Test")
    assert "price" in str(exc_info.value)


def test_item_price_string_coercion():
    """Test Item model coerces string price to float."""
    item = Item(name="Test", price="19.99")
    assert item.price == 19.99
    assert isinstance(item.price, float)


def test_item_extra_fields_ignored():
    """Test Item model ignores extra fields."""
    item = Item(name="Test", price=5.0, extra_field="ignored")
    assert item.name == "Test"
    assert not hasattr(item, "extra_field")


def test_item_description_optional():
    """Test Item model defaults description to empty string."""
    item = Item(name="Test", price=5.0)
    assert item.description == ""


# ============================================================
# Exercise 20.3: Testing Error Handling
# ============================================================

def test_404_not_found(client):
    """Test GET for non-existent item returns 404."""
    response = client.get("/items/nonexistent")
    assert response.status_code == 404


def test_422_validation_error(client):
    """Test POST with wrong types returns 422."""
    response = client.post("/items", json={"name": 123, "price": "not-a-number"})
    assert response.status_code == 422


def test_422_missing_body(client):
    """Test POST with no body returns 422."""
    response = client.post("/items", data={}, headers={"Content-Type": "application/json"})
    assert response.status_code == 422


def test_200_empty_list(client):
    """Test GET returns empty list initially."""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_twice_fails(client):
    """Test deleting same item twice returns 404 on the second try."""
    create_resp = client.post("/items", json={"name": "Temp", "price": 1.0})
    item_id = create_resp.json()["id"]
    # First delete
    resp1 = client.delete(f"/items/{item_id}")
    assert resp1.status_code == 200
    # Second delete
    resp2 = client.delete(f"/items/{item_id}")
    assert resp2.status_code == 404


def test_error_response_format(client):
    """Test 404 error response structure."""
    response = client.get("/items/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Item not found"


# ============================================================
# Exercise 20.4: Parameterized Tests
# ============================================================

@pytest.mark.parametrize("name,price,expected_status", [
    ("Widget", 9.99, 201),
    ("Gadget", 19.99, 201),
    ("Doohickey", 4.99, 201),
    ("Thingamajig", 99.99, 201),
    ("", 5.0, 201),  # empty string name is valid (string length > 0)
])
def test_create_various_items(client, name, price, expected_status):
    """Test creating items with various valid names and prices."""
    response = client.post("/items", json={"name": name, "price": price})
    assert response.status_code == expected_status


@pytest.mark.parametrize("name,price", [
    ("Negative Widget", -1.0),
    ("Zero Price", 0.0),
    ("Very Large Price", 999999999.99),
])
def test_create_items_edge_prices(client, name, price):
    """Test creating items with edge case prices."""
    response = client.post("/items", json={"name": name, "price": price})
    assert response.status_code == 201
    assert response.json()["price"] == price


# ============================================================
# Exercise 20.5: Integration Tests with Fixtures
# ============================================================

def test_full_crud_workflow(client):
    """Test complete CRUD lifecycle: create -> read -> list -> delete -> verify."""
    # Create
    resp = client.post("/items", json={"name": "Integration Test", "price": 25.0})
    assert resp.status_code == 201
    item_id = resp.json()["id"]
    assert resp.json()["name"] == "Integration Test"

    # Read
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Integration Test"

    # List
    resp = client.get("/items")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert any(item["id"] == item_id for item in resp.json())

    # Delete
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 200

    # Verify deleted
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404


def test_populated_client_has_items(populated_client):
    """Test that the populated client fixture creates sample items."""
    response = populated_client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
    names = [item["name"] for item in items]
    assert "Widget" in names
    assert "Gadget" in names
    assert "Doohickey" in names


def test_listing_after_multiple_creates(client):
    """Test that listing reflects all created items."""
    for i in range(5):
        client.post("/items", json={"name": f"Item {i}", "price": float(i * 10)})
    response = client.get("/items")
    assert len(response.json()) == 5


def test_default_description_empty_string(client):
    """Test that items without description get empty string default."""
    resp = client.post("/items", json={"name": "No Desc", "price": 5.0})
    assert resp.json()["description"] == ""


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
