"""
28 - Pagination and Filtering
===============================
Offset vs keyset (cursor) pagination and why offset breaks at scale,
sorting, filter DSLs, Link headers, and the cost of total-count.

Run:      python 28-pagination-and-filtering.py
Verify:   python 28-pagination-and-filtering.py --verify
Reference: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#pagination
"""

from __future__ import annotations

import sys
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Pagination Demo")

# Simulated large dataset: 100k records in "database order" (a stable key)
N_ROWS = 100_000
DB = [{"id": i, "name": f"item-{i:05d}", "score": (i * 37) % 1000} for i in range(N_ROWS)]


class Page(BaseModel):
    items: list[dict[str, Any]]
    next_cursor: str | None = None
    has_more: bool = False
    total: int | None = None


# ============================================================
# 1. Offset pagination — the classic, and its scaling problem
# ============================================================
@app.get("/api/offset", response_model=Page)
def offset_page(limit: int = Query(20, ge=1, le=100),
                offset: int = Query(0, ge=0)) -> Page:
    """Offset/limit. Fine for small tables; O(offset) scans at scale."""
    items = DB[offset:offset + limit]
    return Page(items=items,
                has_more=offset + limit < len(DB),
                total=len(DB))


# ============================================================
# 2. Keyset (cursor) pagination — stable under writes and scale
# ============================================================
@app.get("/api/keyset", response_model=Page)
def keyset_page(limit: int = Query(20, ge=1, le=100),
                cursor: str | None = None) -> Page:
    """Cursor = opaque token encoding the last-seen id.

    WHERE id > :last ORDER BY id LIMIT :n — an index range scan, O(limit),
    independent of how deep into the table you are. Robust to inserts
    and deletes between pages.
    """
    start = int(cursor) if cursor else -1
    items = [r for r in DB if r["id"] > start][:limit]
    last_id = items[-1]["id"] if items else start
    return Page(items=items,
                next_cursor=str(last_id) if len(items) == limit else None,
                has_more=len(items) == limit)


# ============================================================
# 3. Filtering — a small, explicit filter DSL
# ============================================================
@app.get("/api/search", response_model=Page)
def search(name_contains: str | None = Query(None),
           min_score: int | None = Query(None, ge=0, le=999),
           sort: str = Query("id", pattern="^(id|score|name)$"),
           limit: int = Query(20, ge=1, le=100)) -> Page:
    """Explicit query parameters: readable, documentable, safe.

    Alternative DSLs (filters=score:gt:100) trade readability for
    generality; use them only when the filter space is truly open.
    """
    rows = DB
    if name_contains:
        rows = [r for r in rows if name_contains in r["name"]]
    if min_score is not None:
        rows = [r for r in rows if r["score"] >= min_score]

    rows = sorted(rows, key=lambda r: r[sort])
    items = rows[:limit]
    return Page(items=items, has_more=len(rows) > limit, total=len(rows))


# ============================================================
# 4. Link headers — the standard pagination contract
# ============================================================
def build_link_headers(base: str, page: Page, limit: int) -> dict[str, str]:
    """RFC 8288 Link headers: rel=next / prev / first / last."""
    links = []
    if page.next_cursor:
        links.append(f'<{base}?limit={limit}&cursor={page.next_cursor}>; rel="next"')
    if links:
        return {"Link": ", ".join(links)}
    return {}


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- Offset: simple, but O(offset) — breaks past ~10k rows")
print("- Keyset/cursor: index range scan, O(limit) — scale-friendly")
print("- Keyset needs a stable sort key (unique, ordered)")
print("- Explicit query params beat filter-DSLs unless filters are open")
print("- total_count is expensive: skip it on deep pages")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # Offset pagination
        r = client.get("/api/offset", params={"limit": 3, "offset": 0})
        body = r.json()
        assert r.status_code == 200
        assert [i["id"] for i in body["items"]] == [0, 1, 2]
        assert body["total"] == N_ROWS

        # Keyset: walk several pages and confirm no gaps/overlaps
        seen: list[int] = []
        cursor = None
        for _ in range(5):
            params = {"limit": 7}
            if cursor:
                params["cursor"] = cursor
            page = client.get("/api/keyset", params=params).json()
            ids = [i["id"] for i in page["items"]]
            assert ids, "every page must return rows until exhausted"
            seen.extend(ids)
            cursor = page["next_cursor"]
            if not page["has_more"]:
                break
        assert seen == list(range(len(seen))), "keyset pages must be gapless and ordered"

        # Keyset deep-page cost: far page returns instantly with the same shape
        deep = client.get("/api/keyset", params={"limit": 5, "cursor": "99990"})
        assert deep.json()["items"][0]["id"] == 99991

        # Filtering
        r = client.get("/api/search", params={"min_score": 990, "limit": 5, "sort": "score"})
        assert all(i["score"] >= 990 for i in r.json()["items"])
        r = client.get("/api/search", params={"name_contains": "item-00001"})
        assert len(r.json()["items"]) == 1, "name filter is exact substring"

        # Link headers
        base = "/api/keyset"
        page = client.get("/api/keyset", params={"limit": 2}).json()
        headers = build_link_headers(base, page, 2)
        assert '"next"' in headers.get("Link", ""), "next link must be present"

    print("[OK] 28-pagination-and-filtering: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("28-pagination-and-filtering:app", host="127.0.0.1", port=8000)
    else:
        _verify()
