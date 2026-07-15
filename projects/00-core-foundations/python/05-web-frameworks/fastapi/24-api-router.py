"""
24 - APIRouter (Modular Routing)
===================================
Organize your API into modular routers for better maintainability.
Each router handles a group of related endpoints.

Run: uvicorn 24-api-router:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

app = FastAPI(title="APIRouter Demo")


# ----- Router 1: Users -----
users_router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


users_db: dict[int, dict] = {}
next_user_id = 1


@users_router.get("/", response_model=list[UserResponse])
def list_users():
    """List all users."""
    return list(users_db.values())


@users_router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """Create a new user."""
    global next_user_id
    users_db[next_user_id] = {"id": next_user_id, **user.model_dump()}
    next_user_id += 1
    return users_db[next_user_id - 1]


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@users_router.delete("/{user_id}")
def delete_user(user_id: int):
    """Delete user."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"deleted": True}


# ----- Router 2: Products -----
products_router = APIRouter(prefix="/products", tags=["Products"])


class ProductCreate(BaseModel):
    name: str
    price: float
    category: str


products_db: dict[int, dict] = {}
next_product_id = 1


@products_router.get("/")
def list_products(category: str | None = None):
    """List products with optional category filter."""
    products = list(products_db.values())
    if category:
        products = [p for p in products if p["category"] == category]
    return {"count": len(products), "products": products}


@products_router.post("/", status_code=201)
def create_product(product: ProductCreate):
    """Create a new product."""
    global next_product_id
    products_db[next_product_id] = {"id": next_product_id, **product.model_dump()}
    next_product_id += 1
    return products_db[next_product_id - 1]


@products_router.get("/{product_id}")
def get_product(product_id: int):
    """Get product by ID."""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]


# ----- Router 3: Orders -----
orders_router = APIRouter(prefix="/orders", tags=["Orders"])


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


orders_db: list[dict] = []


@orders_router.get("/")
def list_orders():
    """List all orders."""
    return {"count": len(orders_db), "orders": orders_db}


@orders_router.post("/", status_code=201)
def create_order(order: OrderCreate):
    """Create a new order."""
    if order.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if order.product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products_db[order.product_id]
    order_dict = {
        "id": len(orders_db) + 1,
        "user": users_db[order.user_id]["name"],
        "product": product["name"],
        "quantity": order.quantity,
        "total": product["price"] * order.quantity,
        "created_at": datetime.now().isoformat(),
    }
    orders_db.append(order_dict)
    return order_dict


# ----- Router 4: Health & System (no prefix) -----
system_router = APIRouter(tags=["System"])


@system_router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@system_router.get("/info")
def system_info():
    """System information."""
    return {
        "app": "APIRouter Demo",
        "version": "1.0.0",
        "routers": ["users", "products", "orders", "system"],
    }


# ----- Include all routers -----
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(system_router)


# ----- Root endpoint -----
@app.get("/")
def root():
    """API root with available endpoints."""
    return {
        "message": "APIRouter Demo",
        "endpoints": {
            "users": "/users/",
            "products": "/products/",
            "orders": "/orders/",
            "health": "/health",
            "docs": "/docs",
        },
    }


# ----- Advanced: Router with dependencies -----
from fastapi import Depends


def verify_api_key():
    """Shared dependency for admin routes."""
    return {"role": "admin"}


admin_router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(verify_api_key)])


@admin_router.get("/stats")
def admin_stats():
    """Admin stats — requires API key (via router-level dependency)."""
    return {
        "users": len(users_db),
        "products": len(products_db),
        "orders": len(orders_db),
    }


@admin_router.get("/users")
def admin_list_users():
    """Admin user listing."""
    return {"users": list(users_db.values())}


app.include_router(admin_router)


"""
Testing with curl:
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/health
    curl http://127.0.0.1:8000/info

    curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@test.com"}'
    curl http://127.0.0.1:8000/users/

    curl -X POST http://127.0.0.1:8000/products/ -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 999.99, "category": "electronics"}'
    curl http://127.0.0.1:8000/products/?category=electronics

    curl -X POST http://127.0.0.1:8000/orders/ -H "Content-Type: application/json" -d '{"user_id": 1, "product_id": 1, "quantity": 2}'

    curl http://127.0.0.1:8000/admin/stats

    Open /docs to see grouped tags in Swagger UI!
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
