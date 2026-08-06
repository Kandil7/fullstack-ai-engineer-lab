# FastAPI — 29: Error Handling — RFC 9457 Problem Details

Companion exercise: `29-error-handling-rfc9457.py`

---

## Topic Overview

Errors are part of every API's contract. RFC 9457 (Problem Details for HTTP
APIs) standardizes the error envelope so that clients — and the teams
debugging them — parse one shape instead of guessing. This topic covers the
discipline behind professional error handling: one envelope for every error
class, exception handlers that never leak internals, validation errors that
point at the exact field, 404s that are actionable, and 500s that tell
operators what broke without telling attackers how.

The guiding principle: **the error response is a product.** A client-actionable
error (which field, what to fix) saves hours; a leaked traceback costs a
security review.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build an RFC 9457 problem-details envelope.
2. Register global handlers for HTTPException and RequestValidationError.
3. Shape 422 validation errors to point at exact fields.
4. Write client-actionable 404 details.
5. Ensure 500s never leak tracebacks or internals.
6. Keep one error shape across the whole API.
7. Add `instance` and custom fields to problem documents.
8. Test error responses as part of the contract.

## Prerequisites

| Need | Where |
|---|---|
| Exception handling basics | `23-exception-handling.py` |
| Request validation / 422 | `05-request-body.py` |
| Pydantic v2 | `26-pydantic-v2-deep.py` |

## 1. The RFC 9457 Envelope

```python
def problem_detail(status, title, detail, type_="about:blank", **extra):
    body = {"type": type_, "title": title, "status": status, "detail": detail}
    body.update(extra)
    return body
```

Output:
```
{"type": "about:blank", "title": "Not found", "status": 404,
 "detail": "Item 5 does not exist", "instance": "/items/5"}
```

Standard members: `type` (a URI identifying the error class), `title`
(short human title), `status` (HTTP code), `detail` (human-readable specifics),
`instance` (which URL failed). Extensions (like `errors: [...]`) are allowed.

## 2. One Envelope for Every Error

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code,
                        content=problem_detail(
                            status=exc.status_code, title="Request failed",
                            detail=exc.detail, instance=str(request.url.path)))
```

Output:
```
# GET /items/999 -> 404 {"type": "about:blank", "title": "...", "detail": "Item 999 does not exist"}
```

Every `HTTPException` — from any endpoint — flows through this handler and
comes out the same shape. Clients write one parser, not one per endpoint.

## 3. Actionable Validation Errors (422)

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = [{"field": ".".join(str(p) for p in e["loc"]),
               "message": e["msg"], "input": e.get("input")} for e in exc.errors()]
    return JSONResponse(status_code=422,
                        content=problem_detail(422, "Validation error",
                                               "Request body failed validation",
                                               errors=errors))
```

Output:
```
# POST /items {"name": "x"} -> 422
# {"errors": [{"field": "body.name", "message": "String should have at least 3 characters"}]}
```

The field path (`body.name`) tells the client exactly where the problem is —
the difference between an error a client can fix and one it can only display.

## 4. Client-Actionable 404s

```python
raise HTTPException(status_code=404, detail=f"Item {item_id} does not exist")
```

Output:
```
# {"detail": "Item 999 does not exist"}
```

"Item 999 does not exist" is actionable — the client knows the ID was wrong.
"A resource was not found" is not. Details belong in `detail`; never put
implementation specifics there.

## 5. 500s That Never Leak

An unhandled exception becomes a 500. The envelope must exist, and the body
must not contain the traceback or internal state:

- Log the full traceback server-side (structured, with a request ID).
- Return only `{"type": ..., "title": "Internal server error", "status": 500}`.
- Never echo exception messages that may contain secrets.

In the exercise, `raise_server_exceptions=False` on the test client lets the
test assert exactly this.

## 6. Common Mistakes to Avoid

