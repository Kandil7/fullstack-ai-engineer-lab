# Redis — Glossary 06

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Acquire | Lock | the act of winning the lock (SET NX succeeds) |
| Compare-and-delete | Lock | release only if the stored token matches yours |
| Distributed lock | Pattern | coordination across processes via a shared key |
| Expiry (lock) | Lock | TTL that auto-releases a crashed holder's lock |
| Fencing token | Safety | monotonic id checked by the resource against stale writers |
| Heartbeat | Lock | periodic renewal so long jobs outlive the TTL |
| Leader election | Use case | one worker chosen to run a scheduled job |
| Mutual exclusion | Goal | the property that only one holder is active at a time |
| Paused holder | Failure | a holder resumed by GC/network after its lock expired |
| PX | Lock | expiry in milliseconds, set atomically with NX |
| Redlock | Algorithm | quorum acquisition across independent Redis nodes |
| Release | Lock | handing the lock back (only by its owner) |
| SET NX | Primitive | atomic set-if-absent — the acquire |
| Single-flight | Use case | only one replica recomputes a hot cache entry |
| Stale release | Failure | deleting a lock you no longer own |
| Token | Lock | random value proving lock ownership |

## Detailed Definitions

### Acquire
**Definition**: The act of obtaining the lock — succeeding at `SET key token
NX PX`; exactly one contender can win.
**Example**:
```python
print(acquire("job:embed", "worker-a", 30, lc))  # -> True
print(acquire("job:embed", "worker-b", 30, lc))  # -> False
```
```text
# losing is normal: retry with backoff and jitter
```
**Complexity**: O(1).
**Related**: SET NX, Mutual exclusion

### Compare-and-delete
**Definition**: The safe release: read the stored token, delete only if it
matches yours — never delete blindly.
**Example**:
```python
def release(lock_name, token, client):
    if client.get(f"lock:{lock_name}") == token:
        client.delete(f"lock:{lock_name}")
        return True
    return False  # someone else owns it now — do NOT delete
```
```text
# in real Redis this is a Lua script (read + delete, atomic)
```
**Complexity**: O(1).
**Related**: Release, Token, Stale release

### Distributed lock
**Definition**: A coordination primitive held in shared Redis so processes
that share nothing else cannot run the same critical section twice.
**Example**:
```python
acquire("job:embed", token, 30, lc)   # one replica wins
# ... rebuild the embedding index ...
release("job:embed", token, lc)
```
```text
# needed for multi-process jobs, stampedes, leader election
```
**Complexity**: O(1) per acquire/release.
**Related**: Acquire, Mutual exclusion, Leader election

### Expiry (lock)
**Definition**: The TTL attached to a lock so a crashed holder's lock
disappears automatically — the crash-safety half of SET NX PX.
**Example**:
```python
clock.advance(31)  # TTL 30s elapses
print(lc.exists("lock:job:embed"))  # -> 0 (freed by expiry)
```
```text
# the TTL is also a deadline: no job may run longer without renewing
```
**Complexity**: O(1) background.
**Related**: PX, Paused holder, Heartbeat

### Fencing token
**Definition**: A monotonically increasing number granted with the lock; the
resource rejects any write carrying a token older than the last accepted one.
**Example**:
```python
def fenced_write(data, token, db):
    if token <= db["last_token"]:
        return False  # stale or replayed writer
    db["last_token"] = token
    db["data"] = data
    return True
```
```text
# locks say "may I start?"; fencing says "may I still write?"
```
**Complexity**: O(1) at the resource.
**Related**: Paused holder, Mutual exclusion

### Heartbeat
**Definition**: Periodic renewal of the lock TTL so a legitimately long job
does not lose its lock mid-run.
**Example**:
```python
# every 10s while the job runs: EXPIRE lock:<name> 30
# (with ownership check — renew only if you still hold it)
```
```text
# renewing makes the TTL a liveness signal, not a wall
```
**Complexity**: O(1) per beat.
**Related**: Expiry (lock), Paused holder

### Leader election
**Definition**: Using a lock to pick exactly one worker for a scheduled job
— the same primitive, different name.
**Example**:
```python
# nightly embedding sweep: every replica tries acquire("sweep")
# the winner runs; losers retry next round
```
```text
# one leader per job; the lock TTL bounds leader crashes
```
**Complexity**: O(1) per attempt.
**Related**: Distributed lock, Single-flight

### Mutual exclusion
**Definition**: The guarantee a lock exists to provide: at any moment at most
one holder runs the protected section.
**Example**:
```python
# two workers both write the shared index -> corruption
# with the lock: only worker-a's critical section runs at a time
```
```text
# expiry + paused holders can still break it (see fencing)
```
**Complexity**: n/a — the goal, not an operation.
**Related**: Acquire, Fencing token, Paused holder

