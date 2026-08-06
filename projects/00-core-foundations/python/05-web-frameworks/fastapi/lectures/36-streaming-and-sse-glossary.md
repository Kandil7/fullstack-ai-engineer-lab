# Streaming and SSE — Glossary 36

Companion lecture: `36-streaming-and-sse-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Backpressure | Mechanism | Pacing a fast producer to a slow consumer |
| Chunked transfer | HTTP | Sending a body in pieces as they are produced |
| Client disconnect | Failure | The client left; generation must stop |
| data: frame | SSE | The `data: <payload>\n\n` event framing |
| Event stream | SSE | A long-lived HTTP connection pushing events |
| First-byte latency | Performance | Time until the first chunk arrives |
| Generator | Mechanism | A function yielding chunks of the response |
| is_disconnected | Mechanism | FastAPI/Starlette check for client departure |
| Keepalive | SSE | Periodic comment frames keeping idle streams alive |
| Long-lived connection | HTTP | A connection held open for the stream's duration |
| Pacing | Mechanism | Await-based slowing of chunk production |
| StreamingResponse | Mechanism | FastAPI response wrapping a generator |
| SSE | Protocol | Server-Sent Events — one-way server-to-client push |
| Token streaming | AI | Yielding LLM tokens as they are generated |
| X-Accel-Buffering | Header | Tells nginx not to buffer the response |
| Anti-buffering headers | Header | no-cache + X-Accel-Buffering for event streams |

## Detailed Definitions

### Backpressure
**Definition**: The mechanism of slowing a fast producer when the consumer is
slow — implemented with awaits or bounded queues to avoid unbounded buffering.
**Related**: Pacing

### Chunked transfer
**Definition**: HTTP transfer where the body is sent in pieces as produced,
via `Transfer-Encoding: chunked` — the transport behind StreamingResponse.
**Related**: StreamingResponse

### Client disconnect
**Definition**: The client terminating the connection mid-stream; the server
should stop generating to avoid wasted compute.
**Related**: is_disconnected

### data: frame
**Definition**: The SSE framing unit — `data: <payload>\n\n` — one event per
blank-line-terminated frame.
**Example**:
```python
yield f"data: {json.dumps(event)}\n\n"
```
**Related**: SSE

### Event stream
**Definition**: A single long-lived HTTP connection over which the server
pushes a sequence of events.
**Related**: SSE

### First-byte latency
**Definition**: The time until the first chunk of a response arrives — the
metric streaming optimizes; the whole point of streaming.
**Related**: Chunked transfer

### Generator
**Definition**: A function using `yield` to produce chunks incrementally —
the body source of a StreamingResponse.
**Related**: StreamingResponse

### is_disconnected
**Definition**: Starlette's `request.is_disconnected()` — an awaitable check
for whether the client is still connected; polled between chunks.
**Related**: Client disconnect

### Keepalive
**Definition**: Periodic comment frames (`: keepalive\n\n`) that keep idle
SSE connections from timing out.
**Related**: SSE

### Long-lived connection
**Definition**: A connection held open for the duration of a stream, unlike a
standard request/response cycle.
**Related**: SSE

### Pacing
**Definition**: Awaiting between chunk productions so the stream rate matches
the consumer — the practical form of backpressure.
**Related**: Backpressure

### StreamingResponse
**Definition**: FastAPI's response class wrapping a generator; each yield is
flushed to the client.
**Example**:
```python
return StreamingResponse(gen(), media_type="text/plain")
```
**Related**: Generator, Chunked transfer

### SSE
**Definition**: Server-Sent Events — a standardized one-way push protocol over
HTTP with `data:` frame framing.
**Related**: data: frame

### Token streaming
**Definition**: Yielding LLM output tokens as they are generated so chat
interfaces render progressively.
**Related**: StreamingResponse

### X-Accel-Buffering
**Definition**: An nginx-specific header (`X-Accel-Buffering: no`) disabling
proxy buffering for streams.
**Related**: Anti-buffering headers

### Anti-buffering headers
**Definition**: Headers (`Cache-Control: no-cache`, `X-Accel-Buffering: no`)
that stop proxies and CDNs from buffering event streams.
**Related**: X-Accel-Buffering

## Key Concepts Summary

### The streaming stack
- Generator -> StreamingResponse -> chunked transfer.
- SSE: `data: <json>\n\n` frames over a long-lived connection.
- Anti-buffering headers keep proxies out of the way.

### The lifecycle discipline
- Check is_disconnected between chunks; stop on departure.
- Pace with awaits; bounded queues for external producers.
- Keep per-chunk work tiny so the loop serves everyone.

### The cost story
- Memory bounded to chunk size, not body size.
- Disconnect handling stops paying for output nobody receives.
- First-byte latency is the metric streaming buys.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. FastAPI response wrapping a generator — ___
2. The `data: <payload>\n\n` framing unit — ___
3. The check for client departure — ___
4. Pacing a fast producer to a slow consumer — ___
5. Time until the first chunk arrives — ___
6. A long-lived one-way push connection — ___
7. Stops generation for a client that left — ___
8. Tells nginx not to buffer the response — ___

**Answers:** 1-StreamingResponse, 2-data: frame, 3-is_disconnected,
4-backpressure, 5-first-byte latency, 6-SSE, 7-client disconnect,
8-X-Accel-Buffering
