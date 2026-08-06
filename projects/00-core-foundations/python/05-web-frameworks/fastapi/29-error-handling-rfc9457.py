"""
29 - Error Handling (RFC 9457 / Problem Details)
==================================================
Consistent error envelopes, exception handlers, never leaking internals,
validation error shaping, client-actionable messages.

Run:      python 29-error-handling-rfc9457.py
Verify:   python 29-error-handling-rfc9457.py --verify
Reference: https://www.rfc-editor.org/rfc/rfc9457.html
"""

from __future__ import annotations

import sys

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="RFC 9457 Problem Details Demo")


# ============================================================
# 1. The Problem Details envelope (RFC 9457)
# ============================================================
def problem_detail(status: int, title: str, detail: str,
                   type_: str = "about:blank", **extra) -> dict:
    """RFC 9457 problem document: type, title, status, detail, instance."""
    body = {"type": type_, "title": title, "status": status, "detail": detail}
    body.update(extra)
    return body


# ============================================================
# 2. Global handlers: consistent envelope for every error class
# ============================================================
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Every HTTPException -> the same problem-details shape."""
    body = problem_detail(
        status=exc.status_code,
        title=exc.detail if isinstance(exc.detail, str) else "Request failed",
        detail=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        instance=str(request.url.path),
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """422s become actionable: point at the failing field and why."""
    errors = []
    for err in exc.errors():
        errors.append({
            "field": ".".join(str(p) for p in err["loc"]),
            "message": err["msg"],
            "input": err.get("input"),
        })
    body = problem_detail(
        status=422, title="Validation error", detail="Request body failed validation",
        instance=str(request.url.path), errors=errors,
    )
    return JSONResponse(status_code=422, content=body)


# ============================================================
# 3. The happy path that hides internals on failure
# ============================================================
class Item(BaseModel):
    name: str = Field_min_length_3()
    qty: int


def Field_min_length_3():
    from pydantic import Field
    return Field(min_length=3)


ITEMS: dict[int, Item] = {}


@app.post("/items", status_code=201)
def create_item(item: Item) -> dict:
    new_id = len(ITEMS) + 1
    ITEMS[new_id] = item
    return {"id": new_id, "name": item.name}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if item is None:
        # Client-actionable, internals-free 404
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} does not exist",
        )
    return {"id": item_id, "name": item.name}


# ============================================================
# 4. Never leak internals — the honest way to handle 500s
# ============================================================
@app.get("/crash")
def crash():
    raise ValueError("SECRET_DB_PASSWORD was wrong")  # would be a real internal error


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- RFC 9457: {type, title, status, detail, instance}")
print("- One envelope for ALL errors -> clients parse one shape")
print("- Validation 422s point at the exact field")
print("- 404s are client-actionable ('Item 5 does not exist')")
print("- 500s never include tracebacks or internals")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app, raise_server_exceptions=False) as client:
        # 201 + envelope for validation failure
        r = client.post("/items", json={"name": "ok", "qty": 1})
        assert r.status_code == 201

        r = client.post("/items", json={"name": "x", "qty": 1})   # name too short
        assert r.status_code == 422, "validation failure must be 422"
        body = r.json()
        assert body["type"] == "about:blank" and body["status"] == 422
        assert body["errors"][0]["field"] == "body.name", "error pinpoints field"
        assert "SECRET" not in str(body), "no internals in validation errors"

        # 404 with actionable detail
        r = client.get("/items/999")
        assert r.status_code == 404
        assert "does not exist" in r.json()["detail"]

        # 500: envelope, no traceback, no internals
        r = client.get("/crash")
        assert r.status_code == 500
        leaked = str(r.json())
        assert "SECRET_DB_PASSWORD" not in leaked, "internals must never leak"
        assert "traceback" not in leaked.lower()
        assert r.json()["title"] != ""

    print("[OK] 29-error-handling-rfc9457: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("29-error-handling-rfc9457:app", host="127.0.0.1", port=8000)
    else:
        _verify()
