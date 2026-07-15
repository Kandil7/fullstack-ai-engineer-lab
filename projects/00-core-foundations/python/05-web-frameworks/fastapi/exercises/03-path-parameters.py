"""
FastAPI Exercise 03 - Path Parameters
======================================

Topics covered:
- Path parameter types and validation
- Built-in validators (Path, int, float)
- Multiple path parameters
- Enum path parameters

Requirements:
    pip install fastapi uvicorn

Run:
    uvicorn 03-path-parameters:app --reload
"""

from enum import Enum
from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="Path Parameters Exercise")


# =============================================================================
# Exercise 1: Basic Path Parameters
# =============================================================================
# Create endpoints that use path parameters with different types:
#   GET /users/{user_id}       -> {"user_id": user_id, "type": "regular"}
#   GET /products/{product_id} -> {"product_id": product_id, "type": "product"}
#   GET /hello/{name}          -> {"greeting": f"Hello, {name}!"}
#   GET /price/{price}         -> {"price": price, "formatted": f"${price}"}
#
# Hints:
#   - Path parameters are defined in the route path with {param_name}
#   - FastAPI automatically converts to the declared type
#   - Use type hints: int, str, float
# =============================================================================


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Return user info based on path parameter."""
    return {"user_id": user_id, "type": "regular"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Return product info based on path parameter."""
    return {"product_id": product_id, "type": "product"}


@app.get("/hello/{name}")
def hello_user(name: str):
    """Return a personalized greeting."""
    return {"greeting": f"Hello, {name}!"}


@app.get("/price/{price}")
def get_price(price: float):
    """Return price info with formatted string."""
    return {"price": price, "formatted": f"${price}"}


# =============================================================================
# Exercise 2: Path Validation
# =============================================================================
# Create endpoints with path validation using Path() from FastAPI:
#   GET /grade/{score} -> Validate score is between 0 and 100, return grade
#     Score >= 90: A, >= 80: B, >= 70: C, >= 60: D, else: F
#   GET /users/{user_id}/posts/{post_id} -> Two path parameters
#
# Hints:
#   - Use Path(ge=0, le=100) for score validation
#   - Multiple path params work by adding more {params}
# =============================================================================


@app.get("/grade/{score}")
def get_grade(score: int = Path(ge=0, le=100, description="Score between 0 and 100")):
    """Calculate letter grade from score with validation."""
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    return {"score": score, "grade": grade}


@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    """Return info about a specific user's post."""
    return {"user_id": user_id, "post_id": post_id}


# =============================================================================
# Exercise 3: Enum Path Parameters
# =============================================================================
# Use Enum for path parameters with a fixed set of valid values:
#   GET /items/{category} where category is one of: books, electronics, clothing, food
#   Return category info or 404 if invalid
#
# Hints:
#   - Create an Enum class with the valid categories
#   - Use the Enum as the type hint for the path parameter
#   - FastAPI auto-validates and returns 422 for invalid values
# =============================================================================


class ItemCategory(str, Enum):
    """Valid item categories."""
    BOOKS = "books"
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"


ITEMS_BY_CATEGORY = {
    ItemCategory.BOOKS: ["Python 101", "FastAPI Guide", "Data Science Handbook"],
    ItemCategory.ELECTRONICS: ["Laptop", "Mouse", "Keyboard"],
    ItemCategory.CLOTHING: ["T-Shirt", "Jeans", "Jacket"],
    ItemCategory.FOOD: ["Apple", "Bread", "Cheese"],
}


@app.get("/items/{category}")
def get_items_by_category(category: ItemCategory):
    """Return items for a given category. Invalid categories get 422 auto-validation."""
    return {"category": category.value, "items": ITEMS_BY_CATEGORY[category]}


# =============================================================================
# Exercise 4: Path Parameters with Length Validation
# =============================================================================
# Use Path() to add length constraints on string path parameters:
#   GET /codes/{code} -> code must be exactly 6 characters
#   GET /tags/{tag} -> tag must be 2-10 characters
#
# Hints:
#   - Use min_length and max_length in Path()
#   - Or use pattern (regex) for exact length matching
# =============================================================================


@app.get("/codes/{code}")
def get_code(
    code: str = Path(min_length=6, max_length=6, description="Code must be exactly 6 characters")
):
    """Validate code is exactly 6 characters."""
    return {"code": code, "valid": True}


@app.get("/tags/{tag}")
def get_tag(
    tag: str = Path(min_length=2, max_length=10, description="Tag must be 2-10 characters")
):
    """Validate tag length (2-10 characters)."""
    return {"tag": tag, "length": len(tag), "valid": True}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# 1. Run: uvicorn 03-path-parameters:app --reload
# 2. Test: GET /users/42, /products/7, /hello/World, /price/19.99
# 3. Test validation: GET /grade/85 (valid), /grade/150 (should fail)
# 4. Test enum: GET /items/books (valid), /items/cars (should return 422)
# 5. Test length validation: GET /codes/ABC123 (valid), /codes/AB (should fail)
# =============================================================================
