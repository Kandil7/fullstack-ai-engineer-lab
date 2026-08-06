# 33 — Security Essentials Lecture

## 1. Topic Overview

Security is not a feature you bolt on; it is the default state of code
that does not take shortcuts. This topic covers the essential hygiene for
AI/backend engineering:

- **Tokens and secrets**: `secrets` vs `random`, never logging credentials
- **Password hashing**: PBKDF2/bcrypt/argon2, never MD5/SHA1/plaintext
- **Timing-safe comparison**: `hmac.compare_digest`
- **Injection classes**: SQL, command, path traversal — and the new one,
  **prompt injection**
- **Deserialization**: `pickle` and `yaml.load` as RCE
- **ReDoS**: catastrophic regex backtracking
- **Process hygiene**: `subprocess` without `shell=True`, least privilege
- **Supply chain**: dependency CVEs, `.pkl` model files as attack vectors

The AI-specific framing is not an afterthought: **model output is
untrusted input**. A RAG system that pipes retrieved text into an
`eval`, an agent that resolves tool names via `exec`, a pipeline that
`pickle.loads` a downloaded model — these are the same vulnerabilities as
SQL injection, wearing an LLM costume. The lecture ends with prompt
injection as the canonical new injection class.

## 2. Learning Objectives

By the end of this lecture you will be able to:

1. Choose `secrets` over `random` for anything security-relevant.
2. Hash passwords with PBKDF2 (or bcrypt/argon2) with a random salt.
3. Use `hmac.compare_digest` and explain why `==` leaks timing.
4. Write parameterized SQL that resists injection.
5. Run subprocesses without `shell=True`.
6. Block path traversal with `Path.resolve()` + `is_relative_to()`.
7. Explain why `pickle.loads` and `yaml.load` on untrusted input are RCE.
8. Recognize ReDoS patterns and avoid catastrophic backtracking.
9. Apply redaction so credentials never reach logs.
10. Frame prompt injection as the injection class for AI systems.

## 3. Prerequisites

- Basic Python: strings, bytes, exceptions, files.
- **`01-decorators.py`** — no, not really; this topic stands alone.
  But being comfortable with `bytes` vs `str` matters for hashing.
- Basic awareness of what an API key is and why it must stay secret.

## 4. Key Concepts

### 4.1 `secrets` vs `random`

`random` is a pseudorandom number generator: deterministic given a seed.
That is fine for simulations and shuffles — and **fatal for tokens**:

```python
import random, string

def insecure_token(length=16):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))

random.seed(42)
print(insecure_token(8))
random.seed(42)
print(insecure_token(8))     # same seed -> same token
```

```text
# Output:
# Dg9G1Z8y
# Dg9G1Z8y
```

`secrets` draws from the operating system's CSPRNG — unpredictable even
if the attacker knows the seed and past outputs:

```python
import secrets

def secure_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

print(secure_token(8))
```

```text
# Output:
# c2Zh9KbX  (different on every run)
```

**Rule:** anything used as a credential — API keys, session tokens,
password-reset links, OTPs — comes from `secrets`, never `random`.

### 4.2 Password hashing — PBKDF2, never MD5/SHA1

Never store plaintext passwords; never store a fast hash (MD5, SHA1,
even plain SHA256) — they can be brute-forced at billions of guesses per
second. Correct hashes are **slow, salted, keyed**: PBKDF2, bcrypt,
argon2, scrypt. The stdlib pattern:

```python
import hashlib, hmac, secrets

def hash_password(password, salt=None, iterations=100_000):
    salt = salt or secrets.token_bytes(16)          # unique per password
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations)
    return digest, salt

def verify_password(password, digest, salt, iterations=100_000):
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate, digest)

digest, salt = hash_password("correct horse battery staple")
print(len(digest), len(salt))
print(verify_password("correct horse battery staple", digest, salt))
print(verify_password("wrong", digest, salt))
```

```text
# Output:
# 32 16
# True
# False
```

**Why a random salt?** Two users with the same password get different
hashes, so a rainbow table or a leaked hash cannot reveal that "alice"
and "bob" share a password. `iterations` makes each guess expensive —
that is the whole defense.

### 4.3 `hmac.compare_digest` — timing-safe comparison

`a == b` on strings returns at the **first mismatching byte**. An
attacker probing a token can measure how many prefix bytes match and
recover it byte-by-byte. `hmac.compare_digest` runs in constant time
relative to the input length:

