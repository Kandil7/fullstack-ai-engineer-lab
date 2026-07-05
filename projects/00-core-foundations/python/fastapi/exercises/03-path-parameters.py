"""
FastAPI Exercise 03 - Path Parameters
======================================

Topics covered:
- Defining path parameters
- Type conversion (int, float, str, bool, uuid)
- Path parameter validation
- Using Pydantic models for complex paths

Requirements:
    pip install fastapi uvicorn pydantic

Run any exercise:
    uvicorn 03-path-parameters:app1 --reload
    uvicorn 03-path-parameters:app2 --reload
    uvicorn 03-path-parameters:app3 --reload
"""

from fastapi import FastAPI, Path
from pydantic import BaseModel
from uuid import UUID


# =============================================================================
# Exercise 1: Basic Path Parameters
# =============================================================================
# Create an app with these routes:
#   GET /users/{user_id}          -> {"user_id": <int>, "type": "regular"}
#   GET /products/{product_id}    -> {"product_id": <int>, "type": "product"}
#   GET /greetings/{name}         -> {"greeting": "Hello, {name}!"}
#   GET /prices/{price}           -> {"price": <float>, "formatted": "$<price>"}
#
# Hints:
#   - Type hints convert path params: user_id: int
#   - If conversion fails, FastAPI returns 422 error automatically
#   - Use f-strings for formatted responses
#
# Expected behavior:
#   GET /users/123       -> {"user_id": 123, "type": "regular"}
#   GET /products/456    -> {"product_id": 456, "type": "product"}
#   GET /greetings/Alice -> {"greeting": "Hello, Alice!"}
#   GET /prices/19.99    -> {"price": 19.99, "formatted": "$19.99"}
#
# Test with:
#   curl http://localhost:8000/users/123
#   curl http://localhost:8000/products/456
#   curl http://localhost:8000/greetings/Alice
#   curl http://localhost:8000/prices/19.99
# =============================================================================

app1 = FastAPI(title="Exercise 3.1 - Basic Path Parameters")


@app1.get("/users/{user_id}")
def get_user(user_id: int):
    pass  # TODO: Return {"user_id": user_id, "type": "regular"}


@app1.get("/products/{product_id}")
def get_product(product_id: int):
    pass  # TODO: Return {"product_id": product_id, "type": "product"}


@app1.get("/greetings/{name}")
def greet(name: str):
    pass  # TODO: Return {"greeting": f"Hello, {name}!"}


@app1.get("/prices/{price}")
def get_price(price: float):
    pass  # TODO: Return {"price": price, "formatted": f"${price}"}


# =============================================================================
# Exercise 2: Path Parameter Validation with Path()
# =============================================================================
# Create an app with validated path parameters:
#   GET /scores/{score}
#       - score must be between 0 and 100
#       - Return {"score": score, "grade": <grade>}
#       - Grade: 90-100="A", 80-89="B", 70-79="C", 60-69="D", <60="F"
#
#   GET /users/{user_id}/posts/{post_id}
#       - user_id must be >= 1
#       - post_id must be >= 1
#       - Return {"user_id": user_id, "post_id": post_id}
#
# Hints:
#   - Use Path(ge=0, le=100) for range validation
#   - Use Path(ge=1) for minimum value validation
#   - Multiple path params in one route: /users/{user_id}/posts/{post_id}
#   - Grade logic: use if/elif/else or a helper function
#
# Expected behavior:
#   GET /scores/95      -> {"score": 95, "grade": "A"}
#   GET /scores/85      -> {"score": 85, "grade": "B"}
#   GET /scores/55      -> {"score": 55, "grade": "F"}
#   GET /scores/101     -> 422 error (score must be <= 100)
#   GET /scores/-1      -> 422 error (score must be >= 0)
#   GET /users/1/posts/5 -> {"user_id": 1, "post_id": 5}
#   GET /users/0/posts/5 -> 422 error (user_id must be >= 1)
#
# Test with:
#   curl http://localhost:8000/scores/95
#   curl http://localhost:8000/scores/101  # should fail
#   curl http://localhost:8000/users/1/posts/5
# =============================================================================

app2 = FastAPI(title="Exercise 3.2 - Path Validation")


def calculate_grade(score: int) -> str:
    """Calculate letter grade from numeric score."""
    pass  # TODO: Implement grade calculation


@app2.get("/scores/{score}")
def get_score(score: int = Path(ge=0, le=100)):
    pass  # TODO: Return {"score": score, "grade": calculate_grade(score)}


@app2.get("/users/{user_id}/posts/{post_id}")
def get_user_post(
    user_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    pass  # TODO: Return {"user_id": user_id, "post_id": post_id}


# =============================================================================
# Exercise 3: UUID Path Parameters and Enum-like Patterns
# =============================================================================
# Create an app that handles:
#   GET /items/{item_id}
#       - item_id is a UUID
#       - Return {"item_id": str(item_id), "exists": true}
#
#   GET /categories/{category_name}
#       - category_name must be one of: "electronics", "books", "clothing"
#       - If valid: {"category": category_name, "valid": true}
#       - If invalid: return 400 with {"error": "Invalid category"}
#
# Hints:
#   - For UUID: item_id: UUID (from uuid import UUID)
#   - FastAPI auto-validates UUID format
#   - For enum-like: use a list of valid values and check manually
#   - Or use: from enum import Enum; class Category(str, Enum): ...
#
# Expected behavior:
#   GET /items/550e8400-e29b-41d4-a716-446655440000
#       -> {"item_id": "550e8400-e29b-41d4-a716-446655440000", "exists": true}
#   GET /items/not-a-uuid -> 422 error (invalid UUID)
#   GET /categories/electronics -> {"category": "electronics", "valid": true}
#   GET /categories/food -> 400 error
#
# Test with:
#   curl http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440000
#   curl http://localhost:8000/categories/electronics
#   curl http://localhost:8000/categories/food  # should fail
# =============================================================================

from enum import Enum

app3 = FastAPI(title="Exercise 3.3 - UUID and Enum Patterns")


@app3.get("/items/{item_id}")
def get_item_by_uuid(item_id: UUID):
    pass  # TODO: Return {"item_id": str(item_id), "exists": True}


VALID_CATEGORIES = ["electronics", "books", "clothing"]


@app3.get("/categories/{category_name}")
def get_category(category_name: str):
    pass  # TODO: Validate category and return appropriate response


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 03-path-parameters:app1 --reload
#    - Verify type conversion works (int, float, str)
#    - Try invalid types (e.g., /users/abc) - should return 422
#
# 2. Run: uvicorn 03-path-parameters:app2 --reload
#    - Test score validation (0-100 range)
#    - Verify grade calculation is correct
#    - Test multiple path params in one route
#
# 3. Run: uvicorn 03-path-parameters:app3 --reload
#    - Test UUID parsing
#    - Test category validation
#    - Verify error responses for invalid inputs
# =============================================================================
