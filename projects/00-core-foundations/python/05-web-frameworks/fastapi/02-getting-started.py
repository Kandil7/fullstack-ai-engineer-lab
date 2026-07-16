"""
02 - Getting Started with FastAPI
===================================
This lesson covers FastAPI path operations, response types,
and basic request handling patterns.

Run: uvicorn 02-getting-started:app --reload
"""

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Getting Started with FastAPI")


# ----- Pydantic Model for structured data -----
class Item(BaseModel):
    """Pydantic model for automatic validation and serialization."""
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


# In-memory database
fake_items_db: list[dict] = [
    {"id": 1, "name": "Laptop", "price": 999.99, "description": "A powerful laptop"},
    {"id": 2, "name": "Phone", "price": 699.99, "description": "A modern smartphone"},
    {"id": 3, "name": "Tablet", "price": 499.99, "description": "A lightweight tablet"},
]


# ----- Basic GET -----
@app.get("/")
def root():
    """Basic root endpoint."""
    return {
        "message": "FastAPI Getting Started",
        "tips": [
            "Use /docs for interactive API documentation",
            "Use /redoc for alternative documentation",
            "Type hints give you auto-validation",
        ],
    }


# ----- GET with path parameter -----
@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Retrieve a single item by ID. FastAPI auto-converts item_id to int."""
    if item_id < 1 or item_id > len(fake_items_db):
        return {"error": "Item not found"}
    return fake_items_db[item_id - 1]


# ----- GET with query parameters -----
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """
    Query parameters with defaults.
    /items/?skip=0&limit=2
    """
    return fake_items_db[skip : skip + limit]


# ----- POST with Pydantic model -----
@app.post("/items/")
def create_item(item: Item) -> dict:
    """
    Create a new item. FastAPI automatically:
    1. Reads the request body as JSON
    2. Validates against the Item schema
    3. Converts to a Python dict
    4. Returns the response
    """
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    # Assign a new ID
    item_dict["id"] = len(fake_items_db) + 1
    fake_items_db.append(item_dict)
    return item_dict


# ----- PUT for updates -----
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item."""
    if item_id < 1 or item_id > len(fake_items_db):
        return {"error": "Item not found"}
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    fake_items_db[item_id - 1] = item_dict
    return item_dict


# ----- DELETE -----
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id < 1 or item_id > len(fake_items_db):
        return {"error": "Item not found"}
    deleted = fake_items_db.pop(item_id - 1)
    return {"deleted": deleted, "remaining": len(fake_items_db)}


# ----- Multiple response status codes -----
@app.post("/items/multi-status/", status_code=201)
def create_item_status(item: Item):
    """POST returning 201 Created status code."""
    item_dict = item.model_dump()
    item_dict["id"] = len(fake_items_db) + 1
    fake_items_db.append(item_dict)
    return item_dict


# ----- Response with metadata -----
@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Demonstrates returning simple status info.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


"""
Testing with curl:
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/items/1
    curl http://127.0.0.1:8000/items/?skip=0&limit=2
    curl -X POST http://127.0.0.1:8000/items/ -H "Content-Type: application/json" -d '{"name": "Monitor", "price": 399.99}'
    curl -X PUT http://127.0.0.1:8000/items/1 -H "Content-Type: application/json" -d '{"name": "Gaming Laptop", "price": 1299.99}'
    curl -X DELETE http://127.0.0.1:8000/items/2
    curl http://127.0.0.1:8000/health
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