```python
import hmac

def safe_equals(a, b):
    return hmac.compare_digest(a.encode(), b.encode())

print(safe_equals("abc", "abc"))
print(safe_equals("abc", "abd"))
```

```text
# Output:
# True
# False
```

**Rule:** compare secrets (hashes, tokens, signatures) with
`compare_digest`, never with `==`.

### 4.4 SQL injection — parameterized queries

Interpolating input into SQL turns the input into *structure*:

```python
def unsafe_query(conn, user_id):
    return conn.execute(
        f"SELECT name FROM users WHERE id = '{user_id}'").fetchall()

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id TEXT, name TEXT)")
conn.execute("INSERT INTO users VALUES ('1','alice'), ('2','bob')")

print(unsafe_query(conn, "1' OR '1'='1"))   # every row!
```

```text
# Output:
# [('alice',), ('bob',)]
```

The payload `1' OR '1'='1` closes the string and adds `OR TRUE` — the
query now returns the whole table. The fix is **parameter binding**:
the input stays data, never structure:

```python
def safe_query(conn, user_id):
    return conn.execute(
        "SELECT name FROM users WHERE id = ?", (user_id,)).fetchall()

print(safe_query(conn, "1"))
print(safe_query(conn, "1' OR '1'='1"))    # literal value, no match
```

```text
# Output:
# [('alice',)]
# []
```

**Rule:** placeholders (`?` in sqlite3, `%s` in psycopg) always. Never
build SQL with `f"..."`. This holds for ORMs too: their query *builders*
parameterize; `.raw()`/`.execute()` strings do not.

### 4.5 Command injection — no `shell=True`

`subprocess.run(cmd, shell=True)` hands your input to the shell — `;`,
`&&`, backticks become *commands*:

```python
import subprocess

def safe_run(user_input):
    # argument list: the shell never sees the input
    return subprocess.run(
        [sys.executable, "-c", "import sys; print(sys.argv[1])",
         user_input],
        capture_output=True, text=True, check=True).stdout

print(safe_run("hello; whoami").strip())
```

```text
# Output:
# hello; whoami
```

The metacharacters are printed as *data*, not executed. **Rule:** always
pass an argument list; `shell=True` is the command-injection switch.

### 4.6 Path traversal — resolve and verify containment

User-supplied filenames can contain `../..` and escape your data
directory. Fix: resolve the candidate to an absolute path, then verify it
stays inside the root:

```python
from pathlib import Path

def safe_read(root, filename):
    candidate = (root / filename).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError("path escapes the root")
    return candidate.read_text()

root = Path("data")
root.mkdir(exist_ok=True)
(root / "secret.txt").write_text("TOP SECRET")

try:
    safe_read(root, "../../etc/passwd")
except ValueError as exc:
    print(exc)
print(safe_read(root, "secret.txt"))
```

```text
# Output:
# path escapes the root
# TOP SECRET
```

**Rule:** `resolve()` first (it collapses `..` and symlinks), then
`is_relative_to(root)`.

### 4.7 `pickle` — deserialization is code execution

`pickle.loads` will happily execute code: a crafted payload's
`__reduce__` names a callable and arguments, and unpickling *calls it*.

```python
import os, pickle

class Evil:
    def __reduce__(self):
        return (os.system, ("echo PWNED from pickle",))

payload = pickle.dumps(Evil())
pickle.loads(payload)          # runs os.system!
```

```text
# Output:
# PWNED from pickle
```

**Rule:** never `pickle.loads` anything you did not produce yourself.
For untrusted data use safe formats: JSON, or structured formats with
explicit parsing. **AI hook:** `.pkl` model files are the classic
supply-chain vector — only load models from a trusted artifact store,
and verify their hash before loading.

### 4.8 YAML — `safe_load`, always

`yaml.load` accepts `!!python/object/apply:...` tags that construct
arbitrary Python objects — the same RCE as pickle:

```python
import yaml

malicious = "!!python/object/apply:os.system ['echo yaml-pwned']"
yaml.unsafe_load(malicious)    # executes!
```

```text
# Output:
# yaml-pwned
```

`safe_load` refuses the Python-object tag and raises `yaml.YAMLError`:

```python
try:
    yaml.safe_load(malicious)
except yaml.YAMLError as exc:
    print(type(exc).__name__)
print(yaml.safe_load("a: 1"))
```

```text
# Output:
# ConstructorError
# {'a': 1}
```

**Rule:** `yaml.safe_load`, always. A config file is untrusted input.

### 4.9 ReDoS — catastrophic backtracking

