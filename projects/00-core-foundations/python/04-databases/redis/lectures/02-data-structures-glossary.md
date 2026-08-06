# Redis — Glossary 02

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| HGETALL | Hash | read every field of a hash in one call |
| HINCRBY | Hash | atomically increment one hash field |
| Hash | Type | object: one key, many fields, O(1) field ops |
| HSET | Hash | set one or more fields of a hash |
| List | Type | ordered sequence with O(1) push/pop at both ends |
| LPUSH | List | push to the left (head) of a list |
| LRANGE | List | read a slice of a list |
| LTRIM | List | keep only a range, dropping the rest |
| Projection | Design | one entity fanned out into several types per query |
| RPOP | List | pop from the right (tail) of a list |
| SADD | Set | add members to a set (unique) |
| SCARD | Set | size of a set |
| SINTER | Set | intersection of sets |
| SISMEMBER | Set | O(1) membership test |
| Set | Type | unordered collection of unique strings |
| Skip list | Internal | balanced structure backing sorted sets |
| Sorted set | Type | members with scores, kept ordered by score |
| ZADD | Sorted set | insert/update member with a score |
| ZINCRBY | Sorted set | atomically adjust a member's score |
| ZRANK | Sorted set | position of a member by score |
| ZRANGE | Sorted set | slice by score order (ascending) |
| ZREVRANGE | Sorted set | slice descending (top-N) |

## Detailed Definitions

### HGETALL
**Definition**: Command returning every field and value of a hash as a dict.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.hset("user:1", {"name": "sara", "age": "25"})
print(r.hgetall("user:1"))
```
```text
# {'name': 'sara', 'age': '25'} — one round trip for the object
```
**Complexity**: O(fields).
**Related**: Hash, HSET

### HINCRBY
**Definition**: Command atomically incrementing a numeric hash field.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.hset("user:1", "logins", "0")
r.hincrby("user:1", "logins", 1)
print(r.hget("user:1", "logins"))  # -> 1
```
```text
# concurrent increments never lose counts
```
**Complexity**: O(1).
**Related**: Hash, HGETALL

### Hash
**Definition**: A Redis type storing field-value pairs under one key — the
canonical model for an object.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.hset("user:42", {"name": "sara", "email": "sara@x.com"})
print(r.hget("user:42", "name"))  # -> sara
```
```text
# one key per entity, fields as attributes, O(1) per field
```
**Complexity**: O(1) per field operation.
**Related**: HSET, HGETALL, Projection

### HSET
**Definition**: Command setting one or more fields of a hash, creating the
hash if needed.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.hset("product:7", "name", "laptop")
r.hset("product:7", "price", "999")
print(r.hgetall("product:7"))
```
```text
# {'name': 'laptop', 'price': '999'}
```
**Complexity**: O(1) per field.
**Related**: Hash, HGETALL

### List
**Definition**: A Redis type holding an ordered sequence of strings with O(1)
push/pop at both ends — the raw material of queues.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.lpush("q", "a", "b")      # ['b', 'a']
print(r.rpop("q"))          # -> a  (FIFO with LPUSH/RPOP)
```
```text
# same-side push/pop = stack; opposite ends = queue
```
**Complexity**: O(1) at the ends; O(n) at an index.
**Related**: LPUSH, RPOP, LRANGE

### LPUSH
**Definition**: Command pushing one or more values onto the left (head) of a
list.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.lpush("jobs", "j1")
r.lpush("jobs", "j2")       # head is now j2
print(r.lrange("jobs", 0, -1))  # -> ['j2', 'j1']
```
```text
# paired with RPOP it forms a FIFO queue
```
**Complexity**: O(1) per value.
**Related**: List, RPOP

### LRANGE
**Definition**: Command reading a slice of a list by index.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.lpush("jobs", "j1", "j2", "j3")
print(r.lrange("jobs", 0, 1))  # -> ['j3', 'j2']
```
```text
# the standard way to inspect a queue without popping
```
**Complexity**: O(start + count).
**Related**: List, LPUSH

### LTRIM
**Definition**: Command keeping only a range of a list and dropping the rest —
how bounded queues are made.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.lpush("log", "e1", "e2", "e3", "e4")
r.ltrim("log", 0, 1)            # keep newest 2
print(r.lrange("log", 0, -1))   # -> ['e4', 'e3']
```
```text
# prevents unbounded growth of feed/queue keys
```
**Complexity**: O(n) worst case.
**Related**: List, LRANGE

### Projection
**Definition**: The practice of writing one entity into several Redis types,
each tuned to a different query — Redis's answer to denormalization.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.hset("user:42", "name", "sara")      # profile: hash
r.sadd("followers:42", "1", "2")       # membership: set
r.zadd("leaderboard", {"sara": 100})   # ranking: sorted set
```
```text
# writes pay fan-out; reads are single O(1) calls
```
**Complexity**: write cost scales with the number of projections.
**Related**: Hash, Sorted set, Set

### RPOP
**Definition**: Command popping a value from the right (tail) of a list;
returns None when empty.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.lpush("q", "oldest", "newest")
print(r.rpop("q"))  # -> oldest  (FIFO order)
print(r.rpop("q"))  # -> newest
print(r.rpop("q"))  # -> None
```
```text
# LPUSH + RPOP = FIFO; the RQ broker is built on this
```
**Complexity**: O(1).
**Related**: List, LPUSH

### SADD
**Definition**: Command adding members to a set; duplicates are ignored.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.sadd("tags:ml", "vector", "vector", "retrieval")
print(r.smembers("tags:ml"))  # -> {'vector', 'retrieval'}
```
```text
# uniqueness is enforced by the structure, not the caller
```
**Complexity**: O(1) per member.
**Related**: Set, SISMEMBER

### SCARD
**Definition**: Command returning the number of members in a set.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.sadd("followers:42", "1", "2", "3")
print(r.scard("followers:42"))  # -> 3
```
```text
# instant follower counts without loading members
```
**Complexity**: O(1).
**Related**: Set, SADD

