# Challenge 21: Functions

`def add(msg, history=[])` is not a style nit — it is the bug that makes turn 1
of session B contain session A's messages, because the default list is created
**once, when the `def` executes**, and shared by every defaulted call for the
life of the process. Below: that bug, then a `**kwargs` passthrough that must
not mutate or deep-copy a shared provider config, then a keyword-only
`generate()` with a hard token budget.

## 🥉 Bronze — Conversation History Accumulator (~15 min)

**Task:** Implement `append_message(role, content, history=None)`. It appends
`{"role": role, "content": content}` and returns the history. With no
`history`, a **brand new list** is created for that call only. With a list
passed in, it is appended **in place** and the *same object* is returned, so
multi-turn accumulation works. `role` must be `"system"`, `"user"`, or
`"assistant"` — anything else raises `ValueError`.

**Signature:**
```python
def append_message(
    role: str,
    content: str,
    history: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
```

| Input | Expected |
|---|---|
| `("user", "hi")` | `[{"role": "user", "content": "hi"}]` |
| two separate defaulted calls | each returns a **length-1** list, and `first is not second` |
| `("user", "hello", [sys_msg])` | `[sys_msg, user_msg]`, and the return **is** the passed list |
| `("assistant", "")` | `[{"role": "assistant", "content": ""}]` (empty content is legal) |
| `("tool", "x")` | `ValueError` |

**Constraints:** the default must be `None` with the list built inside the
body. The tests make 50 defaulted calls and assert every result has length 1 —
`history=[]` returns lengths 1, 2, 3, … 50 and fails on the second call.

---

## 🥈 Silver — Provider Option Passthrough (~35 min)

**Task:** Implement `call_provider(client, prompt, defaults, **overrides)`,
which calls `client(prompt, **merged)` where `merged` is `defaults` updated by
`overrides`. `defaults` is a long-lived shared config object — it holds the
model, temperature, and the full tool schema — so it must come back unchanged,
and its nested values must be forwarded **by reference**.

**Signature:**
```python
def call_provider(
    client: Callable[..., str],
    prompt: str,
    defaults: dict[str, Any],
    **overrides: Any,
) -> str:
```

| Input | Expected `client` kwargs |
|---|---|
| `defaults={"model": "m1", "temperature": 0.0}` | `{"model": "m1", "temperature": 0.0}` |
| same + `temperature=0.7` | `{"model": "m1", "temperature": 0.7}` (override wins) |
| `defaults={"model": "m1"}` + `top_p=0.9, seed=42` | all three keys |
| `defaults={}`, no overrides | `{}` |
| `defaults={"tools": tools}` | `kwargs["tools"] is tools` (same object) |

**Constraints:** two naive-but-correct versions must fail. `defaults.update(overrides)`
returns the right text but mutates the shared config, so a later request that
passes no `temperature` still gets `0.9` — the tests snapshot `defaults` and
compare. `copy.deepcopy(defaults)` is correct *and* safe, but a `tracemalloc`
guard puts a 20,000-entry tool schema in `defaults` and caps the peak at
**1 MB**: a shallow `{**defaults, **overrides}` allocates one small dict, while
the deepcopy reallocates the whole nested payload at **~10 MB per call**.

---

## 🥇 Gold — Keyword-Only `generate()` With a Token Budget (~75 min)

**Task:** Implement `make_generate(client, *, token_budget, defaults=None)`,
returning a per-session closure:

```python
generate(prompt, *, model, max_tokens=256, **provider_options) -> str
```

- **Every** parameter after `prompt` is keyword-only. `generate(prompt, 256, "gpt-4o")`
  must raise `TypeError`, not quietly send `256` as the model.
- No parameter has a mutable default.
- Raises `BudgetExhausted` **without calling the client** once accumulated usage
  has reached `token_budget`.
- `generate.usage()` returns a **copy** of `{"total_tokens": int, "calls": int}`.
- Counters live in the closure, so two sessions never share state.

The fake client is `client(prompt, *, model, max_tokens, **options) -> {"text": ..., "usage": {"total_tokens": ...}}`.

**Signature:**
```python
def make_generate(
    client: Callable[..., dict[str, Any]],
    *,
    token_budget: int,
    defaults: dict[str, Any] | None = None,
) -> Callable[..., str]:
```

| Scenario | Expected |
|---|---|
| budget 1000, two calls at 30 tokens | `usage() == {"total_tokens": 60, "calls": 2}` |
| budget 100, calls at 60 tokens | 3rd call raises `BudgetExhausted`, spy saw **2** calls |
| budget 0 | first call raises, spy saw **0** calls |
| session A over budget | session B's `usage()` is still `{"total_tokens": 0, "calls": 0}` |
| `gen("p", "gpt-4o")` | `TypeError`, spy saw 0 calls |
| mutating the dict from `usage()` | internal counters unchanged |

**Constraints:** the guards are structural and count calls, not seconds.
`inspect.signature` walks the returned callable and asserts every parameter
after the first is `KEYWORD_ONLY` or `VAR_KEYWORD` and that no default is a
`list`/`dict`/`set`. A spy counts provider calls: five refused attempts must
add **zero** calls — checking the budget *after* the request is the expensive
bug, since a runaway retry loop on an exhausted session bills every attempt
(at $3 / 1M input tokens, 1,000 retries of an 8k-token prompt is $24 of pure
waste). A module-level counter passes every correctness test and fails
`test_sessions_do_not_share_counters`.

**Follow-up:** two sessions are cheap — what breaks first at 10^6 concurrent
sessions, each holding its own closure? (Answer: the closure cells themselves.
~10^6 live closures plus their state dicts is hundreds of MB of process memory
that no eviction ever touches, and the counters are lost on restart. At that
scale session state moves out of the process into Redis with a TTL, and the
closure keeps only the session *key*. The second thing to break is atomicity:
`state["total_tokens"] += n` is not a single operation under threads, so the
budget over-spends — the remote counter needs `INCRBY`.)

---

## Running

```bash
# Should FAIL until you implement starter.py
pytest 01-core-python/challenges/21-functions/test_challenge.py -v

# Validate the reference solution
CHALLENGE_USE_SOLUTION=1 pytest 01-core-python/challenges/21-functions/test_challenge.py -q
```

## Test File Structure

```
challenges/21-functions/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
├── test_challenge.py  # Tests (default: run against starter.py)
└── quiz.md            # 8 recall questions
```
