# OpenAPI and Clients — Glossary 31

Companion lecture: `31-openapi-and-clients-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Contract | Concept | The OpenAPI schema as the authoritative API description |
| Contract testing | Testing | Asserting responses match declared schemas |
| Examples | Schema | Concrete field values for docs and test fixtures |
| Generated client | Tooling | An SDK produced from the OpenAPI document |
| HTTPBearer | Security | FastAPI primitive for bearer-token auth schemes |
| Info | Schema | The OpenAPI metadata block (title, version, description) |
| Mock server | Tooling | A server generated from the schema for development |
| OpenAPI | Standard | The machine-readable API description format |
| operation_id | Schema | The stable name of an operation for generated clients |
| openapi.json | Schema | The compiled document served by FastAPI |
| Paths | Schema | The OpenAPI block mapping URLs to operations |
| Security scheme | Schema | Declared auth requirement (bearer, apiKey, oauth2) |
| Swagger UI | Tooling | Interactive docs rendered from the schema |
| Tags | Schema | Groupings organizing operations in docs and SDKs |
| Typed client | Tooling | SDK with compile-time request/response types |
| Schema drift | Failure | Runtime behavior diverging from the declared contract |

## Detailed Definitions

### Contract
**Definition**: The OpenAPI document as the authoritative, machine-readable
description of the API — what clients, tests, and SDKs all agree on.
**Related**: OpenAPI, openapi.json

### Contract testing
**Definition**: Tests asserting that actual responses and status codes match
the declared schemas, catching drift between code and contract.
**Related**: Schema drift

### Examples
**Definition**: Concrete sample values attached to fields via
`Field(examples=[...])`; they appear in docs and feed generated test fixtures.
**Example**:
```python
sku: str = Field(examples=["GPU-2000"])
```
**Related**: Schema

### Generated client
**Definition**: An SDK produced by tools (openapi-python-client, Kiota) from
the OpenAPI document — typed, versioned, and never drifting by hand.
**Related**: Typed client

### HTTPBearer
**Definition**: A FastAPI security primitive (`fastapi.security.HTTPBearer`)
that enforces bearer tokens at runtime and declares the scheme in OpenAPI.
**Example**:
```python
credentials: HTTPAuthorizationCredentials = Security(bearer)
```
**Related**: Security scheme

### Info
**Definition**: The OpenAPI metadata block: title, version, description,
contact — set via `FastAPI(title=..., version=...)`.
**Related**: OpenAPI

### Mock server
**Definition**: A development server generated from the schema that returns
example-shaped responses before the real API exists.
**Related**: Generated client

### OpenAPI
**Definition**: The standardized format (currently 3.x) describing REST APIs
machine-readably: paths, operations, schemas, security.
**Related**: openapi.json

### operation_id
**Definition**: The schema field naming an operation; generated clients use it
as the method name, so a stable id yields stable SDKs.
**Example**:
```python
@app.get("/products", operation_id="listProducts")
```
**Related**: Generated client

### openapi.json
**Definition**: The compiled OpenAPI document FastAPI serves at `/openapi.json`,
generated from routes and models.
**Related**: OpenAPI

### Paths
**Definition**: The OpenAPI block mapping URL paths to their operations and
methods.
**Related**: OpenAPI

### Security scheme
**Definition**: The declared authentication requirement (bearer, apiKey,
oauth2) attached to operations and listed in `components.securitySchemes`.
**Related**: HTTPBearer

### Swagger UI
**Definition**: The interactive documentation page rendered from the schema,
allowing exploration and request testing in the browser.
**Related**: OpenAPI

### Tags
**Definition**: Named groupings applied to operations (`tags=["products"]`)
that organize docs and often map one-to-one to generated client classes.
**Related**: Paths

### Typed client
**Definition**: A generated SDK with compile-time request/response models and
one method per operation — no stringly-typed API calls.
**Related**: Generated client

### Schema drift
**Definition**: The divergence between declared schemas and actual runtime
behavior — caught by contract testing and code review of /openapi.json.
**Related**: Contract testing

## Key Concepts Summary

### The schema is the surface
- Code is the source; /openapi.json is the compiled contract.
- Tags, operation_ids, and examples shape the generated SDK.
- Swagger UI, mock servers, and tests all consume the same document.

### Security in the contract
- Use Security(...) primitives so auth is declared, not just enforced.
- Declared schemes mean generated clients send tokens automatically.

### Consistency
- Generate clients in CI; never hand-maintain an SDK.
- Contract-test responses against the schema.
- Review /openapi.json in code review.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The machine-readable API description format — ___
2. Stable operation name for generated clients — ___
3. Concrete sample values attached to fields — ___
4. The metadata block (title, version) — ___
5. Declared auth requirement on an operation — ___
6. Interactive docs rendered from the schema — ___
7. Groupings organizing operations — ___
8. Runtime diverging from the declared contract — ___

**Answers:** 1-OpenAPI, 2-operation_id, 3-examples, 4-info, 5-security scheme,
6-Swagger UI, 7-tags, 8-schema drift