### SINTER
**Definition**: Command returning the intersection of two or more sets.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.sadd("liked:ai", "u1", "u2")
r.sadd("liked:db", "u2", "u3")
print(r.sinter("liked:ai", "liked:db"))  # -> {'u2'}
```
```text
# "users who liked X and Y" in one call
```
**Complexity**: O(min set size).
**Related**: Set, SISMEMBER

### SISMEMBER
**Definition**: Command testing whether a member is in a set — O(1)
membership.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.sadd("allowed", "a")
print(r.sismember("allowed", "a"))  # -> True
print(r.sismember("allowed", "z"))  # -> False
```
```text
# the reason sets beat lists for membership questions
```
**Complexity**: O(1).
**Related**: Set, SADD

### Set
**Definition**: A Redis type holding an unordered collection of unique
strings with O(1) membership operations.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.sadd("seen", "doc-1", "doc-1", "doc-2")
print(r.scard("seen"))  # -> 2 (deduplicated)
```
```text
# dedup, allow-lists, and set algebra live here
```
**Complexity**: O(1) per member op.
**Related**: SADD, SISMEMBER, SCARD

### Skip list
**Definition**: The internal balanced structure that keeps sorted-set members
ordered by score with O(log n) operations.
**Example**:
```python
# conceptual: layered linked lists let ZADD/ZRANK skip levels
# -> O(log n) insert, rank, and range queries
```
```text
# you never touch it directly; it explains the cost model
```
**Complexity**: O(log n) per sorted-set op.
**Related**: Sorted set, ZADD

### Sorted set
**Definition**: A Redis type whose members carry a numeric score and are kept
ordered by it — the type for rankings and priority.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.zadd("leaderboard", {"alice": 100, "bob": 250})
print(r.zrevrange("leaderboard", 0, 0, withscores=True))
```
```text
# [('bob', 250.0)] — the top of the board
```
**Complexity**: O(log n) per op.
**Related**: ZADD, ZRANGE, Skip list

### ZADD
**Definition**: Command inserting or updating a member with its score in a
sorted set.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.zadd("scores", {"a": 10, "b": 30})
r.zadd("scores", {"a": 20})      # update a's score
print(r.zscore("scores", "a"))   # -> 20.0
```
```text
# insert and update are the same command
```
**Complexity**: O(log n).
**Related**: Sorted set, ZINCRBY

### ZINCRBY
**Definition**: Command atomically adding a delta to a member's score.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.zadd("lb", {"alice": 100})
r.zincrby("lb", 50, "alice")
print(r.zscore("lb", "alice"))  # -> 150.0
```
```text
# no read-modify-write race: the increment is atomic
```
**Complexity**: O(log n).
**Related**: Sorted set, ZADD

### ZRANK
**Definition**: Command returning a member's position in the score order
(0 = lowest score).
**Example**:
```python
from redis_client import get_client

r = get_client()
r.zadd("lb", {"low": 1, "mid": 2, "high": 3})
print(r.zrank("lb", "mid"))  # -> 1
```
```text
# rank = index in ascending score order
```
**Complexity**: O(log n).
**Related**: Sorted set, ZRANGE

### ZRANGE
**Definition**: Command returning a slice of a sorted set in ascending score
order.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.zadd("lb", {"a": 10, "b": 20, "c": 30})
print(r.zrange("lb", 0, 1, withscores=True))
```
```text
# [('a', 10.0), ('b', 20.0)] — lowest scores first
```
**Complexity**: O(log n + count).
**Related**: Sorted set, ZREVRANGE

### ZREVRANGE
**Definition**: Command returning a slice in descending score order — the
top-N idiom.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.zadd("lb", {"a": 10, "b": 20, "c": 30})
print(r.zrevrange("lb", 0, 1, withscores=True))
```
```text
# [('c', 30.0), ('b', 20.0)] — the leaderboard view
```
**Complexity**: O(log n + count).
**Related**: Sorted set, ZRANGE

## Key Concepts Summary

### The five types
- String: scalar, counter, blob — the atom
- Hash: object with O(1) field access (HSET/HGET/HINCRBY/HGETALL)
- List: FIFO queue / stack via LPUSH/RPOP, O(1) ends
- Set: membership and dedup via SADD/SISMEMBER/SCARD/SINTER
- Sorted set: ranking and top-N via ZADD/ZRANGE/ZREVRANGE, O(log n)

### Choosing by query
- "Is it in there?" -> set
- "Show me the object" -> hash
- "Process in order" -> list
- "Give me the top 10" -> sorted set
- "Count/flag/cache" -> string

### Cost model
- Ends of lists and set ops are O(1); sorted sets pay O(log n) for order
- Every type is a projection of one entity; writes fan out, reads stay single
- Skip lists and ~2x pointer overhead explain zset memory

## Practice Terms

Match each term to its definition (answers at the bottom).

1. HINCRBY — ___
2. LPUSH + RPOP — ___
3. SISMEMBER — ___
4. ZREVRANGE — ___
5. LTRIM — ___
6. SINTER — ___
7. ZINCRBY — ___
8. Skip list — ___

a) FIFO queue pattern
b) O(1) membership test
c) Atomic hash field increment
d) Top-N in descending order
e) Intersection of sets
f) Keep only a range of a list
g) Atomic score adjustment
h) Structure backing sorted sets

**Answers:** 1-c, 2-a, 3-b, 4-d, 5-f, 6-e, 7-g, 8-h