### Mistake 1: Leaking internals in errors
```python
# WRONG — exception message may contain connection strings, paths
raise HTTPException(500, str(original_exception))
# CORRECT — log it; return a generic envelope
```

### Mistake 2: Different shapes per endpoint
```python
# WRONG — one endpoint returns {"error": "..."}, another {"msg": "..."}
# CORRECT — one problem-details handler for every error class
```

### Mistake 3: Unactionable messages
```python
# WRONG — "Something went wrong" with no field, no id, no guidance
# CORRECT — "Item 999 does not exist" / field-specific 422 details
```

### Mistake 4: Raising ValidationError by hand
```python
# WRONG — hand-rolled ValidationError bypasses the 422 handler cleanly
# CORRECT — let schemas validate; handle RequestValidationError globally
```

### Mistake 5: No tests for error responses
```python
# WRONG — only happy-path tests; errors drift out of the contract
# CORRECT — assert the envelope for 400/404/422/500 in CI
```

## 7. Best Practices

1. One envelope (RFC 9457) for all errors.
2. Global handlers per exception class — never per-endpoint.
3. Point validation errors at exact fields with the input shown.
4. Make 404/409 details actionable.
5. Never leak tracebacks or secrets; log them server-side.
6. Add `instance` so operators can correlate failures to URLs.
7. Keep custom fields (errors, code) documented in the schema.
8. Test error responses like any other contract.
9. Use `exc.status_code` from the exception, not a hardcoded value.
10. Distinguish 4xx (client can fix) from 5xx (we own it) clearly.

## 8. Complexity and Cost

| Error class | Handling cost | Notes |
|---|---|---|
| HTTPException | O(1) handler | Single global handler |
| RequestValidationError | O(errors) | One entry per failing field |
| Unhandled 500 | O(log) server-side | Envelope is cheap; logging is the cost |
| Error testing | per-case | Include in CI suite |

Error handling is cheap — the cost is discipline, not compute.

## 9. AI Engineering Relevance

**Where this shows up:** LLM and model-serving APIs have brutal error
surfaces — invalid structured outputs, rate limits, provider timeouts. A
consistent problem-details envelope is what lets agents and clients recover.

| Concept here | Used for |
|---|---|
| 422 field errors | Telling callers which LLM output field failed validation |
| 429 + Retry-After | Provider rate-limit signalling |
| Actionable 404 | Missing documents in retrieval APIs |
| No-leak 500 | Never exposing prompt templates or keys |
| instance | Correlating failures to requests in tracing |

**Scale note:** at high QPS, error responses are a measurable share of
traffic. A well-shaped error that clients handle automatically (retry,
fallback) is far cheaper than an ambiguous one that pages an on-call engineer.

## 10. Summary

| Concept | Description |
|---|---|
| RFC 9457 | The standard problem-details envelope |
| Global handlers | One shape per exception class |
| 422 shaping | Field-level, actionable validation errors |
| 404 detail | Actionable, client-fixable messages |
| 500 hygiene | Log server-side; leak nothing |
| instance | URL correlation in every error |

## 11. Quick Reference

| Task | Idiom |
|---|---|
| Envelope | `{"type", "title", "status", "detail", "instance"}` |
| HTTP errors | `@app.exception_handler(HTTPException)` |
| Validation errors | `@app.exception_handler(RequestValidationError)` |
| Actionable 404 | `HTTPException(404, f"Item {id} does not exist")` |
| Rate limited | `HTTPException(429, headers={"Retry-After": "2"})` |
| Test 500 | `TestClient(app, raise_server_exceptions=False)` |

## 12. Next Steps

Next: **[30 — Idempotency and Retries](30-idempotency-and-retries-lecture.md)** — making retries safe.

Continues in: **[27 — API Versioning](27-api-versioning-lecture.md)** — the contract that errors describe.

Official docs: <https://www.rfc-editor.org/rfc/rfc9457.html> · <https://fastapi.tiangolo.com/tutorial/handling-errors/>