Nested quantifiers like `(a+)+$` backtrack **exponentially** on
near-miss inputs. A 30-character string of `a`s followed by `b` can take
minutes:

```python
evil = r"^(a+)+$"      # DON'T use this on attacker input
safe = r"^a+$"         # linear

import re
print(re.search(safe, "a" * 30 + "b") is not None)   # quick, False
```

```text
# Output:
# False
```

**Rules:** avoid nested quantifiers on untrusted input; anchor
patterns; pre-check input length; prefer linear patterns; if a regex
must be complex, add a timeout (e.g. `regex` module) or a length cap.

### 4.10 Secret management — never log credentials

API keys end up in logs via debug prints, exception messages, and
request dumps. Redact or never include:

```python
def redact(value):
    return f"***{value[-4:]}" if len(value) > 4 else "***"

api_key = "sk-1234567890abcdef"
print(f"log line: calling provider with key {redact(api_key)}")
```

```text
# Output:
# log line: calling provider with key ***cdef
```

**Rules:** keys live in environment variables or a secrets manager
(never in code, never in config files in the repo); rotate on any
suspicion; `git-secrets`-style pre-commit hooks catch accidental
commits.

### 4.11 Subprocess hygiene, TLS, least privilege, dependencies

- **TLS**: `requests`/`httpx` verify certificates by default — never
  disable `verify=False` in production; pin the trust store.
- **Least privilege**: run the worker as a user that can only read its
  input dir and write its output dir. A compromised embedding worker
  with root access is a root compromise.
- **Dependencies**: `pip-audit` / `osv-scanner` in CI; a pinned
  vulnerable dependency is a scheduled incident.
- **`.pkl` models**: hash-verified downloads from a trusted store only.

### 4.12 Prompt injection — the new injection class

Prompt injection is the LLM-era version of SQL injection: untrusted text
(relevant documents, web content, user profiles) is concatenated into a
prompt, and its *instructions* hijack the model's behavior. The
mitigations mirror classic injection defense:

1. **Treat model output as untrusted data**, never as code or authority
   (no `eval` on tool choices — dispatch tables, from topic 32).
2. **Validate before acting**: tool arguments from the model are input;
   parameterize, whitelist, and check ranges like any user input.
3. **Never log credentials** — and remember model *input* is often
   logged too; a prompt containing a user's API key leaks it.
4. **Least privilege for tools**: a search tool that can read the whole
   filesystem is a prompt-injection amplifier.
5. **Sandbox and contain**: retrieval is an input channel like a form
   field; the model is the parser, not the trust boundary.

## 5. Common Mistakes

1. **`random` for tokens** — predictable; always `secrets`.
2. **MD5/SHA1 for passwords** — instant brute force; PBKDF2/bcrypt.
3. **`==` on secrets** — timing leak; `hmac.compare_digest`.
4. **f-string SQL** — injection; parameter binding.
5. **`shell=True`** — command injection; argument lists.
6. **Joining paths without `resolve()`** — traversal; verify
   `is_relative_to`.
7. **`pickle.loads` on untrusted data** — RCE; safe formats.
8. **`yaml.load` instead of `safe_load`** — RCE via Python tags.
9. **Logging API keys** — redact or never include.
10. **`verify=False`** — disables TLS protection in production.
11. **Unbounded regex on input** — ReDoS; linear patterns + length caps.

## 6. Best Practices

- **Default to safe**: `secrets`, parameterized SQL, `safe_load`,
  argument lists, `compare_digest` — the safe variant is the *only*
  variant in new code.
- **Credentials are environment, never code** — and never logs.
- **Hash passwords with a KDF and a fresh salt per user**; verify with
  `compare_digest`.
- **Model output is untrusted input** — validate tool arguments, never
  execute model-chosen code, whitelist names via dispatch tables.
- **Sandbox file/model access**: resolve+verify paths; hash-verify
  artifacts before loading; run workers with least privilege.
- **Automate hygiene**: `pip-audit` in CI, secret scanning pre-commit,
  dependency pinning with review.

## 7. Complexity and Cost

| Pattern | Time | Space | Failure cost |
|---|---|---|---|
| `secrets.token_*` | O(n) | O(n) | Predictable tokens |
| PBKDF2 (100k iters) | ~50 ms/hash | O(1) | Brute-forced passwords |
| `compare_digest` | O(n) | O(1) | Timing attack on secrets |
| Parameterized SQL | O(1) | O(1) | Full DB dump |
| Argument-list subprocess | O(1) | O(1) | Arbitrary command execution |
| `resolve`+`is_relative_to` | O(path) | O(1) | File read/write anywhere |
| `pickle`/`yaml.load` | O(data) | O(data) | **RCE** |
| ReDoS-safe regex | O(n) | O(1) | Minutes-long CPU burn |
| Redaction | O(n) | O(1) | Credential leak |

