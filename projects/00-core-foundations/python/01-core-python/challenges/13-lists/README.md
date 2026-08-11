# Challenge 13: Lists

An inference service takes 10,000 prompts per minute and the provider accepts 32
per call. The list you slice them into decides your throughput; the list you
*alias* decides whether user 500's request arrives carrying 499 other people's
prompts. Batching, reordering, and copying are three list decisions with three
different production incidents behind them.

## 🥉 Bronze — Batch Prompts for Inference (~15 min)

**Task:** Implement `batch_prompts(prompts, batch_size)`, returning consecutive
batches of at most `batch_size` prompts, request order preserved. The final
batch may be short — dropping it is the classic off-by-one here, and it silently
loses the tail of every request. Raise `ValueError` if `batch_size < 1`.

**Signature:**
```python
def batch_prompts(prompts: list[str], batch_size: int) -> list[list[str]]:
```

| Input | Expected |
|---|---|
| `["a","b","c","d","e"], 2` | `[["a","b"], ["c","d"], ["e"]]` |
| `["a","b","c","d"], 2` | `[["a","b"], ["c","d"]]` |
| `["a","b"], 32` | `[["a","b"]]` (batch_size > n) |
| `["a","b","c"], 1` | `[["a"], ["b"], ["c"]]` |
| `[], 4` | `[]` |
| `["a","b"], 0` | `ValueError` |

**Constraints:** `n <= 10^5`. Must not mutate `prompts`, and each returned batch
must be an independent list — mutating `batches[0][0]` must not touch the input.
Any correct approach passes; slicing at a stride
(`range(0, len(prompts), batch_size)`) gets it in one line and clamps the last
batch for free.

---

## 🥈 Silver — Realign Out-of-Order Results (~35 min)

**Task:** Implement `align_batch_results(results, count)`. A provider returns
completions as `(position, text)` pairs in *arrival* order, which is not request
order. Return the texts in request order.

Every position in `range(count)` appears exactly once. Enforce that: raise
`ValueError` on a position outside the range, a duplicated position, or a
missing one. A provider that echoes index 3 twice must not be allowed to
silently overwrite one response and leave a hole.

**Signature:**
```python
def align_batch_results(results: list[tuple[int, str]], count: int) -> list[str]:
```

| Input | Expected |
|---|---|
| `[(2,"third"), (0,"first"), (1,"second")], 3` | `["first","second","third"]` |
| `[(3,"d"), (2,"c"), (1,"b"), (0,"a")], 4` | `["a","b","c","d"]` |
| `[(1,"b"), (0,"")], 2` | `["", "b"]` (empty completion is a real answer) |
| `[], 0` | `[]` |
| `[(0,"a"), (2,"c")], 3` | `ValueError` (position 1 missing) |
| `[(0,"a"), (0,"b")], 2` | `ValueError` (duplicate position) |
| `[(0,"a"), (5,"f")], 2` | `ValueError` (out of range) |

**Constraints:** `count <= 10^5`. Must not mutate `results`. The tests wrap
every position in an `int` subclass that counts comparisons and assert the total
stays under `4 * count`. `sorted(results)` on shuffled arrival order — where
timsort's run detection cannot help — costs a genuine `n log2 n`: **~850,000
comparisons against a 200,000 budget** at `count = 50_000`, 4x over. The
position is data you were *handed*; paying `O(n log n)` to rediscover it is the
mistake. Scatter into a pre-allocated buffer instead: `O(n)`, zero comparisons.

Note that an empty completion `""` is falsy, so a `if out[pos]` occupancy test
mistakes it for an unfilled slot. Track occupancy separately.

---

## 🥇 Gold — Shared Prompt Prefix, No Aliasing (~75 min)

**Task:** Implement `build_conversations(shared_prefix, user_prompts)`, returning
one conversation per user prompt: the prefix messages followed by a fresh
`{"role": "user", "content": prompt}` message.

The prefix is a system prompt plus retrieved context — typically 40 messages,
identical for every request in the batch, and **read-only**. There are exactly
two ways to get this wrong and they fail in opposite directions:

- `conv = shared_prefix` then `conv.append(user_msg)` **aliases the caller's
  list**. Every request appends to the one template, so request 500 carries 499
  other users' prompts. That is a cross-tenant prompt leak *and* an unbounded
  token bill.
- `copy.deepcopy(shared_prefix)` per conversation is safe but duplicates every
  message dict `n` times to protect data nobody mutates.

The correct move is the middle one: a **new list, shared message objects**.

**Signature:**
```python
def build_conversations(
    shared_prefix: list[dict[str, str]],
    user_prompts: list[str],
) -> list[list[dict[str, str]]]:
```

| Input | Expected |
|---|---|
| `[{"role":"system","content":"S"}], ["q1","q2"]` | 2 conversations, each `[S_msg, {"role":"user","content":"qN"}]` |
| `[], ["q"]` | `[[{"role":"user","content":"q"}]]` |
| `prefix, []` | `[]` |
| `[], ["q","q"]` | two *equal but distinct* conversations |

**Constraints:** 5,000 conversations over a 40-message prefix, memory < 12 MB.
The tests check four things a shortcut breaks:

- **Identity of prefix messages** — `conv[i] is shared_prefix[i]` must hold. A
  deep copy fails this.
- **Copy-call count** — the prefix messages are a `dict` subclass counting
  `copy()`/`__deepcopy__` calls; the budget is exactly **0**.
- **`tracemalloc` peak** — deep-copying allocates 200,000 dicts, **~35 MB
  against a 12 MB ceiling**. Sharing costs one pointer per slot, ~3 MB.
- **No mutation, no shared backing list** — `shared_prefix` must still have 40
  messages afterwards, and appending an assistant reply to `convs[0]` must not
  change `len(convs[1])`.

**Follow-up:** sharing works because the prefix is read-only. What breaks first
when a per-turn step starts *editing* one of those shared message dicts in
place? (Answer: the sharing itself — an in-place edit to a shared dict is
visible in all 5,000 conversations at once, which is the same cross-tenant leak
one level down. At that point you either make messages immutable — frozen
dataclass or tuple — so the type system forbids the edit, or you copy-on-write
just the message being edited. Note `list(shared_prefix)` is a shallow copy: it
protects the *list* from `append`, never the *dicts* from mutation.)

---

## Running

```bash
# Should FAIL until you implement starter.py
pytest 01-core-python/challenges/13-lists/test_challenge.py -v

# Validate the reference solution
CHALLENGE_USE_SOLUTION=1 pytest 01-core-python/challenges/13-lists/test_challenge.py -q
```

## Test File Structure

```
challenges/13-lists/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
├── test_challenge.py  # Tests (default: run against starter.py)
└── quiz.md            # 8 recall questions
```
