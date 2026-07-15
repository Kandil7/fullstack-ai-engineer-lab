"""
03 - Path Parameters
======================
Path parameters are variable parts of a URL path.
They are used to capture values from the URL and pass them to the function.

Run: uvicorn 03-path-parameters:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI(title="Path Parameters in FastAPI")


# ----- Simple path parameter -----
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Path parameter with type conversion.
    FastAPI sees user_id: int and validates/converts it.
    """
    return {"user_id": user_id, "name": f"User {user_id}"}


# ----- Multiple path parameters -----
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    """Multiple path parameters in a single URL."""
    return {
        "user_id": user_id,
        "post_id": post_id,
        "content": f"Post {post_id} by User {user_id}",
    }


# ----- Path parameter with predefined values (Enum) -----
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    """
    Path parameter constrained to an enum.
    Only the listed values are accepted; others return 422.
    """
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name is ModelName.resnet:
        return {"model_name": model_name, "message": "Residual Learning FTW!"}
    elif model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeNet is best!"}


# ----- Path parameter with validation using Path() -----
@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(
        ...,
        title="Product ID",
        description="The unique identifier of the product",
        ge=1,       # greater than or equal
        le=1000,    # less than or equal
    )
):
    """
    Using Path() for additional validation and documentation.
    ge=1 means product_id must be >= 1
    """
    return {
        "product_id": product_id,
        "name": f"Product #{product_id}",
        "available": True,
    }


# ----- Path parameter with string type -----
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    """
    The :path type allows slashes in the parameter.
    e.g., /files/home/user/document.txt
    """
    return {"file_path": file_path, "exists": True}


# ----- Predefined values for string path params -----
@app.get("/status/{status_code}")
def get_status(status_code: str):
    """
    Path parameter as string with custom validation.
    """
    valid_codes = ["200", "404", "500", "503"]
    if status_code not in valid_codes:
        return {"error": f"Invalid status code. Valid: {valid_codes}"}
    messages = {
        "200": "OK",
        "404": "Not Found",
        "500": "Internal Server Error",
        "503": "Service Unavailable",
    }
    return {"status_code": status_code, "message": messages[status_code]}


# ----- UUID path parameter -----
from uuid import UUID


@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    """FastAPI handles UUID conversion automatically."""
    return {
        "order_id": str(order_id),
        "status": "shipped",
        "estimated_delivery": datetime.now().isoformat(),
    }


# ----- Path parameter with regex pattern -----
from fastapi import HTTPException

@app.get("/categories/{category_name}")
def get_category(category_name: str):
    """
    Validate category_name with custom logic.
    In production, use Path(pattern=r'^[a-z-]+$') for regex validation.
    """
    allowed_categories = ["electronics", "books", "clothing", "home", "sports"]
    if category_name.lower() not in allowed_categories:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category_name}' not found. Allowed: {allowed_categories}",
        )
    return {
        "category": category_name.lower(),
        "item_count": 42,
    }


"""
Testing with curl:
    curl http://127.0.0.1:8000/users/42
    curl http://127.0.0.1:8000/users/5/posts/10
    curl http://127.0.0.1:8000/models/resnet
    curl http://127.0.0.1:8000/products/42
    curl http://127.0.0.1:8000/files/home/user/document.txt
    curl http://127.0.0.1:8000/status/200
    curl http://127.0.0.1:8000/orders/550e8400-e29b-41d4-a716-446655440000
    curl http://127.0.0.1:8000/categories/electronics
    curl http://127.0.0.1:8000/categories/invalid
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
