"""
FastAPI Exercise 04 - Query Parameters
=========================================

Topics covered:
- Basic query parameters
- Optional query parameters with defaults
- Query parameter validation
- Boolean and list query parameters
- Mixed path and query parameters

Run:
    uvicorn 04-query-parameters:app --reload
"""

from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI(title="Query Parameters Exercise")


# =============================================================================
# Exercise 1: Basic Query Parameters
# =============================================================================
@app.get("/search")
def search_items(
    q: str = Query(..., description="Search query string"),
    limit: int = Query(10, ge=1, le=100, description="Max results to return"),
):
    """Search with query and optional limit."""
    return {"query": q, "limit": limit, "results": []}


@app.get("/products/filter")
def filter_products(
    category: str = Query(..., description="Product category"),
    min_price: float = Query(0, ge=0, description="Minimum price"),
    max_price: float = Query(10000, ge=0, description="Maximum price"),
):
    """Filter products by category and price range."""
    return {"category": category, "min_price": min_price, "max_price": max_price}


# =============================================================================
# Exercise 2: Username Validation
# =============================================================================
VALID_SORT_OPTIONS = ["price", "name", "rating", "date"]


@app.get("/users/{username}")
def get_user_profile(
    username: str,
    include_details: bool = Query(False, description="Include extra details"),
):
    """Get user profile with optional details."""
    return {"username": username, "valid": True, "details_included": include_details}


@app.get("/products")
def list_products(
    sort_by: str = Query("name", description="Sort field"),
):
    """List products with optional sorting."""
    if sort_by not in VALID_SORT_OPTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by '{sort_by}'. Valid options: {VALID_SORT_OPTIONS}"
        )
    return {"sort_by": sort_by, "valid": True, "products": []}


# =============================================================================
# Exercise 3: Multiple Query Parameters
# =============================================================================
@app.get("/items/filter")
def filter_items(
    tags: list[str] = Query([], description="Filter by tags"),
    item_name: Optional[str] = Query(None, min_length=1, max_length=50),
):
    """Filter items by tags and optional name."""
    return {"tags": tags, "count": len(tags), "item_name": item_name}


@app.get("/debug")
def debug_request(
    verbose: bool = Query(False, description="Enable verbose output"),
    debug: bool = Query(False, description="Enable debug mode"),
):
    """Debug endpoint with boolean flags."""
    return {"verbose": verbose, "debug": debug}
