# FastAPI — 31: OpenAPI and Typed Clients

Companion exercise: `31-openapi-and-clients.py`

---

## Topic Overview

FastAPI generates an OpenAPI document from your code — and that document is
not documentation; it is the **API surface**. Clients are generated from it,
contract tests are written against it, and SDKs are derived from it. This
topic covers treating the schema as a first-class product: customizing titles
and versions, tagging and naming operations so generated clients get stable
method names, declaring security schemes so auth appears in the docs, and
adding examples that make contracts human-readable and testable.

The mental shift: **your code is the source of truth, and the OpenAPI schema
is the compiled contract.** If the schema is sloppy, every generated client,
test, and doc inherits the sloppiness.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why OpenAPI is the API surface, not just docs.
2. Customize app metadata (title, version, description, tags).
3. Use `operation_id` to stabilize generated client method names.
4. Declare security schemes that appear in the OpenAPI document.
5. Add examples that flow into docs and client generation.
6. Explain the contract-testing role of the schema.
7. Generate a typed client from the schema (conceptually and in miniature).
8. Keep the schema and the runtime behavior in agreement.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI basics | `01-introduction.py` through `06-response-model.py` |
| Auth / security | `12-security.py`, `13-jwt-auth.py` |
| Pydantic v2 | `26-pydantic-v2-deep.py` |

## 1. OpenAPI as the API Surface

```python
app = FastAPI(
    title="Inventory API",
    version="2.1.0",
    description="Product catalog with typed examples and auth scheme.",
)
```

Output:
```
# GET /openapi.json -> {"openapi": "3.1.0", "info": {"title": "Inventory API", ...}}
```

Every route, schema, parameter, and security scheme is compiled into
`/openapi.json`. Tools consume this document: generated clients, mock servers,
contract tests, and the interactive Swagger UI. The schema is the contract —
your code is its source.

## 2. Tags — Grouping the Surface

```python
app = FastAPI(openapi_tags=[
    {"name": "products", "description": "Catalog operations"},
    {"name": "admin", "description": "Restricted operations"},
])

@app.get("/products", tags=["products"], ...)
def list_products(): ...
```

Output:
```
# /openapi.json groups operations under tags -> organized docs and SDKs
```

Tags give the surface structure: products vs admin, public vs internal.
Generated clients often become one class per tag — a clean tag scheme yields a
clean SDK.

## 3. operation_id — Stable Method Names

```python
@app.get("/products", operation_id="listProducts")
def list_products(): ...
```

Output:
```
# schema: "operationId": "listProducts" -> generated client method listProducts()
```

Without an explicit `operation_id`, generated clients derive names from
path+method (often ugly and unstable across refactors). A stable, deliberate
`operation_id` is the difference between `client.list_products()` and
`client.api_v1_products_get()`.

## 4. Security Schemes — Auth in the Contract

```python
from fastapi.security import HTTPBearer

bearer = HTTPBearer()

@app.post("/products", security=...)
def create_product(credentials: HTTPAuthorizationCredentials = Security(bearer)):
    ...
```

Output:
```
# schema declares a securitySchemes.httpBearer and marks the operation
# -> generated clients know to send the Authorization header
```

Declaring security in the schema means generated clients, mock servers, and
docs all know a token is required — before a single 401 is ever returned.
FastAPI's `HTTPBearer`, `OAuth2PasswordBearer`, and `APIKeyHeader` primitives
emit the right OpenAPI declarations automatically.

## 5. Examples — Making the Contract Concrete

```python
class Product(BaseModel):
    sku: str = Field(examples=["GPU-2000"])
    name: str = Field(examples=["A100 GPU"])
    price_cents: int = Field(gt=0, examples=[150000])
```

Output:
```
# examples appear in /openapi.json -> Swagger UI shows them, tests use them
```

Examples turn an abstract schema into something a reader can immediately
exercise — and they flow into generated test fixtures and documentation.

## 6. Contract Testing Against the Schema

The schema enables contract testing: assert that responses actually match the
declared shapes, that status codes match the declared `responses`, and that
error envelopes match. When schema and runtime disagree, the contract is
broken — and CI should catch it.

## 7. Generating Typed Clients

Real-world tools (`openapi-python-client`, Microsoft Kiota, `openapi-generator`)
parse the schema into full SDKs: typed request/response models, one method per
operation, auth wired in. The exercise shows a miniature generator to make the
mechanism concrete:

