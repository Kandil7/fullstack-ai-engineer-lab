# Error Handling (RFC 9457) — Glossary 29

Companion lecture: `29-error-handling-rfc9457-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 422 | HTTP status | Unprocessable content — validation failed |
| detail | Envelope | Human-readable specifics of the error |
| Envelope | Design | The single JSON shape every error response uses |
| Exception handler | Mechanism | Registered function converting an exception class to a response |
| HTTPException | Mechanism | The exception endpoints raise for HTTP-level failures |
| instance | Envelope | The URL that produced the error |
| Internal leak | Failure | Exposing tracebacks, secrets, or internals in responses |
| Problem details | Standard | RFC 9457 envelope: type, title, status, detail, instance |
| RequestValidationError | Mechanism | Raised when request data fails schema validation |
| Retry-After | Header | Server tells the client when to retry (429/503) |
| status | Envelope | The HTTP status code in the body |
| title | Envelope | Short human-readable error name |
| traceback | Failure | The internal stack trace that must never be returned |
| type | Envelope | URI identifying the error class |
| Actionable error | Design | A message telling the client what to fix |
| raise_server_exceptions | Testing | TestClient flag exposing 500s for assertion |

## Detailed Definitions

### 422
**Definition**: HTTP status "Unprocessable Entity" — the request was parsed but
failed validation. FastAPI returns it when a body fails a Pydantic schema.
**Related**: RequestValidationError

### detail
**Definition**: The RFC 9457 member carrying human-readable, client-actionable
specifics ("Item 999 does not exist").
**Related**: Problem details

### Envelope
**Definition**: The single, consistent JSON shape every error response uses, so
clients write one parser.
**Related**: Problem details

### Exception handler
**Definition**: A function registered with `@app.exception_handler(ExceptionClass)`
that converts a raised exception into a response.
**Example**:
```python
@app.exception_handler(HTTPException)
async def handle(request, exc): ...
```
**Related**: HTTPException

### HTTPException
**Definition**: FastAPI's exception for HTTP-level failures; endpoints raise it
with a status code and detail.
**Example**:
```python
raise HTTPException(404, "Item 999 does not exist")
```
**Related**: Exception handler

### instance
**Definition**: The RFC 9457 member identifying the specific URL that failed —
correlates errors to requests.
**Related**: Problem details

### Internal leak
**Definition**: Returning tracebacks, secrets, or internal state in an error
body — a security and operational failure.
**Related**: traceback

### Problem details
**Definition**: RFC 9457's standard error envelope with members `type`,
`title`, `status`, `detail`, `instance`, plus extensions.
**Example**:
```python
{"type": "about:blank", "title": "Not found", "status": 404,
 "detail": "Item 5 does not exist", "instance": "/items/5"}
```
**Related**: Envelope

### RequestValidationError
**Definition**: Raised by FastAPI when request data fails schema validation;
a global handler reshapes it into a 422 with field-level errors.
**Related**: 422

### Retry-After
**Definition**: A response header telling clients how many seconds to wait
before retrying, used on 429 and 503.
**Example**:
```python
raise HTTPException(429, headers={"Retry-After": "2"})
```
**Related**: Idempotency

### status
**Definition**: The RFC 9457 member holding the HTTP status code, mirrored from
the response.
**Related**: Problem details

### title
**Definition**: The RFC 9457 member giving a short human-readable name for the
error class.
**Related**: Problem details

### traceback
**Definition**: The Python stack trace of an exception — logged server-side,
never returned to clients.
**Related**: Internal leak

### type
**Definition**: The RFC 9457 member identifying the error class, usually a URI;
`about:blank` for generic errors.
**Related**: Problem details

### Actionable error
**Definition**: An error message telling the client what to fix (field, ID,
constraint) rather than a vague "something went wrong".
**Related**: detail

### raise_server_exceptions
**Definition**: A TestClient constructor flag; `False` lets tests assert on 500
bodies instead of re-raising the server exception.
**Example**:
```python
with TestClient(app, raise_server_exceptions=False) as client:
    r = client.get("/crash")
    assert r.status_code == 500
```
**Related**: Exception handler

## Key Concepts Summary

### The envelope
- type, title, status, detail, instance — one shape for every error.
- Extensions (errors: [...]) carry structured specifics.

### The handlers
- HTTPException handler for 4xx/5xx raised in endpoints.
- RequestValidationError handler for schema failures (422).
- Unhandled exceptions become leak-free 500s.

### The discipline
- Actionable messages; never leak tracebacks or secrets.
- Test error responses as contract.
- 4xx = client can fix; 5xx = we own it.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The standard RFC 9457 error envelope — ___
2. Raised when a request body fails validation — ___
3. The URL that produced the error — ___
4. Status for failed validation — ___
5. Header telling the client when to retry — ___
6. A message telling the client what to fix — ___
7. Registered function converting exceptions to responses — ___
8. TestClient flag for asserting on 500s — ___

**Answers:** 1-problem details, 2-RequestValidationError, 3-instance, 4-422,
5-Retry-After, 6-actionable error, 7-exception handler, 8-raise_server_exceptions
