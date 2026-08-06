"""
36 - Streaming and SSE
========================
StreamingResponse, Server-Sent Events, chunked transfer, streaming LLM
tokens, client disconnect handling, backpressure.

Run:      python 36-streaming-and-sse.py
Verify:   python 36-streaming-and-sse.py --verify
Reference: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
"""

from __future__ import annotations

import asyncio
import json
import sys

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Streaming Demo")


# ============================================================
# 1. StreamingResponse — chunked body, first-byte latency
# ============================================================
async def token_stream(text: str, chunk: int = 2):
    """Yield chunks as they become available — the shape of LLM token
    streaming. The client renders the first chunk in ms, not seconds."""
    for i in range(0, len(text), chunk):
        yield text[i:i + chunk]
        await asyncio.sleep(0.01)     # simulate generation latency


@app.get("/stream/text")
async def stream_text() -> StreamingResponse:
    return StreamingResponse(
        token_stream("Hello from a streaming endpoint!", chunk=2),
        media_type="text/plain",
    )


# ============================================================
# 2. Server-Sent Events — one-way push over a long-lived connection
# ============================================================
async def sse_generator(n: int = 5):
    """SSE framing: 'data: <json>\\n\\n' per event."""
    for i in range(n):
        event = {"step": i, "message": f"event {i}"}
        yield f"data: {json.dumps(event)}\n\n"
        await asyncio.sleep(0.01)


@app.get("/stream/events")
async def stream_events() -> StreamingResponse:
    """SSE for progress updates: ingestion status, job progress, ticks."""
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ============================================================
# 3. LLM-style streaming with client disconnect handling
# ============================================================
async def llm_stream(request: Request):
    """A streamed completion. On disconnect, generation must stop —
    otherwise you burn tokens/money serving a client that left."""
    tokens = ["The", " quick", " brown", " fox", " jumps", " over", " the",
              " lazy", " dog."]
    for tok in tokens:
        if await request.is_disconnected():
            print("  [client disconnected — stopping generation]")
            return
        yield tok + " "
        await asyncio.sleep(0.01)


@app.get("/stream/llm")
async def stream_llm(request: Request) -> StreamingResponse:
    return StreamingResponse(llm_stream(request), media_type="text/plain")


# ============================================================
# 4. Backpressure — don't let a slow client buffer the world
# ============================================================
async def backpressured_stream():
    """Awaited yields give the server a chance to pause when the client
    is slow; unbounded buffering of a fast producer is the failure mode."""
    for i in range(10):
        yield f"chunk {i}\n"
        await asyncio.sleep(0.005)   # natural pacing = backpressure


@app.get("/stream/backpressure")
async def stream_backpressure() -> StreamingResponse:
    return StreamingResponse(backpressured_stream(), media_type="text/plain")


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- StreamingResponse: chunked body, first-byte latency matters")
print("- SSE: data: <json> frames over a long-lived HTTP connection")
print("- LLM streaming: yield tokens; STOP on client disconnect")
print("- Backpressure: pace a fast producer to a slow consumer")
print("- Headers: Cache-Control: no-cache, X-Accel-Buffering: no")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # Plain text stream: chunks reassemble the message
        r = client.get("/stream/text")
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/plain")
        body = "".join(r.iter_text())  # TestClient buffers, but framing is checked
        assert body == "Hello from a streaming endpoint!"

        # SSE framing: each event is data: <json> + blank line
        r = client.get("/stream/events")
        assert "text/event-stream" in r.headers["content-type"]
        events = [line for line in r.text.split("\n") if line.startswith("data: ")]
        assert len(events) == 5, "five SSE events expected"
        first = json.loads(events[0][6:])
        assert first["step"] == 0

        # LLM stream returns the tokens
        r = client.get("/stream/llm")
        text = "".join(r.iter_text())
        assert text.startswith("The") and "dog." in text

        # Backpressure stream
        r = client.get("/stream/backpressure")
        assert "chunk 9" in r.text

    print("[OK] 36-streaming-and-sse: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("36-streaming-and-sse:app", host="127.0.0.1", port=8000)
    else:
        _verify()