**Scale notes:** hashing cost is the *feature* (slowing attackers), but
it also slows you: 100k iterations ≈ 50ms per login — fine at 100 RPS,
painful at 10k RPS; that is why session tokens (fast, `secrets`) and
password hashes (slow, KDF) are different mechanisms. ReDoS is a
distributed denial-of-service with one request; length caps are the
cheapest mitigation.

## 8. AI Engineering Relevance

- **Prompt injection** is the SQL injection of AI apps: untrusted
  retrieved text steering a model. Same defense shape: input
  validation, whitelists, least privilege, treat model output as data.
- **Tool-call validation**: an agent resolving `TOOLS[name]` is safe;
  `eval(model_choice)` is RCE. Topic 32's dispatch table is the
  security boundary.
- **`.pkl` model files** are supply-chain vectors; a hijacked model
  card = code execution on your inference server.
- **Configs in YAML** (model configs, eval configs) must use
  `safe_load`; a poisoned config is a poisoned run.
- **API keys in prompts/logs**: RAG systems log prompts containing
  user secrets; redact both sides.
- **Retrieval is an input channel**: a document store is a form field;
  treat retrieved chunks like any untrusted input before they drive
  tool calls.

## 9. Practice Exercises

1. **Token choice:** generate 100 tokens with `secrets`; assert they are
   all unique and correct length. Then show `random.seed` reproducibility
   makes `random` tokens predictable.
2. **Password store:** implement `hash_password`/`verify_password` with
   PBKDF2; assert correct/wrong verification, and that two hashes of the
   same password differ (salt).
3. **SQL guard:** build a `safe_query` and assert the injection payload
   returns `[]` while the legitimate ID returns the row.
4. **Path traversal guard:** with a root dir, assert `../..` payloads
   raise `ValueError` and in-root files read fine.
5. **YAML guard:** assert `safe_load` raises on a Python-tag payload and
   parses plain YAML correctly.
6. **Redaction:** assert `redact()` never returns the full secret and
   keeps only the last 4 chars.

## 10. Summary

- `secrets`, not `random`, for tokens; PBKDF2/bcrypt for passwords;
  `compare_digest` for secrets.
- Parameterized SQL, argument-list subprocess, `resolve()`+containment
  checks — the three classic injection classes, fixed by construction.
- `pickle.loads` and `yaml.load` are RCE on untrusted input; safe
  formats and `safe_load` are the defaults.
- ReDoS: linear regexes + length caps.
- Credentials live in env/secrets managers and never in logs.
- **Prompt injection is the new injection class**: model output is
  untrusted; dispatch tables, validation, and least privilege are the
  defenses.

## 11. Quick Reference

| Need | Tool |
|---|---|
| Random token/OTP | `secrets.token_urlsafe(32)` |
| Hash a password | `hashlib.pbkdf2_hmac` (bcrypt/argon2 in prod) |
| Compare secrets | `hmac.compare_digest` |
| Query the DB | Parameter binding (`?`/`%s`), never f-strings |
| Run a command | Argument list, never `shell=True` |
| Read a file by user path | `resolve()` + `is_relative_to(root)` |
| Deserialize untrusted data | JSON / safe formats, never `pickle` |
| Parse YAML | `yaml.safe_load` |
| Regex on input | Linear patterns, anchored, length-capped |
| Store API keys | Env / secrets manager; redact in logs |
| Verify TLS | Keep verification on (`verify=False` never in prod) |
| Check dependencies | `pip-audit` / `osv-scanner` in CI |
| Load a model artifact | Hash-verify from a trusted store |

## 12. Next Steps

- **`32-metaprogramming`** — the `@tool` registry and why tool-name
  resolution is a dispatch table, not `eval` (the security boundary of
  agent frameworks).
- **`34-debugging-techniques`** — how to *find* the security bug: reading
  tracebacks, `faulthandler`, deterministic repro under fixed seeds.
- **`08-mlops`** — model packaging (`.pkl` hygiene), artifact stores,
  and CI gates that enforce `pip-audit` and secret scanning.
- Practice the threat-modeling angle: for each pattern here, ask "what
  is the input channel, and what happens if it is adversarial?" — that
  question is the job description of an AI safety engineer.
