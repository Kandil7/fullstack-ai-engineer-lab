"""
FastAPI Exercise 02 - Getting Started
======================================

Topics covered:
- HTTP methods (GET, POST, PUT, DELETE)
- Response status codes
- Request and Response objects
- Running with uvicorn

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 02-getting-started:app1 --reload
    uvicorn 02-getting-started:app2 --reload
    uvicorn 02-getting-started:app3 --reload
"""

from fastapi import FastAPI, Response, status


# =============================================================================
# Exercise 1: HTTP Methods
# =============================================================================
# Create an app with CRUD-style routes for "items":
#   GET    /items        -> {"items": [], "count": 0}
#   POST   /items        -> status 201, body: {"created": true}
#   PUT    /items/{id}   -> {"updated": true, "id": <id>}
#   DELETE /items/{id}   -> {"deleted": true, "id": <id>}
#
# Hints:
#   - Use @app.post(), @app.put(), @app.delete() decorators
#   - For POST, return status_code=201 (Created)
#   - For PUT/DELETE, use path parameter {id}
#   - You can return status code via Response(status_code=...) or
#     by returning a tuple: (dict, status_code)
#
# Expected behavior:
#   GET  /items       -> 200, {"items": [], "count": 0}
#   POST /items       -> 201, {"created": true}
#   PUT  /items/42    -> 200, {"updated": true, "id": 42}
#   DELETE /items/42  -> 200, {"deleted": true, "id": 42}
#
# Test with:
#   curl -X GET http://localhost:8000/items
#   curl -X POST http://localhost:8000/items
#   curl -X PUT http://localhost:8000/items/42
#   curl -X DELETE http://localhost:8000/items/42
# =============================================================================

app1 = FastAPI(title="Exercise 2.1 - HTTP Methods")


@app1.get("/items")
def list_items():
    pass  # TODO: Return {"items": [], "count": 0}


@app1.post("/items", status_code=201)
def create_item():
    pass  # TODO: Return {"created": true}


@app1.put("/items/{item_id}")
def update_item(item_id: int):
    pass  # TODO: Return {"updated": true, "id": item_id}


@app1.delete("/items/{item_id}")
def delete_item(item_id: int):
    pass  # TODO: Return {"deleted": true, "id": item_id}


# =============================================================================
# Exercise 2: Custom Status Codes
# =============================================================================
# Create an app that demonstrates various HTTP status codes:
#   GET /ok           -> 200 with {"status": "ok"}
#   GET /created      -> 201 with {"status": "created"}
#   GET /no-content   -> 204 with NO body
#   GET /not-found    -> 404 with {"error": "resource not found"}
#   GET /forbidden    -> 403 with {"error": "access denied"}
#   GET /server-error -> 500 with {"error": "internal server error"}
#
# Hints:
#   - Use Response(status_code=204) for no content
#   - For error codes, return dict + status_code as tuple
#   - You can also use: from fastapi.responses import JSONResponse
#
# Expected behavior:
#   GET /ok           -> 200, {"status": "ok"}
#   GET /created      -> 201, {"status": "created"}
#   GET /no-content   -> 204, (empty body)
#   GET /not-found    -> 404, {"error": "resource not found"}
#   GET /forbidden    -> 403, {"error": "access denied"}
#   GET /server-error -> 500, {"error": "internal server error"}
#
# Test with:
#   curl -i http://localhost:8000/ok
#   curl -i http://localhost:8000/no-content
#   curl -i http://localhost:8000/not-found
# =============================================================================

app2 = FastAPI(title="Exercise 2.2 - Status Codes")


@app2.get("/ok")
def get_ok():
    pass  # TODO: Return 200 with {"status": "ok"}


@app2.get("/created")
def get_created():
    pass  # TODO: Return 201 with {"status": "created"}


@app2.get("/no-content")
def get_no_content(response: Response):
    pass  # TODO: Return 204 with empty body
    # Hint: Use response.status_code = 204 and return Response(status_code=204)


@app2.get("/not-found")
def get_not_found():
    pass  # TODO: Return 404 with {"error": "resource not found"}


@app2.get("/forbidden")
def get_forbidden():
    pass  # TODO: Return 403 with {"error": "access denied"}


@app2.get("/server-error")
def get_server_error():
    pass  # TODO: Return 500 with {"error": "internal server error"}


# =============================================================================
# Exercise 3: Reading Request Details
# =============================================================================
# Create an app that reads and returns request information:
#   GET /request-info  -> returns a dict with:
#     {
#       "method": <HTTP method>,
#       "path": <request path>,
#       "headers": {"host": ..., "user-agent": ...},
#       "query_params": <dict of query params>
#     }
#
#   GET /echo?name=<name>&age=<age> -> returns:
#     {"name": <name>, "age": <age>}
#
# Hints:
#   - Use from starlette.requests import Request
#   - request.method, request.url.path, request.headers, request.query_params
#   - For /echo, use Query parameters (covered more in exercise 04)
#   - For query params: name: str = Query(default=...)
#
# Expected behavior:
#   GET /request-info -> 200 with request details dict
#   GET /echo?name=alice&age=30 -> 200, {"name": "alice", "age": "30"}
#
# Test with:
#   curl http://localhost:8000/request-info
#   curl "http://localhost:8000/echo?name=alice&age=30"
# =============================================================================

from fastapi import Query
from starlette.requests import Request

app3 = FastAPI(title="Exercise 2.3 - Request Details")


@app3.get("/request-info")
async def request_info(request: Request):
    pass  # TODO: Return request method, path, headers, and query params


@app3.get("/echo")
async def echo(name: str = Query(default=""), age: str = Query(default="")):
    pass  # TODO: Return {"name": name, "age": age}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 02-getting-started:app1 --reload
#    - Test GET /items (should return empty list)
#    - Test POST /items (should return 201)
#    - Test PUT /items/42 (should return id: 42)
#    - Test DELETE /items/42 (should return id: 42)
#
# 2. Run: uvicorn 02-getting-started:app2 --reload
#    - Test all status code endpoints
#    - Verify /no-content returns 204 with empty body
#
# 3. Run: uvicorn 02-getting-started:app3 --reload
#    - Verify /request-info returns request details
#    - Verify /echo echoes back query params
# =============================================================================
