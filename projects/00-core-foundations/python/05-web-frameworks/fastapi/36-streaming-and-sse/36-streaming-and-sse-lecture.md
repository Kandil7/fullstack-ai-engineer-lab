# FastAPI — 36: Streaming and SSE

Companion exercise: `36-streaming-and-sse.py`

---

## Topic Overview

Some responses should not wait to be complete: LLM tokens, progress updates,
live metrics, file downloads. Streaming delivers the first bytes in
milliseconds instead of seconds, and for LLM APIs it is the difference between
a chat that feels instant and one that feels broken. This topic covers
`StreamingResponse` (chunked bodies), Server-Sent Events (SSE) for
one-way push over a long-lived connection, the client-disconnect problem
(keep generating for a client that left = wasted tokens), and backpressure
(pacing a fast producer to a slow consumer).

The core discipline: streaming is not "return a generator" — it is managing
a connection that must be opened fast, paced correctly, and closed honestly.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Return a `StreamingResponse` from a generator.
2. Frame SSE events correctly (`data: <json>\n\n`).
3. Stream LLM tokens with early stop on disconnect.
4. Explain why disconnect handling saves money and compute.
5. Pace a stream to a slow client (backpressure).
6. Choose streaming vs buffered responses.
7. Set the right headers for SSE and chunked transfer.
8. Test streaming endpoints without a real client.

## Prerequisites

| Need | Where |
|---|---|
| Async generators | `02-advanced-python/02-generators.py` |
| Async endpoints | `32-async-endpoints-deep.py` |
| Requests/headers | `04-query-parameters.py` |

## 1. StreamingResponse — Chunked Bodies

```python
async def token_stream(text, chunk=2):
    for i in range(0, len(text), chunk):
        yield text[i:i + chunk]
        await asyncio.sleep(0.01)

@app.get("/stream/text")
async def stream_text():
    return StreamingResponse(token_stream("Hello!"), media_type="text/plain")
```

Output:
```
# the client receives "He" then "ll" then "o!" as they are produced
```

`StreamingResponse` wraps a generator; each `yield` is flushed to the client.
First-byte latency collapses from "whole response time" to "first chunk time".

## 2. Server-Sent Events — One-Way Push

```python
async def sse_generator(n=5):
    for i in range(n):
        event = {"step": i, "message": f"event {i}"}
        yield f"data: {json.dumps(event)}\n\n"
        await asyncio.sleep(0.01)

@app.get("/stream/events")
async def stream_events():
    return StreamingResponse(sse_generator(),
                             media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache",
                                      "X-Accel-Buffering": "no"})
```

Output:
```
# data: {"step": 0, "message": "event 0"}
# data: {"step": 1, "message": "event 1"}
# ... one event per blank-line-terminated frame
```

SSE is a one-way push over a single long-lived HTTP connection — ideal for
progress bars, job status, and live metrics. Framing: `data: <payload>\n\n`
per event. The headers prevent proxies from buffering the stream.

## 3. Streaming LLM Tokens

```python
async def llm_stream(request: Request):
    for tok in tokens:
        if await request.is_disconnected():
            print("[client disconnected — stopping generation]")
            return
        yield tok + " "
        await asyncio.sleep(0.01)
```

Output:
```
# "The" " quick" " brown" ... token by token
# client leaves -> generation stops on the next token
```

Two rules make token streaming production-safe: yield tokens as they arrive,
and **check `request.is_disconnected()`** between tokens so you stop spending
compute (and money) on a client that left.

## 4. Backpressure — Pacing Producer to Consumer

A fast producer and a slow consumer is a buffering problem: the server either
fills memory or the client times out. Natural pacing — awaiting between
chunks — gives the loop room to slow the producer to the consumer's rate.

```python
async def backpressured_stream():
    for i in range(10):
        yield f"chunk {i}\n"
        await asyncio.sleep(0.005)     # pace = backpressure
```

Output:
```
# chunks arrive at a bounded rate; no unbounded buffering
```

When the producer is external (a fast provider API), use bounded queues or
await-based pacing rather than letting memory grow unbounded.

## 5. Streaming vs Buffered — The Choice

