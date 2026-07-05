"""
FastAPI Exercise 05 - Request Body
===================================

Topics covered:
- Defining request body with Pydantic models
- Body validation and default values
- Nested models
- Multiple body parameters

Requirements:
    pip install fastapi uvicorn pydantic

Run any exercise:
    uvicorn 05-request-body:app1 --reload
    uvicorn 05-request-body:app2 --reload
    uvicorn 05-request-body:app3 --reload
"""

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional


# =============================================================================
# Exercise 1: Basic Pydantic Request Body
# =============================================================================
# Create an app with POST endpoints:
#   POST /users
#       - Body: {"name": str, "email": str, "age": int}
#       - Return: {"id": 1, "name": ..., "email": ..., "age": ..., "created": true}
#
#   POST /products
#       - Body: {"name": str, "price": float, "description": str (optional)}
#       - Return: {"id": 1, "name": ..., "price": ..., "description": ...}
#
# Hints:
#   - Create Pydantic models: class User(BaseModel): name: str; ...
#   - Use the model as the function parameter type
#   - Optional fields: description: Optional[str] = None
#   - You can use Field for extra validation: price: float = Field(gt=0)
#
# Expected behavior:
#   POST /users with {"name": "Alice", "email": "alice@example.com", "age": 30}
#       -> {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30, "created": true}
#   POST /users with {"name": "Bob"}
#       -> 422 (missing required fields)
#
# Test with:
#   curl -X POST http://localhost:8000/users \
#     -H "Content-Type: application/json" \
#     -d '{"name": "Alice", "email": "alice@example.com", "age": 30}'
# =============================================================================

app1 = FastAPI(title="Exercise 5.1 - Basic Request Body")


class UserCreate(BaseModel):
    name: str
    email: str
    age: int


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    description: Optional[str] = None


@app1.post("/users")
def create_user(user: UserCreate):
    pass  # TODO: Return {"id": 1, **user.model_dump(), "created": True}


@app1.post("/products")
def create_product(product: ProductCreate):
    pass  # TODO: Return {"id": 1, **product.model_dump()}


# =============================================================================
# Exercise 2: Nested Pydantic Models
# =============================================================================
# Create an app with nested request bodies:
#   POST /orders
#       - Body: {
#           "customer_name": str,
#           "items": [{"name": str, "quantity": int, "price": float}],
#           "shipping_address": {
#               "street": str,
#               "city": str,
#               "zip_code": str
#           }
#       }
#       - Return: {
#           "order_id": 1,
#           "customer_name": ...,
#           "total": <sum of quantity * price>,
#           "item_count": <len(items)>
#       }
#
# Hints:
#   - Create Address(BaseModel): street, city, zip_code
#   - Create OrderItem(BaseModel): name, quantity, price
#   - Create Order(BaseModel): customer_name, items: list[OrderItem], shipping_address: Address
#   - Calculate total: sum(item.quantity * item.price for item in order.items)
#
# Expected behavior:
#   POST /orders with valid body -> {"order_id": 1, "total": 59.97, "item_count": 2}
#   POST /orders with missing fields -> 422 validation error
#
# Test with:
#   curl -X POST http://localhost:8000/orders \
#     -H "Content-Type: application/json" \
#     -d '{
#       "customer_name": "Alice",
#       "items": [
#         {"name": "Widget", "quantity": 2, "price": 9.99},
#         {"name": "Gadget", "quantity": 1, "price": 39.99}
#       ],
#       "shipping_address": {
#         "street": "123 Main St",
#         "city": "Springfield",
#         "zip_code": "62701"
#       }
#     }'
# =============================================================================

app2 = FastAPI(title="Exercise 5.2 - Nested Models")


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class OrderItem(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class Order(BaseModel):
    customer_name: str
    items: list[OrderItem]
    shipping_address: Address


@app2.post("/orders")
def create_order(order: Order):
    pass  # TODO: Calculate total and return order summary


# =============================================================================
# Exercise 3: Body with Path/Query + Body
# =============================================================================
# Create an app combining path params, query params, and body:
#   PUT /users/{user_id}
#       - Path: user_id: int
#       - Body: {"name": str, "email": str}
#       - Query: notify: bool = False
#       - Return: {"user_id": ..., "name": ..., "email": ..., "notify": ...}
#
#   POST /items/{item_id}/reviews
#       - Path: item_id: int
#       - Body: {"rating": int, "comment": str}
#       - Return: {"item_id": ..., "review": {...}, "average_rating": ...}
#
# Hints:
#   - FastAPI distinguishes path, query, and body params by type
#   - Path params use type hint without default
#   - Query params use Query(...)
#   - Body params use Pydantic model or Body(...)
#   - You can have one Pydantic body + other params
#
# Expected behavior:
#   PUT /users/42?notify=true with {"name": "Bob", "email": "bob@test.com"}
#       -> {"user_id": 42, "name": "Bob", "email": "bob@test.com", "notify": true}
#   POST /items/100/reviews with {"rating": 5, "comment": "Great!"}
#       -> {"item_id": 100, "review": {...}, "average_rating": 5.0}
#
# Test with:
#   curl -X PUT "http://localhost:8000/users/42?notify=true" \
#     -H "Content-Type: application/json" \
#     -d '{"name": "Bob", "email": "bob@test.com"}'
#   curl -X POST http://localhost:8000/items/100/reviews \
#     -H "Content-Type: application/json" \
#     -d '{"rating": 5, "comment": "Great!"}'
# =============================================================================

app3 = FastAPI(title="Exercise 5.3 - Path + Query + Body")


class UserUpdate(BaseModel):
    name: str
    email: str


class Review(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1, max_length=500)


# In-memory storage for average rating calculation
reviews_store: dict[int, list[int]] = {}


@app3.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    notify: bool = False,
):
    pass  # TODO: Return {"user_id": user_id, "name": user.name, "email": user.email, "notify": notify}


@app3.post("/items/{item_id}/reviews")
def create_review(item_id: int, review: Review):
    pass  # TODO: Store review, calculate average, return result


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 05-request-body:app1 --reload
#    - Test POST with valid body
#    - Test POST with missing fields (should return 422)
#    - Verify optional fields work
#
# 2. Run: uvicorn 05-request-body:app2 --reload
#    - Test nested model validation
#    - Verify total calculation
#    - Test with invalid nested data
#
# 3. Run: uvicorn 05-request-body:app3 --reload
#    - Test path + query + body combination
#    - Verify all three param types work together
#    - Test review rating validation (1-5 range)
# =============================================================================
