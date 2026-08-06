"""
33 - Database Async
=====================
Async SQLAlchemy in requests, session-per-request DI, pool sizing vs
worker count, transaction scope, avoiding pool exhaustion.

Run:      python 33-database-async.py
Verify:   python 33-database-async.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
"""

from __future__ import annotations

import sys

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# In-memory async SQLite via aiosqlite when available; otherwise a pure
# async stub so the file still runs and teaches the DI shape.
try:
    import aiosqlite  # noqa: F401
    HAS_AIOSQLITE = True
except ImportError:
    HAS_AIOSQLITE = False


class Row(BaseModel):
    id: int
    name: str


class RowIn(BaseModel):
    name: str


# ============================================================
# Session-per-request DI — the async connection lifecycle
# ============================================================
class AsyncDB:
    """Minimal async connection holder (aiosqlite-backed when available)."""

    def __init__(self, path: str = ":memory:"):
        self._conn = None
        self.path = path

    async def connect(self) -> None:
        if HAS_AIOSQLITE:
            import aiosqlite
            self._conn = await aiosqlite.connect(self.path)
            await self._conn.execute("CREATE TABLE IF NOT EXISTS rows (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
            await self._conn.commit()
        else:
            self._conn = object()   # stub
            self._rows: list[Row] = []

    async def close(self) -> None:
        if self._conn is not None and HAS_AIOSQLITE:
            await self._conn.close()
        self._conn = None

    async def insert(self, name: str) -> Row:
        if HAS_AIOSQLITE:
            cur = await self._conn.execute("INSERT INTO rows (name) VALUES (?)", (name,))
            await self._conn.commit()
            return Row(id=cur.lastrowid, name=name)
        row = Row(id=len(self._rows) + 1, name=name)
        self._rows.append(row)
        return row

    async def get(self, row_id: int) -> Row | None:
        if HAS_AIOSQLITE:
            cur = await self._conn.execute("SELECT id, name FROM rows WHERE id = ?", (row_id,))
            row = await cur.fetchone()
            return Row(id=row[0], name=row[1]) if row else None
        return next((r for r in self._rows if r.id == row_id), None)


db = AsyncDB()


async def get_db() -> AsyncDB:
    """Session-per-request: one connection per request, closed after."""
    await db.connect()
    try:
        yield db
    finally:
        await db.close()


app = FastAPI(title="Async DB Demo", lifespan=None)


# Simulated lifespan: connect once (real apps connect at startup)
import asyncio  # noqa: E402


@app.on_event("startup")
async def startup() -> None:
    await db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await db.close()


# ============================================================
# Async endpoints: await the DB, never block the loop
# ============================================================
@app.post("/rows", status_code=201, response_model=Row)
async def create_row(body: RowIn, d: AsyncDB = Depends(get_db)) -> Row:
    return await d.insert(body.name)


@app.get("/rows/{row_id}", response_model=Row)
async def get_row(row_id: int, d: AsyncDB = Depends(get_db)) -> Row:
    row = await d.get(row_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Row not found")
    return row


# ============================================================
# Pool sizing math — the rule that prevents exhaustion
# ============================================================
def recommend_pool_size(workers: int, concurrency_per_worker: int = 10) -> dict:
    """Pool sizing rule: pool_size ~= workers x concurrent requests/worker.

    Too small -> 503s under load. Too large -> DB connections idle and
    the database runs out of file descriptors.
    """
    return {
        "uvicorn_workers": workers,
        "pool_size": max(5, workers * concurrency_per_worker),
        "max_overflow": max(2, workers * concurrency_per_worker // 2),
        "reason": "pool must cover peak concurrent requests across workers",
    }


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- Async DB calls (await) keep the event loop free")
print("- Session-per-request DI: acquire, yield, close in finally")
print("- Pool sizing: workers x concurrency, not workers x 1")
print("- Transaction scope: begin/commit/rollback per request")
print("- Pool exhaustion looks like 503s and timeout storms")
print("=" * 60)
print(recommend_pool_size(workers=4))


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        r = client.post("/rows", json={"name": "alpha"})
        assert r.status_code == 201
        row_id = r.json()["id"]
        assert r.json()["name"] == "alpha"

        r = client.get(f"/rows/{row_id}")
        assert r.status_code == 200
        assert r.json()["name"] == "alpha"

        assert client.get("/rows/999").status_code == 404

    # Pool sizing sanity
    rec = recommend_pool_size(4)
    assert rec["pool_size"] == 40
    assert rec["max_overflow"] == 20

    print("[OK] 33-database-async: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("33-database-async:app", host="127.0.0.1", port=8000)
    else:
        _verify()