### Paused holder
**Definition**: A lock holder whose process pauses (GC, network) past its own
TTL, resumes, and keeps writing while a new holder works — the expiry trap.
**Example**:
```python
# a's lock expires at t=30 (pause); b acquires at t=31;
# a resumes at t=35 and writes — two writers!
# fix: fencing tokens rejected by the resource
```
```text
# locks alone cannot fix paused-process races
```
**Complexity**: n/a — a failure mode.
**Related**: Fencing token, Expiry (lock)

### PX
**Definition**: The flag setting lock expiry in milliseconds within the same
SET that acquires — atomicity of acquire+expiry.
**Example**:
```python
# SET lock:job token NX PX 30000   (30 seconds)
# NOT: SETNX then EXPIRE (a crash between them = permanent lock)
```
```text
# atomic acquire-with-expiry is non-negotiable
```
**Complexity**: O(1).
**Related**: SET NX, Expiry (lock)

### Redlock
**Definition**: The distributed lock algorithm acquiring on a quorum of
independent Redis nodes; tolerates node crashes at high complexity cost.
**Example**:
```python
# acquire on N/2+1 of N independent nodes, release on all
# criticism (Kleppmann): a pause longer than every TTL still breaks it
```
```text
# consensus: single Redis + TTL + fencing suffices for most systems
```
**Complexity**: O(nodes) round trips per acquire.
**Related**: Distributed lock, Mutual exclusion

### Release
**Definition**: Handing the lock back — only by its owner, via
compare-and-delete.
**Example**:
```python
print(release("job:embed", "worker-b", lc))  # -> True (owner)
print(release("job:embed", "worker-a", lc))  # -> False (stale)
```
```text
# release in a finally block so exceptions never leak the lock
```
**Complexity**: O(1).
**Related**: Compare-and-delete, Stale release

### SET NX
**Definition**: The atomic set-if-absent command — the acquire half of the
lock, combined with PX for expiry.
**Example**:
```python
print(lc.set(f"lock:{name}", token, nx=True, ex=30))  # True wins
```
```text
# NX alone leaks locks on crash; NX + PX together are correct
```
**Complexity**: O(1).
**Related**: Acquire, PX

### Single-flight
**Definition**: The use case where one replica wins the lock to recompute a
shared expensive value while others wait — the cache stampede fix.
**Example**:
```python
if r.set("lock:hot", "loading", nx=True, ex=10):
    value = expensive_recompute()
    r.set("hot", value, ex=300)
    r.delete("lock:hot")
# losers spin-read the cache briefly, then fall back
```
```text
# the most common real-world distributed lock in AI systems
```
**Complexity**: O(1) lock + bounded retry.
**Related**: Distributed lock, Leader election

### Stale release
**Definition**: A release attempt by a former holder whose lock already
expired — must be rejected, never delete someone else's lock.
**Example**:
```python
# a's lock expired; b holds it now
print(release("job:embed", "worker-a", lc))  # -> False, b keeps it
```
```text
# blind DEL is the bug; token compare is the fix
```
**Complexity**: O(1).
**Related**: Compare-and-delete, Token

### Token
**Definition**: A random value stored in the lock key at acquire time,
proving ownership at release time.
**Example**:
```python
token = uuid4().hex            # unique per acquire
acquire("job:embed", token, 30, lc)
release("job:embed", token, lc)  # only this token releases
```
```text
# without a token, any caller could delete the lock
```
**Complexity**: O(1).
**Related**: Compare-and-delete, Stale release

## Key Concepts Summary

### The primitive
- SET NX PX = atomic acquire with crash-safe expiry; never SETNX then EXPIRE
- Release = compare-and-delete with your token; never blind DEL
- TTL is both crash safety and a deadline — renew with heartbeats

### The trap
- Expiry handles dead holders; paused holders need fencing tokens at the
  resource, because locks alone cannot stop a resumed writer
- Redlock's quorum does not fix pauses either — usually overkill

### When to use
- Multi-process single-run jobs, stampede single-flight, leader election
- Not needed: single-process concurrency (threading.Lock), single DB writes
  (transactions)

## Practice Terms

Match each term to its definition (answers at the bottom).

1. SET NX PX — ___
2. Compare-and-delete — ___
3. Paused holder — ___
4. Fencing token — ___
5. Stale release — ___
6. Heartbeat — ___
7. Redlock — ___
8. Leader election — ___

a) Release only if the token matches
b) Atomic acquire with expiry
c) A resumed writer whose lock expired
d) Rejected by the resource via monotonic tokens
e) Renewal so long jobs keep the lock
f) Quorum acquisition across nodes
g) One worker chosen for a scheduled job
h) Deleting a lock you no longer own

**Answers:** 1-b, 2-a, 3-c, 4-d, 5-h, 6-e, 7-f, 8-g
