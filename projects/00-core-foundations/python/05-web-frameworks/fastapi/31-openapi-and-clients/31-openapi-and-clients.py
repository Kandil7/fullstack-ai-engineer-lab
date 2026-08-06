"""
31 - OpenAPI and Typed Clients
================================
Customizing the schema, tags and operation IDs, security schemes,
examples, generating typed clients, docs as the API surface.

Run:      python 31-openapi-and-clients.py
Verify:   python 31-openapi-and-clients.py --verify
Reference: https://spec.openapis.org/oas/v3.1.0.html
"""

from __future__ import annotations

import sys

from fastapi import FastAPI, APIRouter, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ============================================================
# 1. Documented, tagged, versioned API surface
# ============================================================
app = FastAPI(
    title="Inventory API",
    version="2.1.0",
    description="Product catalog with typed examples and auth scheme.",
    openapi_tags=[
        {"name": "products", "description": "Catalog operations"},
        {"name": "admin", "description": "Restricted operations"},
    ],
)

bearer = HTTPBearer()


class Product(BaseModel):
    sku: str = Field(examples=["GPU-2000"])
    name: str = Field(examples=["A100 GPU"])
    price_cents: int = Field(gt=0, examples=[150000])


PRODUCTS: dict[str, Product] = {}


@app.get("/products", tags=["products"], operation_id="listProducts",
         summary="List all products", responses={200: {"description": "OK"}})
def list_products(limit: int = 10) -> list[Product]:
    return list(PRODUCTS.values())[:limit]


@app.post("/products", tags=["products"], operation_id="createProduct",
          status_code=201, response_model=Product,
          responses={401: {"description": "Missing bearer token"}})
def create_product(product: Product,
                   credentials: HTTPAuthorizationCredentials = Security(bearer)) -> Product:
    """Requires a bearer token — visible in the OpenAPI security scheme."""
    if credentials.credentials != "admin-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    PRODUCTS[product.sku] = product
    return product


# ============================================================
# 2. Generating a typed client from the schema
# ============================================================
def generate_python_client(openapi: dict) -> str:
    """A tiny illustration: real tools (openapi-python-client, kiota)
    parse the same schema into full SDKs."""
    lines = ["class InventoryClient:", "    \"\"\"Typed client generated from OpenAPI.\"\"\""]
    for path, methods in openapi.get("paths", {}).items():
        for method, spec in methods.items():
            if method not in ("get", "post", "put", "delete"):
                continue
            op_id = spec.get("operationId", f"{method}_{path.replace('/', '_')}")
            lines.append(f"    def {op_id}(self, base_url: str):")
            lines.append(f"        # {method.upper()} {path}")
            lines.append("        ...")
    return "\n".join(lines)


# ============================================================
# 3. Contract: examples flow into docs and client generation
# ============================================================
print("=" * 60)
print("Summary:")
print("- OpenAPI = the API surface: docs, examples, security schemes")
print("- operation_id gives clients stable method names")
print("- Examples make the contract human-readable and testable")
print("- Typed clients are GENERATED from the schema, never hand-written")
print("- A schema that documents auth prevents 401s before they happen")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # OpenAPI metadata
        schema = client.get("/openapi.json").json()
        assert schema["info"]["title"] == "Inventory API"
        assert schema["info"]["version"] == "2.1.0"
        assert "listProducts" in schema["paths"]["/products"]["get"]["operationId"]
        assert "createProduct" in schema["paths"]["/products"]["post"]["operationId"]

        # Security scheme declared on the protected operation
        post_op = schema["paths"]["/products"]["post"]
        assert "security" in post_op, "protected op must declare security"
        assert "HTTPBearer" in schema["components"]["securitySchemes"]

        # Examples present in the schema
        assert "GPU-2000" in str(schema["components"]["schemas"]["Product"])

        # Auth enforced at runtime
        r = client.post("/products", json={"sku": "X", "name": "Y", "price_cents": 1})
        assert r.status_code == 403 or r.status_code == 401, "no token -> rejected"

        # Generated client covers every path
        code = generate_python_client(schema)
        assert "listProducts" in code and "createProduct" in code

    print("[OK] 31-openapi-and-clients: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("31-openapi-and-clients:app", host="127.0.0.1", port=8000)
    else:
        _verify()
