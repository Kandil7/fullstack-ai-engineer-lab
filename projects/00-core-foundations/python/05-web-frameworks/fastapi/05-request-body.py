"""
05 - Request Body
===================
When you need to send data from a client to your API, you send it as a request body.
FastAPI uses Pydantic models to declare and validate request bodies.

Run: uvicorn 05-request-body:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Request Body in FastAPI")


# ----- Pydantic Models -----
class UserCreate(BaseModel):
    """Model for creating a new user."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., description="User's email address")
    age: int = Field(..., ge=0, le=150, description="User's age")
    bio: str | None = Field(default=None, max_length=500, description="Short bio")
    is_active: bool = Field(default=True, description="Whether user is active")


class UserUpdate(BaseModel):
    """Model for updating a user (all fields optional)."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = None
    age: int | None = Field(default=None, ge=0, le=150)
    bio: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    """Model for user response (includes generated fields)."""
    id: int
    name: str
    email: str
    age: int
    bio: str | None = None
    is_active: bool
    created_at: str


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class OrderItem(BaseModel):
    product_name: str
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., gt=0)


class Order(BaseModel):
    """Nested Pydantic model for complex request bodies."""
    customer_name: str
    items: list[OrderItem]
    shipping_address: Address
    notes: str | None = None


# In-memory database
users_db: dict[int, dict] = {}
orders_db: list[dict] = []
next_user_id = 1


# ----- Create user with request body -----
@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """
    Create a new user. The request body is automatically:
    1. Read from JSON
    2. Validated against UserCreate schema
    3. Converted to a Python object
    """
    global next_user_id
    user_dict = user.model_dump()
    user_dict["id"] = next_user_id
    user_dict["created_at"] = datetime.now().isoformat()
    users_db[next_user_id] = user_dict
    next_user_id += 1
    return user_dict


# ----- Update with partial body -----
@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    """
    Partial update using PATCH. Only fields sent in the body are updated.
    Pydantic ignores None values (unset fields).
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    stored = users_db[user_id]
    update_data = user.model_dump(exclude_unset=True)
    stored.update(update_data)
    return stored


# ----- Full update with PUT -----
@app.put("/users/{user_id}", response_model=UserResponse)
def full_update_user(user_id: int, user: UserCreate):
    """
    Full update using PUT. All fields are required.
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user.model_dump()
    user_dict["id"] = user_id
    user_dict["created_at"] = users_db[user_id]["created_at"]
    users_db[user_id] = user_dict
    return user_dict


# ----- Complex nested request body -----
@app.post("/orders/")
def create_order(order: Order):
    """
    Complex nested request body.
    FastAPI validates the entire nested structure automatically.
    """
    total = sum(item.quantity * item.unit_price for item in order.items)
    order_dict = {
        "id": len(orders_db) + 1,
        "customer": order.customer_name,
        "items": [item.model_dump() for item in order.items],
        "shipping": order.shipping_address.model_dump(),
        "notes": order.notes,
        "total": round(total, 2),
        "created_at": datetime.now().isoformat(),
    }
    orders_db.append(order_dict)
    return order_dict


# ----- Multiple body parameters -----
@app.post("/batch-create")
def batch_create(
    users: list[UserCreate],
    send_welcome_email: bool = True,
):
    """
    Receive a list of users as the request body.
    Multiple body params use Body() in FastAPI.
    """
    created = []
    for user in users:
        global next_user_id
        user_dict = user.model_dump()
        user_dict["id"] = next_user_id
        user_dict["created_at"] = datetime.now().isoformat()
        users_db[next_user_id] = user_dict
        created.append(user_dict)
        next_user_id += 1
    return {
        "created_count": len(created),
        "send_email": send_welcome_email,
        "users": created,
    }


# ----- Request body with field examples -----
class ProductCreate(BaseModel):
    """Product with field examples for better docs."""
    name: str = Field(..., examples=["Wireless Mouse"])
    description: str = Field(default="", examples=["Ergonomic wireless mouse with USB receiver"])
    price: float = Field(..., gt=0, examples=[29.99])
    in_stock: bool = Field(default=True)
    tags: list[str] = Field(default=[], examples=[["electronics", "peripherals"]])


@app.post("/products/", status_code=201)
def create_product(product: ProductCreate):
    """Products with Field examples for Swagger UI."""
    return {
        "id": len(orders_db) + 1,
        **product.model_dump(),
    }


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com", "age": 30}'

    curl -X PATCH http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d '{"bio": "Updated bio"}'

    curl -X PUT http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d '{"name": "Alice Smith", "email": "alice@new.com", "age": 31}'

    curl -X POST http://127.0.0.1:8000/orders/ -H "Content-Type: application/json" -d '{"customer_name": "Bob", "items": [{"product_name": "Keyboard", "quantity": 2, "unit_price": 79.99}], "shipping_address": {"street": "123 Main St", "city": "Springfield", "state": "IL", "zip_code": "62701"}}'

    curl -X POST http://127.0.0.1:8000/batch-create -H "Content-Type: application/json" -d '[{"name": "User1", "email": "u1@test.com", "age": 20}, {"name": "User2", "email": "u2@test.com", "age": 25}]'
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
