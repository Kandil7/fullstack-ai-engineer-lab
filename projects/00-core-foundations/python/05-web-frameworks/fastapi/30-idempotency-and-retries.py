"""
30 - Idempotency and Retries
==============================
Idempotency keys, safe vs unsafe methods, at-least-once delivery reality,
dedup storage, Retry-After, exactly-once as a fiction.

Run:      python 30-idempotency-and-retries.py
Verify:   python 30-idempotency-and-retries.py --verify
Reference: https://stripe.com/docs/api/idempotent_requests
"""

from __future__ import annotations

import sys
import threading
import uuid

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Idempotency Demo")

# In-memory idempotency store: key -> (status, response, attempt_count)
_IDEMPOTENCY: dict[str, dict] = {}
_LOCK = threading.Lock()
_CHARGES: list[dict] = []


class ChargeRequest(BaseModel):
    amount_cents: int = 1


class ChargeResponse(BaseModel):
    charge_id: str
    amount_cents: int
    status: str
    deduplicated: bool = False
    attempts: int = 1


# ============================================================
# 1. The problem: retries cause duplicate side effects
# ============================================================
@app.post("/naive/charges")
def naive_charge(body: ChargeRequest):
    """No idempotency: a client retry creates a SECOND charge."""
    charge_id = str(uuid.uuid4())
    _CHARGES.append(charge_id)
    return {"charge_id": charge_id, "amount_cents": body.amount_cents}


# ============================================================
# 2. The fix: Idempotency-Key header + dedup store
# ============================================================
@app.post("/charges", response_model=ChargeResponse, status_code=201)
def charge(body: ChargeRequest,
           idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    """At-least-once delivery made safe: same key -> same result, once."""
    if not idempotency_key:
        raise HTTPException(status_code=400,
                            detail="Idempotency-Key header is required for POST /charges")

    with _LOCK:
        existing = _IDEMPOTENCY.get(idempotency_key)
        if existing is not None:
            # Replay: return the ORIGINAL response, mark the dedup
            existing["attempts"] += 1
            return ChargeResponse(
                charge_id=existing["charge_id"],
                amount_cents=existing["amount_cents"],
                status=existing["status"],
                deduplicated=True,
                attempts=existing["attempts"],
            )

        # First attempt: do the side effect ONCE
        charge_id = str(uuid.uuid4())
        _CHARGES.append(charge_id)
        entry = {"charge_id": charge_id, "amount_cents": body.amount_cents,
                 "status": "succeeded", "attempts": 1}
        _IDEMPOTENCY[idempotency_key] = entry
        return ChargeResponse(**entry)


# ============================================================
# 3. Safe vs unsafe methods — the retry rule
# ============================================================
SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def can_retry(method: str, has_idempotency_key: bool) -> tuple[bool, str]:
    """GET retries are free; POST/PUT/DELETE retries need a key."""
    if method in SAFE_METHODS:
        return True, "safe method: retry freely"
    if has_idempotency_key:
        return True, "unsafe method with Idempotency-Key: safe to retry"
    return False, "unsafe method without a key: retrying may duplicate"


# ============================================================
# 4. Retry-After — backoff the client from the server side
# ============================================================
@app.get("/rate-limit-demo")
def rate_limit_demo(retry_after_seconds: int = 2) -> dict:
    """A 429 with Retry-After tells the client WHEN to retry."""
    raise HTTPException(
        status_code=429,
        detail="Rate limit exceeded",
        headers={"Retry-After": str(retry_after_seconds)},
    )


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- Idempotency-Key: same key + same request = same result, once")
print("- At-least-once delivery is the reality; dedup makes it safe")
print("- Safe methods (GET) retry freely; unsafe need a key")
print("- Retry-After drives client backoff on 429/503")
print("- Exactly-once is a fiction: design for at-least-once + dedup")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # Naive: two retries, two charges (the bug)
        r1 = client.post("/naive/charges", json={"amount_cents": 100})
        r2 = client.post("/naive/charges", json={"amount_cents": 100})
        assert r1.json()["charge_id"] != r2.json()["charge_id"], \
            "naive retry must double-charge (demonstrating the bug)"

        # Idempotent: same key, two requests, ONE charge
        key = "order-123"
        a = client.post("/charges", json={"amount_cents": 500},
                        headers={"Idempotency-Key": key})
        b = client.post("/charges", json={"amount_cents": 500},
                        headers={"Idempotency-Key": key})
        assert a.status_code == 201 and b.status_code == 201
        assert a.json()["charge_id"] == b.json()["charge_id"], "same key -> same id"
        assert a.json()["deduplicated"] is False
        assert b.json()["deduplicated"] is True, "replay must be flagged"
        assert b.json()["attempts"] == 2

        # Missing key rejected
        assert client.post("/charges", json={"amount_cents": 1}).status_code == 400

        # Retry rules
        assert can_retry("GET", False)[0] is True
        assert can_retry("POST", True)[0] is True
        assert can_retry("DELETE", False)[0] is False

        # Retry-After header present on 429
        r = client.get("/rate-limit-demo")
        assert r.status_code == 429
        assert r.headers.get("retry-after") == "2"

    print("[OK] 30-idempotency-and-retries: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("30-idempotency-and-retries:app", host="127.0.0.1", port=8000)
    else:
        _verify()