```python
def generate_python_client(openapi: dict) -> str:
    lines = ["class InventoryClient:"]
    for path, methods in openapi["paths"].items():
        for method, spec in methods.items():
            op_id = spec.get("operationId", f"{method}_{path}")
            lines.append(f"    def {op_id}(self, base_url: str): ...")
    return "\n".join(lines)
```

Output:
```
class InventoryClient:
    def listProducts(self, base_url: str): ...
    def createProduct(self, base_url: str): ...
```

Because the client is generated, it never drifts from the server: regenerate
on each release and the SDK is always in sync.

## 8. Common Mistakes to Avoid

### Mistake 1: Treating the schema as an afterthought
```python
# WRONG — unset metadata, no tags, no operation_ids
# CORRECT — deliberate title/version/tags/operation_ids; it is the contract
```

### Mistake 2: Auth implemented but not declared
```python
# WRONG — endpoint enforces a token but the schema shows no security scheme
# CORRECT — use Security(...) so the schema declares it and clients send it
```

### Mistake 3: Unstable generated method names
```python
# WRONG — no operation_id; clients get path-derived names that churn
# CORRECT — explicit operation_id per operation
```

### Mistake 4: No examples
```python
# WRONG — schemas with no example values
# CORRECT — Field(examples=[...]) on key fields
```

### Mistake 5: Hand-writing clients
```python
# WRONG — hand-maintained SDK drifts from the API
# CORRECT — generate from the schema in CI; commit the generated code
```

## 9. Best Practices

1. Set title, version, and description on every app.
2. Use tags to group the surface; one group per client class.
3. Give every operation a stable `operation_id`.
4. Declare security schemes in the schema, not just in code.
5. Add examples to every non-obvious field.
6. Generate clients from the schema; never hand-write them.
7. Contract-test responses against the declared schemas in CI.
8. Keep one schema as the source of truth (the compiled one).
9. Version the schema with the API (`info.version`).
10. Review /openapi.json as part of code review.

## 10. Complexity and Cost

| Concern | Cost | Notes |
|---|---|---|
| Schema generation | O(routes + models) at startup | Automatic, cheap |
| Client generation | one-time per release | In CI |
| Contract tests | per endpoint | Small suite, high value |
| Docs hosting | static | Swagger UI serves from the schema |

The schema costs nothing at runtime and buys consistency everywhere else.

## 11. AI Engineering Relevance

**Where this shows up:** every model/LLM API ships a schema that agents and
SDKs consume; structured-output endpoints *are* schemas (see
`09-genai/03-structured-output`).

| Concept here | Used for |
|---|---|
| operation_id | Stable tool names for function-calling agents |
| Security schemes | Declaring API keys for LLM gateway endpoints |
| Examples | Showing agents valid tool-call payloads |
| Generated clients | SDKs for model-serving APIs |
| Contract tests | Verifying structured outputs match declared schemas |

**Scale note:** when the consumers of your API are other programs (agents,
pipelines, SDKs), the schema is the interface that matters most. A clean,
typed, example-rich schema is what makes autonomous consumers reliable.

## 12. Summary

| Concept | Description |
|---|---|
| OpenAPI | The compiled contract generated from your code |
| Tags | Grouping the surface for docs and SDKs |
| operation_id | Stable names for generated client methods |
| Security schemes | Auth declared in the contract |
| Examples | Concrete values for docs and tests |
| Generated clients | SDKs that never drift from the server |

## Quick Reference

| Task | Idiom |
|---|---|
| Metadata | `FastAPI(title=..., version=..., description=...)` |
| Group ops | `tags=["products"]` + `openapi_tags=[...]` |
| Stable names | `operation_id="listProducts"` |
| Declare auth | `Security(HTTPBearer())` |
| Examples | `Field(examples=[...])` |
| Inspect schema | `GET /openapi.json` |
| Generate client | `openapi-python-client generate --url .../openapi.json` |

## Next Steps

Next: **[32 — Async Endpoints Deep](32-async-endpoints-deep-lecture.md)** — the threadpool subtlety.

Continues in: **[09-genai — 03 Structured Output](../../09-genai/lectures/03-structured-output-lecture.md)** — schemas as the LLM contract.

Official docs: <https://spec.openapis.org/oas/v3.1.0.html> · <https://fastapi.tiangolo.com/advanced/generate-clients/>
