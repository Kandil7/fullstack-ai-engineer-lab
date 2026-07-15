"""
FastAPI Exercise 04 - Query Parameters
=======================================

Topics covered:
- Defining query parameters
- Default values and optional parameters
- Query validation (min_length, max_length, regex, etc.)
- Multiple values and aliasing

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 04-query-parameters:app1 --reload
    uvicorn 04-query-parameters:app2 --reload
    uvicorn 04-query-parameters:app3 --reload
"""

from fastapi import FastAPI, Query
from typing import Optional


# =============================================================================
# Exercise 1: Basic Query Parameters
# =============================================================================
# Create an app with these endpoints:
#   GET /search
#       - q: str (required query param)
#       - Return {"query": q, "results": []}
#
#   GET /search
#       - q: str (required)
#       - limit: int = 10 (default 10)
#       - Return {"query": q, "limit": limit, "results": []}
#
#   GET /filter
#       - category: Optional[str] = None
#       - min_price: Optional[float] = None
#       - max_price: Optional[float] = None
#       - Return all params as a dict
#
# Hints:
#   - Query params without defaults are REQUIRED
#   - Query params with defaults are OPTIONAL
#   - Use Optional[str] = None for truly optional params
#   - Combine both in one route if needed
#
# Expected behavior:
#   GET /search?q=fastapi               -> {"query": "fastapi", "limit": 10, ...}
#   GET /search?q=fastapi&limit=5        -> {"query": "fastapi", "limit": 5, ...}
#   GET /search                          -> 422 (q is required)
#   GET /filter?category=books           -> {"category": "books", ...}
#   GET /filter?min_price=10&max_price=50 -> {"min_price": 10.0, ...}
#
# Test with:
#   curl "http://localhost:8000/search?q=fastapi"
#   curl "http://localhost:8000/search?q=fastapi&limit=5"
#   curl "http://localhost:8000/filter?category=books&min_price=10"
# =============================================================================

app1 = FastAPI(title="Exercise 4.1 - Basic Query Parameters")


@app1.get("/search")
def search(q: str, limit: int = 10):
    pass  # TODO: Return {"query": q, "limit": limit, "results": []}


@app1.get("/filter")
def filter_items(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    pass  # TODO: Return {"category": category, "min_price": min_price, "max_price": max_price}


# =============================================================================
# Exercise 2: Query Parameter Validation
# =============================================================================
# Create an app with validated query parameters:
#   GET /users
#       - username: str (min_length=3, max_length=20, pattern=^[a-zA-Z0-9_]+$)
#       - Return {"username": username, "valid": true}
#
#   GET /products
#       - page: int = 1 (ge=1)
#       - page_size: int = 10 (ge=1, le=100)
#       - sort_by: str = "name" (enum-like: name, price, date)
#       - Return all params
#
# Hints:
#   - Use Query(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
#   - Use Query(ge=1) for minimum value
#   - For enum-like: validate against a list, return 400 if invalid
#   - Pattern is a regex string
#
# Expected behavior:
#   GET /users?username=alice        -> {"username": "alice", "valid": true}
#   GET /users?username=ab           -> 422 (too short)
#   GET /users?username=alice bob    -> 422 (invalid pattern)
#   GET /products?page=2&page_size=5 -> {"page": 2, "page_size": 5, "sort_by": "name"}
#   GET /products?sort_by=invalid    -> 400 (invalid sort)
#
# Test with:
#   curl "http://localhost:8000/users?username=alice"
#   curl "http://localhost:8000/users?username=ab"  # should fail
#   curl "http://localhost:8000/products?page=2&sort_by=price"
# =============================================================================

app2 = FastAPI(title="Exercise 4.2 - Query Validation")


@app2.get("/users")
def get_users(
    username: str = Query(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$"),
):
    pass  # TODO: Return {"username": username, "valid": True}


VALID_SORT_OPTIONS = ["name", "price", "date"]


@app2.get("/products")
def get_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="name"),
):
    pass  # TODO: Validate sort_by against VALID_SORT_OPTIONS, return 400 if invalid


# =============================================================================
# Exercise 3: Multiple Values and Aliases
# =============================================================================
# Create an app demonstrating:
#   GET /tags
#       - tags: list[str] (accepts multiple values like ?tags=a&tags=b)
#       - Return {"tags": tags, "count": len(tags)}
#
#   GET /items
#       - item-name: str (note the alias, since Python vars can't have hyphens)
#       - Return {"item_name": item_name}  # note: return with underscore
#
#   GET /config
#       - verbose: bool = False
#       - debug: bool = False
#       - Return {"verbose": verbose, "debug": debug}
#
# Hints:
#   - For list params: tags: list[str] or list[str] = []
#   - For alias: Query(alias="item-name")
#   - Bool params: ?verbose=true or ?verbose=1 (FastAPI handles conversion)
#   - Default bool is False (absent = False)
#
# Expected behavior:
#   GET /tags?tags=python&tags=fastapi   -> {"tags": ["python", "fastapi"], "count": 2}
#   GET /tags                            -> {"tags": [], "count": 0}
#   GET /items?item-name=my-item         -> {"item_name": "my-item"}
#   GET /config?verbose=true&debug=true  -> {"verbose": true, "debug": true}
#   GET /config                          -> {"verbose": false, "debug": false}
#
# Test with:
#   curl "http://localhost:8000/tags?tags=python&tags=fastapi"
#   curl "http://localhost:8000/items?item-name=my-item"
#   curl "http://localhost:8000/config?verbose=true"
# =============================================================================

app3 = FastAPI(title="Exercise 4.3 - Multiple Values and Aliases")


@app3.get("/tags")
def get_tags(tags: list[str] = Query(default=[])):
    pass  # TODO: Return {"tags": tags, "count": len(tags)}


@app3.get("/items")
def get_item(item_name: str = Query(alias="item-name")):
    pass  # TODO: Return {"item_name": item_name}


@app3.get("/config")
def get_config(
    verbose: bool = Query(default=False),
    debug: bool = Query(default=False),
):
    pass  # TODO: Return {"verbose": verbose, "debug": debug}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 04-query-parameters:app1 --reload
#    - Test required vs optional params
#    - Verify missing required param returns 422
#
# 2. Run: uvicorn 04-query-parameters:app2 --reload
#    - Test min/max length validation
#    - Test pattern validation
#    - Test ge/le validation
#
# 3. Run: uvicorn 04-query-parameters:app3 --reload
#    - Test multiple values for list param
#    - Test alias (item-name -> item_name)
#    - Test boolean query params
# =============================================================================
