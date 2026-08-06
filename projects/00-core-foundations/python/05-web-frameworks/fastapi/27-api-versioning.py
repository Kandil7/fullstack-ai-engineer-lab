"""
27 - API Versioning
=====================
URL path vs header vs media-type versioning, deprecation policy with
Sunset headers, breaking vs additive changes, supporting two versions
in one app.

Run:      python 27-api-versioning.py
Verify:   python 27-api-versioning.py --verify
Reference: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning-a-restful-web-api
"""

from __future__ import annotations

import sys

from fastapi import FastAPI, APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Versioned API", version="2.0.0")

# ============================================================
# 1. URL path versioning — explicit, cacheable, most common
# ============================================================
v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")


class UserV1(BaseModel):
    id: int
    name: str


class UserV2(UserV1):
    email: str | None = None    # additive change: v2 adds a field


USERS = {1: {"id": 1, "name": "ada", "email": "ada@example.com"}}


@v1.get("/users/{user_id}")
def get_user_v1(user_id: int) -> UserV1:
    """v1 returns id + name only."""
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserV1(id=user["id"], name=user["name"])


@v2.get("/users/{user_id}", response_model=UserV2)
def get_user_v2(user_id: int) -> UserV2:
    """v2 adds email. Both versions coexist in one app."""
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserV2(**user)


app.include_router(v1)
app.include_router(v2)

# ============================================================
# 2. Header versioning + deprecation via Sunset header
# ============================================================
SUPPORTED_VERSIONS = {"1", "2"}
DEPRECATED_VERSIONS = {"1"}
SUNSET_DATE = "Sun, 31 Dec 2026 23:59:59 GMT"


@app.get("/api/items", response_model=list[dict])
def get_items(api_version: str = Header(default="1", alias="X-API-Version"),
              response_headers: dict = Depends(lambda: {})):
    """Header-based versioning: the URL stays stable, the header picks v."""
    if api_version not in SUPPORTED_VERSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported version: {api_version}")

    items = [{"id": 1, "name": "item"}]

    # Version 2 adds a field (additive change)
    if api_version == "2":
        for it in items:
            it["active"] = True

    # Deprecation communication lives on the response
    resp = {"items": items}
    if api_version in DEPRECATED_VERSIONS:
        resp["deprecated"] = True
        resp["sunset"] = SUNSET_DATE
    return resp


# ============================================================
# 3. Additive vs breaking changes — the versioning decision table
# ============================================================
print("=" * 60)
print("Breaking vs additive changes:")
print("  ADDITIVE  (safe in v1): new optional field, new endpoint,")
print("            new enum value, relaxed constraint, longer timeout")
print("  BREAKING  (needs v2) : removed field, renamed field, changed type,")
print("            changed status codes, stricter validation, auth changes")
print("=" * 60)


def is_additive(old: dict, new: dict) -> bool:
    """True if every old key still exists with a compatible value."""
    for key, value in old.items():
        if key not in new:
            return False
        if type(value) is not type(new[key]):
            return False
    return True


# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- URL path: explicit and cache-friendly, forever URLs")
print("- Header: URL stability, but clients must remember the header")
print("- Media type (Accept): REST-pure, least common in practice")
print("- Communicate deprecation with Sunset + Deprecation headers")
print("- Prefer additive changes; version only when you must break")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # Path versioning: both versions live
        r1 = client.get("/api/v1/users/1")
        assert r1.status_code == 200, "v1 must exist"
        assert "email" not in r1.json(), "v1 shape is id+name only"
        r2 = client.get("/api/v2/users/1")
        assert r2.status_code == 200
        assert r2.json()["email"] == "ada@example.com", "v2 adds email"

        # 404 shared across versions
        assert client.get("/api/v2/users/999").status_code == 404

        # Header versioning
        r_h1 = client.get("/api/items", headers={"X-API-Version": "1"})
        assert r_h1.status_code == 200
        assert r_h1.json()["deprecated"] is True, "v1 flagged deprecated"
        assert r_h1.json()["sunset"] == SUNSET_DATE
        r_h2 = client.get("/api/items", headers={"X-API-Version": "2"})
        assert r_h2.status_code == 200
        assert r_h2.json()["items"][0]["active"] is True, "v2 adds active"
        assert client.get("/api/items", headers={"X-API-Version": "9"}).status_code == 400

    # Decision table logic
    assert is_additive({"a": 1}, {"a": 1, "b": 2}), "new key is additive"
    assert not is_additive({"a": 1}, {"a": "1"}), "type change is breaking"
    assert not is_additive({"a": 1}, {"b": 1}), "renamed key is breaking"

    print("[OK] 27-api-versioning: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("27-api-versioning:app", host="127.0.0.1", port=8000)
    else:
        _verify()
