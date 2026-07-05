"""
04 - Query Parameters
=======================
Query parameters come after the ? in the URL.
They are key=value pairs separated by &.
FastAPI handles them automatically using function parameters.

Run: uvicorn 04-query-parameters:app --reload
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Query Parameters in FastAPI")


# In-memory data
USERS = [
    {"id": 1, "name": "Alice", "age": 30, "department": "Engineering", "active": True},
    {"id": 2, "name": "Bob", "age": 25, "department": "Marketing", "active": True},
    {"id": 3, "name": "Charlie", "age": 35, "department": "Engineering", "active": False},
    {"id": 4, "name": "Diana", "age": 28, "department": "Sales", "active": True},
    {"id": 5, "name": "Eve", "age": 32, "department": "Engineering", "active": True},
]


# ----- Basic query parameters with defaults -----
@app.get("/search")
def search_items(q: str = "", page: int = 1, per_page: int = 10):
    """
    Search with query parameters.
    All parameters have defaults, so they're all optional.
    /search?q=phone&page=2&per_page=5
    """
    results = [u for u in USERS if q.lower() in u["name"].lower()] if q else USERS
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "query": q,
        "page": page,
        "per_page": per_page,
        "total": len(results),
        "results": results[start:end],
    }


# ----- Query parameters with validation -----
@app.get("/users/")
def list_users(
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
    sort_by: str = Query(default="name", description="Field to sort by"),
    order: str = Query(default="asc", description="Sort order: asc or desc"),
):
    """
    Query parameters with Pydantic validation via Query().
    ge=greater than or equal, le=less than or equal.
    """
    sorted_users = sorted(USERS, key=lambda u: u.get(sort_by, ""), reverse=(order == "desc"))
    paginated = sorted_users[skip : skip + limit]
    return {
        "total": len(USERS),
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "order": order,
        "results": paginated,
    }


# ----- Required query parameter (no default) -----
@app.get("/filter")
def filter_users(department: str):
    """
    A required query parameter — no default value.
    /filter?department=Engineering
    """
    filtered = [u for u in USERS if u["department"].lower() == department.lower()]
    return {"department": department, "count": len(filtered), "users": filtered}


# ----- Boolean query parameter -----
@app.get("/active-users")
def get_active_users(active: bool = True):
    """Query parameter as boolean. /active-users?active=false"""
    filtered = [u for u in USERS if u["active"] == active]
    return {"active": active, "count": len(filtered), "users": filtered}


# ----- List query parameter -----
@app.get("/multi-filter")
def multi_filter(
    departments: list[str] = Query(default=[], description="Filter by departments"),
    min_age: int = Query(default=0, ge=0),
    max_age: int = Query(default=100, le=200),
):
    """
    List query params: /multi-filter?departments=Engineering&departments=Sales&min_age=25
    Use [] or repeat the param for multiple values.
    """
    filtered = USERS
    if departments:
        filtered = [u for u in filtered if u["department"] in departments]
    filtered = [u for u in filtered if min_age <= u["age"] <= max_age]
    return {
        "filters": {"departments": departments, "min_age": min_age, "max_age": max_age},
        "count": len(filtered),
        "results": filtered,
    }


# ----- Optional query parameter with alias -----
@app.get("/products/")
def list_products(
    product_name: str | None = Query(default=None, alias="name"),
    min_price: float = Query(default=0.0, ge=0),
    max_price: float = Query(default=10000.0, le=100000),
    tags: list[str] = Query(default=[]),
):
    """
    Optional params and aliases.
    /products/?name=laptop&min_price=500&tags=new&tags=sale
    """
    return {
        "filters": {
            "name": product_name,
            "min_price": min_price,
            "max_price": max_price,
            "tags": tags,
        },
        "message": "Products endpoint (demo data)",
    }


# ----- Search with pagination and metadata -----
@app.get("/users/search")
def advanced_search(
    q: str = Query(default="", min_length=0, max_length=50, description="Search term"),
    department: str | None = Query(default=None),
    min_age: int = Query(default=0, ge=0, le=150),
    max_age: int = Query(default=100, ge=0, le=150),
    active_only: bool = Query(default=False),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
):
    """
    Advanced search combining multiple query parameter types.
    /users/search?q=eng&department=Engineering&min_age=25&page=1
    """
    results = USERS

    # Apply filters
    if q:
        results = [u for u in results if q.lower() in u["name"].lower()]
    if department:
        results = [u for u in results if u["department"].lower() == department.lower()]
    results = [u for u in results if min_age <= u["age"] <= max_age]
    if active_only:
        results = [u for u in results if u["active"]]

    # Pagination
    total = len(results)
    start = (page - 1) * page_size
    paginated = results[start : start + page_size]
    total_pages = (total + page_size - 1) // page_size

    return {
        "query": q,
        "filters": {
            "department": department,
            "age_range": [min_age, max_age],
            "active_only": active_only,
        },
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
        },
        "results": paginated,
    }


"""
Testing with curl:
    curl "http://127.0.0.1:8000/search?q=alice"
    curl "http://127.0.0.1:8000/search?page=1&per_page=2"
    curl "http://127.0.0.1:8000/users/?sort_by=age&order=desc"
    curl "http://127.0.0.1:8000/filter?department=Engineering"
    curl "http://127.0.0.1:8000/active-users?active=true"
    curl "http://127.0.0.1:8000/multi-filter?departments=Engineering&departments=Sales&min_age=25"
    curl "http://127.0.0.1:8000/products/?name=laptop&min_price=500"
    curl "http://127.0.0.1:8000/users/search?q=e&department=Engineering&page=1"
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