| Use streaming when | Use buffered when |
|---|---|
| Tokens/events arrive over time | The whole body is ready instantly |
| First-byte latency matters | Payload is small |
| Long jobs need progress | You need Content-Length |
| Large file downloads | Simple, cacheable responses |

Streaming trades a known Content-Length and simple semantics for latency and
liveness. Most list endpoints should stay buffered.

## 6. Common Mistakes to Avoid

### Mistake 1: Not handling client disconnect
```python
# WRONG — generator keeps yielding to a dead connection
# CORRECT — check request.is_disconnected() between chunks
```

### Mistake 2: Forgetting SSE framing
```python
# WRONG — yield raw JSON with no "data: " prefix; clients can't parse
# CORRECT — f"data: {json.dumps(event)}\n\n"
```

### Mistake 3: Buffering proxies eating the stream
```python
# WRONG — reverse proxy buffers the whole response
# CORRECT — Cache-Control: no-cache, X-Accel-Buffering: no
```

### Mistake 4: Unbounded producer buffering
```python
# WRONG — collect everything, then stream it (no latency win)
# CORRECT — stream chunks as they arrive
```

### Mistake 5: Blocking calls inside the stream generator
```python
# WRONG — time.sleep / sync calls stall the whole loop between chunks
# CORRECT — await genuine async I/O between yields
```

## 7. Best Practices

1. Stream only what benefits from streaming.
2. Frame SSE precisely; test with a real parser.
3. Check `is_disconnected()` in any long generator.
4. Set anti-buffering headers for event streams.
5. Pace with awaits; use bounded queues for external producers.
6. Keep per-chunk work tiny — the loop serves everyone.
7. Add keepalive comments for idle SSE connections.
8. Set timeouts on both sides of the stream.
9. Log stream duration and bytes for cost tracking.
10. Test disconnects explicitly (abort mid-stream).

## 8. Complexity and Cost

| Aspect | Cost | Notes |
|---|---|---|
| First byte | O(chunk) | The latency win |
| Per chunk | O(1) | Loop must stay free |
| Memory | O(chunk) not O(body) | Bounded by pacing |
| Wasted generation | disconnected clients | Stopped via is_disconnected() |

The cost story: streaming bounds memory to chunk size and — with disconnect
handling — stops paying for output nobody receives.

## 9. AI Engineering Relevance

**Where this shows up:** token streaming is the defining UX of chat and agent
interfaces, and progress streaming is the defining UX of ingestion and
fine-tuning UIs.

| Concept here | Used for |
|---|---|
| Token streaming | Chat completions and agent reasoning visible as they happen |
| is_disconnected | Not billing for abandoned generations |
| SSE | Job progress for ingestion/fine-tuning dashboards |
| Backpressure | Pacing provider streams to slow user connections |
| Anti-buffering headers | Getting streams through nginx/CDN |

**Scale note:** at high concurrency, streaming multiplies per-connection
state. Disconnect handling is not a nicety — it is the difference between
charging customers for output they never saw and not.

## 10. Summary

| Concept | Description |
|---|---|
| StreamingResponse | Chunked body from a generator |
| SSE | One-way push, `data: <json>\n\n` frames |
| Disconnect | Stop generating when the client leaves |
| Backpressure | Pace producer to consumer |
| Headers | no-cache + X-Accel-Buffering: no |

## 11. Quick Reference

| Task | Idiom |
|---|---|
| Stream a generator | `StreamingResponse(gen(), media_type="text/plain")` |
| SSE frame | `yield f"data: {json.dumps(event)}\n\n"` |
| Detect disconnect | `if await request.is_disconnected(): return` |
| Prevent buffering | `Cache-Control: no-cache` + `X-Accel-Buffering: no` |
| Pace | `await asyncio.sleep(...)` between chunks |

## 12. Next Steps

Next: **[37 — Load Testing](37-load-testing-lecture.md)** — measuring what you built.

Continues in: **[09-genai — 02 API Clients](../../09-genai/lectures/02-api-clients-lecture.md)** — streaming from the provider side.

Official docs: <https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events> · <https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse>
