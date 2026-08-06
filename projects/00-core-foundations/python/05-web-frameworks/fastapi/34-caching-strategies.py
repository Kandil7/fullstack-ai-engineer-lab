"""
34 - Caching Strategies
=========================
Response caching, ETag/If-None-Match, Cache-Control, Redis-backed caching,
cache-key design, invalidation, per-user vs shared.

Run:      python 34-caching-strategies.py
Verify:   python 34-caching-strategies.py --verify
Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
"""

from __future__ import annotations

import hashlib
import sys
import time

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Caching Demo")

# ============================================================
# 1. ETag + If-None-Match — conditional requests (HTTP-level cache)
# ============================================================
DATA_VERSION = 1
_LAST_UPDATED = time.time()


def etag_for(payload: str) -> str:
    return hashlib.sha1(payload.encode()).hexdigest()[:16]


@app.get("/catalog")
def catalog(request: Request) -> Response:
    """ETag lets clients/CDNs validate: 304 when nothing changed."""
    body = {
        "version": DATA_VERSION,
        "items": ["gpu", "cpu", "ram"],
        "generated_at": round(_LAST_UPDATED, 2),
    }
    payload = repr(sorted(body.items(), key=lambda kv: kv[0]))
    etag = etag_for(payload)

    # Client sends back the ETag it has; if it matches, 304 Not Modified
    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304)

    return Response(
        content=__import__("json").dumps(body),
        media_type="application/json",
        headers={"ETag": etag, "Cache-Control": "private, max-age=60"},
    )


# ============================================================
# 2. Cache-Control policy — the decision table
# ============================================================
CACHE_POLICIES = {
    "public": "shared cache: CDN/proxies may store",
    "private": "only the browser may store",
    "no-store": "never store (auth, personal data)",
    "no-cache": "must revalidate with the server before reuse",
    "max-age=60": "fresh for 60s without asking",
}


# ============================================================
# 3. Server-side cache (in-memory) with TTL and key design
# ============================================================
class MemoryCache:
    def __init__(self, ttl: float = 10.0):
        self._store: dict[str, tuple[float, object]] = {}
        self.ttl = ttl

    def get(self, key: str) -> object | None:
        hit = self._store.get(key)
        if hit is None:
            return None
        ts, value = hit
        if time.time() - ts > self.ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: object) -> None:
        self._store[key] = (time.time(), value)


cache = MemoryCache(ttl=10)


def expensive_compute(query: str) -> dict:
    """Stand-in for a slow DB search / model call."""
    time.sleep(0.05)
    return {"query": query, "hits": 100}


@app.get("/search")
def search(q: str) -> dict:
    """Cache-aside: check cache -> compute -> store. Key = the full request
    identity so different queries never collide."""
    key = f"search:{q.strip().lower()}"
    cached = cache.get(key)
    if cached is not None:
        return {"source": "cache", **cached}
    result = expensive_compute(q)
    cache.set(key, result)
    return {"source": "compute", **result}


# ============================================================
# 4. Per-user vs shared — the auth pitfall
# ============================================================
class UserScoped:
    """Private data must be keyed by user OR marked no-store.

    Never serve user A's cached dashboard to user B. The two options:
    1) key includes user_id and responses are Cache-Control: private
    2) no-store entirely for highly sensitive data
    """

    def __init__(self):
        self._store: dict[str, dict] = {}

    def get_dashboard(self, user_id: int) -> dict:
        key = f"dashboard:user:{user_id}"
        if key not in self._store:
            self._store[key] = {"user": user_id, "balance": 100 + user_id}
        return self._store[key]


user_scoped = UserScoped()


@app.get("/dashboard/{user_id}")
def dashboard(user_id: int, response: Response) -> dict:
    response.headers["Cache-Control"] = "private, max-age=5"
    return user_scoped.get_dashboard(user_id)


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- ETag + If-None-Match: 304s save bandwidth, not compute")
print("- Cache-Control: public/private/no-store per data class")
print("- Cache-aside: check -> compute -> store with a TTL")
print("- Cache keys must encode the FULL request identity")
print("- Per-user data: private or user-scoped keys, never shared")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # ETag flow: first 200 with ETag, then 304 with the same ETag
        r1 = client.get("/catalog")
        assert r1.status_code == 200
        etag = r1.headers["etag"]
        assert etag, "response must carry an ETag"

        r2 = client.get("/catalog", headers={"If-None-Match": etag})
        assert r2.status_code == 304, "matching If-None-Match must 304"

        # Cache-aside: first compute, then cache hit
        s1 = client.get("/search", params={"q": "GPU"}).json()
        assert s1["source"] == "compute"
        s2 = client.get("/search", params={"q": "GPU"}).json()
        assert s2["source"] == "cache", "repeat query must hit cache"

        # Keys distinguish queries
        s3 = client.get("/search", params={"q": "CPU"}).json()
        assert s3["source"] == "compute", "different query must not collide"

        # Per-user isolation
        d1 = client.get("/dashboard/1").json()
        d2 = client.get("/dashboard/2").json()
        assert d1["user"] == 1 and d2["user"] == 2, "users never share"

        # Policy table sanity
        assert CACHE_POLICIES["no-store"] and CACHE_POLICIES["private"]

    print("[OK] 34-caching-strategies: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("34-caching-strategies:app", host="127.0.0.1", port=8000)
    else:
        _verify()
