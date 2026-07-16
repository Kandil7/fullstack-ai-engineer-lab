"""
FastAPI Exercise 05 - Request Body
====================================

Topics covered:
- Pydantic request models
- Nested models
- Optional fields with defaults
- Request body + path parameters
- Request body + query parameters

Run:
    uvicorn 05-request-body:app --reload
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Request Body Exercise")

# In-memory stores
users_db: dict[int, dict] = {}
products_db: dict[int, dict] = {}
next_user_id = 1
next_product_id = 1


# =============================================================================
# Exercise 1: Basic Request Body
# =============================================================================
class UserCreate(BaseModel):
    """User creation model."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int = Field(ge=0, le=150, default=18)


class ProductCreate(BaseModel):
    """Product creation model."""
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(gt=0, description="Price must be positive")
    in_stock: bool = True


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    """Create a new user from request body."""
    global next_user_id
    user_data = {"id": next_user_id, **user.model_dump(), "created": True}
    users_db[next_user_id] = user_data
    next_user_id += 1
    return {"id": next_user_id - 1, **user.model_dump(), "created": True}


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    """Create a new product from request body."""
    global next_product_id
    product_data = {"id": next_product_id, **product.model_dump()}
    products_db[next_product_id] = product_data
    next_product_id += 1
    return {"id": next_product_id - 1, **product.model_dump()}


# =============================================================================
# Exercise 2: Nested Models
# =============================================================================
class OrderItem(BaseModel):
    """Item within an order."""
    product_id: int
    quantity: int = Field(ge=1, le=100)
    unit_price: float = Field(gt=0)


class OrderCreate(BaseModel):
    """Order creation with nested items."""
    customer_name: str = Field(..., min_length=1)
    items: list[OrderItem] = Field(..., min_length=1)
    shipping_address: str


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    """Create an order with nested items."""
    total = sum(item.quantity * item.unit_price for item in order.items)
    return {
        "order_id": 1,
        "customer": order.customer_name,
        "items_count": len(order.items),
        "total": round(total, 2),
        "shipping_to": order.shipping_address,
        "status": "confirmed",
    }


# =============================================================================
# Exercise 3: Body + Path + Query Parameters
# =============================================================================
class UserProfile(BaseModel):
    """User profile update model."""
    name: Optional[str] = None
    email: Optional[str] = None
    notify: bool = True


class ReviewCreate(BaseModel):
    """Product review model."""
    rating: int = Field(ge=1, le=5)
    comment: str = Field(..., min_length=1, max_length=1000)


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserProfile):
    """Update user with body + path parameter."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = {k: v for k, v in user.model_dump().items() if v is not None}
    users_db[user_id].update(update_data)
    return {
        "user_id": user_id,
        "name": user.name or users_db[user_id].get("name"),
        "email": user.email or users_db[user_id].get("email"),
        "notify": user.notify,
    }


@app.post("/products/{product_id}/reviews", status_code=201)
def create_review(product_id: int, review: ReviewCreate):
    """Create a review for a product with path parameter."""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "product_id": product_id,
        "rating": review.rating,
        "comment": review.comment,
        "submitted": True,
    }
