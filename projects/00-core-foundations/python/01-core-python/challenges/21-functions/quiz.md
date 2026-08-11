# Challenge 21 — Quiz: Functions

1. `def add(msg, history=[])` — the default list is created:
   - A) on every call  (B) once, when the `def` executes  (C) on first call only  (D) never
2. Calling that buggy `add("a")` then `add("b")` returns lists of length:
   - A) 1 and 2  (B) 1 and 1  (C) 2 and 2  (D) 0 and 1
3. The safe idiom for a mutable default is:
   - A) `history=[]`  (B) `history=tuple()`  (C) `history=None` + build inside  (D) `global history`
4. Inside `def f(**kwargs)`, `kwargs` is:
   - A) a tuple  (B) a dict  (C) a list  (D) a set
5. `{**defaults, **overrides}` on conflicting keys keeps the value from:
   - A) `defaults`  (B) whichever is longer  (C) `overrides`  (D) raises `KeyError`
6. `defaults.update(overrides)` differs from `{**defaults, **overrides}` because it:
   - A) mutates the caller's dict  (B) is slower  (C) deep-copies  (D) drops keys
7. In `def gen(prompt, *, model, max_tokens=256)`, calling `gen("p", "m")` gives:
   - A) `model="m"`  (B) `max_tokens="m"`  (C) a warning  (D) `TypeError`
8. Per-session counters in a closure cell versus a module-level global:
   - A) identical behaviour  (B) the closure is shared across sessions  (C) both are thread-safe  (D) the global is shared across all sessions

**Answers:** 1-B, 2-A, 3-C, 4-B, 5-C, 6-A, 7-D, 8-D
