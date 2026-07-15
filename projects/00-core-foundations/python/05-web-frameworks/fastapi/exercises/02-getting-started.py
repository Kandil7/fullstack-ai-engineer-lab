"""
FastAPI Exercise 02 - Getting Started with FastAPI
===================================================

Topics covered:
- CRUD operations with HTTP methods
- Status codes for different scenarios
- Request/Response cycle understanding

Requirements:
    pip install fastapi uvicorn

Run:
    uvicorn 02-getting-started:app --reload
"""

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="CRUD Exercise")

# In-memory data store
items_db: dict[int, dict] = {}


# =============================================================================
# Exercise 1: Basic CRUD Operations
# =============================================================================
# Implement a simple item management API:
#   GET    /items       -> List all items
#   POST   /items       -> Create a new item
#   PUT    /items/{id}  -> Update an existing item
#   DELETE /items/{id}  -> Delete an item
#
# Hints:
#   - Use @app.get, @app.post, @app.put, @app.delete decorators
#   - POST typically returns status 201
#   - DELETE typically returns status 204 (no content)
#   - Use a simple auto-incrementing ID counter
# =============================================================================

next_id = 1


@app.get("/items")
def list_items():
    """Return all items with count."""
    return {"items": list(items_db.values()), "count": len(items_db)}


@app.post("/items", status_code=201)
def create_item(item: dict):
    """Create a new item and return it with its assigned ID."""
    global next_id
    item_id = next_id
    next_id += 1
    items_db[item_id] = {"id": item_id, **item}
    return {"created": True, "id": item_id, "item": items_db[item_id]}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    """Update an existing item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = {"id": item_id, **item}
    return {"updated": True, "id": item_id, "item": items_db[item_id]}


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Delete an item by ID. Returns no content."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]


# =============================================================================
# Exercise 2: Status Code Practice
# =============================================================================
# Create endpoints that demonstrate different HTTP status codes:
#   GET /status/200  -> {"status": "ok"}            (OK)
#   GET /status/201  -> {"status": "created"}        (Created)
#   GET /status/204  -> no body                      (No Content)
#   GET /status/404  -> {"error": "resource not found"}  (Not Found)
#   GET /status/403  -> {"error": "access denied"}       (Forbidden)
#   GET /status/500  -> {"error": "internal server error"} (Server Error)
#
# Hints:
#   - Use status_code parameter in the decorator or return Response directly
#   - 204 responses should have no body
#   - 4xx and 5xx errors should raise HTTPException
# =============================================================================


@app.get("/status/200")
def status_ok():
    """Return 200 OK with a status message."""
    return {"status": "ok"}


@app.get("/status/201", status_code=201)
def status_created():
    """Return 201 Created with a status message."""
    return {"status": "created"}


@app.get("/status/204", status_code=204)
def status_no_content():
    """Return 204 No Content with empty body."""
    return None  # FastAPI will send empty body for 204


@app.get("/status/404")
def status_not_found():
    """Return 404 Not Found."""
    raise HTTPException(status_code=404, detail={"error": "resource not found"})


@app.get("/status/403")
def status_forbidden():
    """Return 403 Forbidden."""
    raise HTTPException(status_code=403, detail={"error": "access denied"})


@app.get("/status/500")
def status_server_error():
    """Return 500 Internal Server Error."""
    raise HTTPException(status_code=500, detail={"error": "internal server error"})


# =============================================================================
# Exercise 3: Request Inspection
# =============================================================================
# Create an endpoint that inspects and returns request details:
#   GET /inspect?name=John&age=30  -> {
#       "method": "GET",
#       "path": "/inspect",
#       "headers": {...},
#       "query_params": {"name": "John", "age": "30"}
#   }
#   POST /inspect with body {"name": "John", "age": 30} -> {
#       "method": "POST",
#       "path": "/inspect",
#       "headers": {...},
#       "body": {"name": "John", "age": 30}
#   }
#
# Hints:
#   - Use the Request object from Starlette (FastAPI's underlying framework)
#   - Import: from starlette.requests import Request
#   - Access request.method, request.url.path, request.headers
#   - Use await request.json() for POST body
# =============================================================================

@app.api_route("/inspect", methods=["GET", "POST"])
async def inspect_request(request: Request):
    """Inspect and return details about the incoming request."""
    info = {
        "method": request.method,
        "path": request.url.path,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
    }
    if request.method == "POST":
        try:
            body = await request.json()
            info["body"] = body
        except Exception:
            info["body"] = None
    return info


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# 1. Run: uvicorn 02-getting-started:app --reload
# 2. Test CRUD: POST /items, GET /items, PUT /items/1, DELETE /items/1
# 3. Test all /status/* endpoints
# 4. Test the /inspect endpoint with GET and POST
# =============================================================================
