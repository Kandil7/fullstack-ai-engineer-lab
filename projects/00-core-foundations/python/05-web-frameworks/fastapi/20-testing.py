"""
20 - Testing
==============
Testing FastAPI applications using TestClient (httpx) and pytest.
Covers: unit tests, integration tests, dependency overriding, and mocking.

Requires: pip install httpx pytest

Run: pytest 20-testing.py -v
"""

import sys
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel


# ----- App setup -----
app = FastAPI(title="Testing Demo")


class ItemCreate(BaseModel):
    name: str
    price: float


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float


# In-memory store
items_db: dict[int, dict] = {}
next_id = 1


def get_db():
    """Database dependency (overridable in tests)."""
    return items_db


@app.get("/")
def root():
    return {"message": "Hello, Testing!"}


@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: dict = Depends(get_db)):
    global next_id
    db[next_id] = {"id": next_id, **item.model_dump()}
    next_id += 1
    return db[next_id - 1]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: dict = Depends(get_db)):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]


@app.get("/items/", response_model=list[ItemResponse])
def list_items(db: dict = Depends(get_db)):
    return list(db.values())


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: dict = Depends(get_db)):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"deleted": True}


# ----- Test Client Setup -----
client = TestClient(app)


# ----- Tests -----
def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Testing!"}


def test_create_item():
    """Test creating an item."""
    response = client.post(
        "/items/",
        json={"name": "Laptop", "price": 999.99},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert "id" in data


def test_create_multiple_items():
    """Test creating multiple items."""
    items = [
        {"name": "Phone", "price": 699.99},
        {"name": "Tablet", "price": 499.99},
    ]
    for item in items:
        response = client.post("/items/", json=item)
        assert response.status_code == 201


def test_get_item():
    """Test getting a specific item."""
    # Create an item first
    create_resp = client.post("/items/", json={"name": "Widget", "price": 9.99})
    item_id = create_resp.json()["id"]

    # Get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Widget"


def test_get_nonexistent_item():
    """Test 404 for nonexistent item."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_list_items():
    """Test listing all items."""
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_delete_item():
    """Test deleting an item."""
    # Create
    create_resp = client.post("/items/", json={"name": "To Delete", "price": 1.0})
    item_id = create_resp.json()["id"]

    # Delete
    delete_resp = client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["deleted"] is True

    # Verify it's gone
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_item():
    """Test deleting nonexistent item returns 404."""
    response = client.delete("/items/99999")
    assert response.status_code == 404


def test_create_item_validation():
    """Test validation: missing required field."""
    response = client.post("/items/", json={"name": "Incomplete"})
    assert response.status_code == 422  # Validation error


def test_create_item_wrong_type():
    """Test validation: wrong type for price."""
    response = client.post("/items/", json={"name": "Test", "price": "not-a-number"})
    assert response.status_code == 422


# ----- Parameterized tests -----
import pytest


@pytest.mark.parametrize("name,price", [
    ("Laptop", 999.99),
    ("Phone", 699.99),
    ("Tablet", 499.99),
    ("Watch", 299.99),
])
def test_create_various_items(name, price):
    """Parameterized test for creating different items."""
    response = client.post("/items/", json={"name": name, "price": price})
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["price"] == price


# ----- Dependency override for testing -----
test_db = {}


def override_get_db():
    """Override dependency for testing with isolated DB."""
    return test_db


app.dependency_overrides[get_db] = override_get_db


def test_with_overridden_dependency():
    """Test using dependency override for isolation."""
    test_db.clear()
    response = client.post("/items/", json={"name": "Override Test", "price": 42.0})
    assert response.status_code == 201
    assert "Override Test" in str(test_db.values())


"""
Testing with pytest:
    pytest 20-testing.py -v
    pytest 20-testing.py -v -k "test_create"
    pytest 20-testing.py --tb=short

    Run directly:
    python 20-testing.py
"""

def _verify():
    """Run the smoke tests in-process with the module-level TestClient."""
    try:
        from fastapi.testclient import TestClient  # noqa: F401 (already imported above)
    except ImportError:
        print("[skip] fastapi not installed")
        return

    test_root()
    test_create_item()
    test_get_item()
    test_list_items()
    test_delete_item()
    test_get_nonexistent_item()
    test_create_item_validation()
    test_create_item_wrong_type()
    test_with_overridden_dependency()
    print("[OK] 20-testing: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
