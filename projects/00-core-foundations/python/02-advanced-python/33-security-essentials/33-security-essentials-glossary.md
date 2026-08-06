# 33 — Security Essentials Glossary

## Quick Reference

| Term | Definition | Complexity |
|---|---|---|
| CSPRNG | Cryptographically secure PRNG — `secrets`, OS-backed | O(1) per draw |
| `secrets` | stdlib module for tokens/OTPs — unpredictable | O(n) |
| `random` | PRNG for simulation — predictable when seeded | O(1) |
| Password hashing | Slow, salted key derivation (PBKDF2/bcrypt/argon2) | ~50 ms/hash |
| Salt | Random bytes per password; defeats rainbow tables | O(1) |
| KDF | Key derivation function — the slow hash class | O(iterations) |
| `hmac.compare_digest` | Constant-time secret comparison | O(n) |
| Timing attack | Extracting secrets from response-time differences | — |
| SQL injection | Input becomes SQL structure via string interpolation | — |
| Parameterized query | `?`/`%s` placeholders; input stays data | O(1) |
| Command injection | Input becomes shell commands via `shell=True` | — |
| Path traversal | `../` escapes the allowed directory | — |
| `is_relative_to` | `Path` containment check after `resolve()` | O(path) |
| Pickle RCE | `pickle.loads` executes `__reduce__` payloads | O(data) |
| `__reduce__` | Pickle hook; attacker-controlled callable + args | — |
| YAML object tag | `!!python/object/apply:...` constructs Python objects | — |
| `yaml.safe_load` | YAML parser that refuses Python-object tags | O(data) |
| ReDoS | Exponential regex backtracking on crafted input | O(2^n) worst |
| Redaction | Masking secrets before they reach logs | O(n) |
| TLS verification | Checking server certs (`verify=False` is the danger) | O(1) |
| Least privilege | Minimal permissions per process/user | — |
| CVE | Known vulnerability in a dependency | — |
| Supply-chain attack | Malicious artifact (model file, package) at load time | — |
| Prompt injection | Untrusted text steering model behavior via instructions | — |
| Dispatch table | `{name: callable}` — the safe tool-selection boundary | O(1) |

## Detailed Definitions

### CSPRNG
**Definition:** A cryptographically secure pseudorandom number generator
— output is unpredictable even given previous outputs and the seed.
Python exposes the OS CSPRNG through `secrets`. Anything used as a
credential must come from a CSPRNG.

```python
import secrets
token = secrets.token_urlsafe(32)   # URL-safe random token
```

**Related Terms:** `secrets`, `random`

### `secrets`
**Definition:** The stdlib module for generating secure tokens: API
keys, session tokens, password-reset links, OTPs. Backed by the OS
CSPRNG; never seedable, never reproducible.

```python
import secrets
print(secrets.token_hex(16))
```

```text
# Output:
# 3f8a... (random on every run)
```

**Related Terms:** CSPRNG, `random`

### `random`
**Definition:** The PRNG for simulation, shuffles, and games.
Deterministic given a seed — `random.seed(42)` reproduces the same
sequence. This determinism is exactly why it must never generate
tokens.

```python
import random
random.seed(42)
print(random.choice("abcd"))   # same result after every seed(42)
```

```text
# Output:
# c  (deterministic)
```

**Related Terms:** `secrets`, CSPRNG

### Password hashing
**Definition:** Storing a one-way, *slow*, salted transform of a
password. "Slow" is the feature: each attacker guess costs ~50 ms
instead of nanoseconds. Never store plaintext, MD5, SHA1, or unsalted
hashes.

```python
import hashlib, secrets

def hash_password(password, salt=None, iterations=100_000):
    salt = salt or secrets.token_bytes(16)
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt,
                               iterations), salt
```

**Related Terms:** Salt, KDF

### Salt
**Definition:** Random bytes generated per password, mixed into the
hash. Two users with the same password get different hashes; precomputed
rainbow tables become useless.

```python
h1, s1 = hash_password("p@ss")
h2, s2 = hash_password("p@ss")
print(h1 == h2)   # False — different salts
```

```text
# Output:
# False
```

**Related Terms:** Password hashing

### KDF
**Definition:** Key derivation function — the *slow hash* family
(PBKDF2, bcrypt, argon2, scrypt). Deliberately expensive so brute force
is impractical. PBKDF2 is stdlib; bcrypt/argon2 are the production
preference.

**Related Terms:** Password hashing, Salt

### `hmac.compare_digest`
**Definition:** Constant-time comparison for secrets. `==` exits at the
first mismatch, leaking prefix information through timing; this function
runs in time proportional to the input length regardless of where they
differ.

```python
import hmac
print(hmac.compare_digest(b"abc", b"abc"))
```

```text
# Output:
# True
```

**Related Terms:** Timing attack

### Timing attack
**Definition:** Recovering secret material by measuring how long
operations take. `==` on a 32-char token returns after k+1 comparisons
when k prefix bytes match — an attacker who can measure response time
can recover the token byte by byte.

**Related Terms:** `hmac.compare_digest`

### SQL injection
**Definition:** The vulnerability where input is interpolated into SQL,
turning input into structure. The payload `1' OR '1'='1` closes the
string literal and appends `OR TRUE`, dumping the table.

```python
# BAD:  f"SELECT ... WHERE id = '{user_id}'"
# GOOD: "SELECT ... WHERE id = ?", (user_id,)
```

**Related Terms:** Parameterized query, Injection classes

### Parameterized query
**Definition:** SQL with placeholders (`?` in sqlite3, `%s` in
psycopg); the driver binds values as data. The input can never become
SQL structure, so injection is impossible by construction.

**Related Terms:** SQL injection

### Command injection
**Definition:** When user input reaches a shell, `;`, `&&`, and
backticks become commands. `subprocess.run(cmd, shell=True)` is the
switch that enables it; argument lists (`["echo", user_input]`) keep
input as data.

**Related Terms:** Injection classes, `subprocess`

### Path traversal
**Definition:** Using `../` sequences in filenames to escape the
allowed directory and read/write anywhere. Defeated by `resolve()` (which
collapses `..` and symlinks) + `is_relative_to(root)`.

```python
from pathlib import Path

candidate = (root / filename).resolve()
if not candidate.is_relative_to(root.resolve()):
    raise ValueError("path escapes the root")
```

**Related Terms:** `is_relative_to`, Injection classes

### `is_relative_to`
**Definition:** `Path` method: `p.is_relative_to(q)` is True when `p`
is inside `q`. The containment check that makes path handling safe —
always after `resolve()`.

**Related Terms:** Path traversal

### Pickle RCE
**Definition:** `pickle.loads` deserializes objects by executing
protocol opcodes — including a `__reduce__` that names any callable with
any arguments. A crafted pickle runs arbitrary code:

```python
class Evil:
    def __reduce__(self):
        return (os.system, ("echo PWNED",))
```

**Related Terms:** `__reduce__`, Supply-chain attack

### `__reduce__`
**Definition:** Pickle's serialization hook. The object unpickles by
*invoking* the returned `(callable, args)` — which is why untrusted
pickles are RCE. Never `pickle.loads` anything you did not produce.

**Related Terms:** Pickle RCE

### YAML object tag
**Definition:** `!!python/object/apply:...` tags in YAML instruct the
parser to construct Python objects — code execution. `yaml.load`
honors them; `yaml.safe_load` refuses and raises `yaml.YAMLError`.

**Related Terms:** `yaml.safe_load`

### `yaml.safe_load`
**Definition:** The safe YAML parser: plain data only (dicts, lists,
scalars), no Python-object construction. The *only* `yaml` load function
for untrusted configs.

```python
import yaml
yaml.safe_load("a: 1")     # {'a': 1}
```

**Related Terms:** YAML object tag

### ReDoS
**Definition:** Regular expression denial of service. Nested quantifiers
(`(a+)+$`) backtrack exponentially on near-miss inputs: 30 characters of
`a` then `b` can take minutes of CPU. Mitigations: linear patterns,
anchors, length caps, timeouts.

```python
# BAD:  r"^(a+)+$"
# GOOD: r"^a+$"
```

**Related Terms:** Injection classes

### Redaction
**Definition:** Masking secrets before they reach logs:
`***cdef` instead of the full key. Logs are searched by attackers and
ingested by monitoring; credentials in logs are leaked credentials.

**Related Terms:** Secret management

### TLS verification
**Definition:** The client checking the server's certificate chain.
`verify=False` (requests/httpx) disables it — the connection is
encrypted but the peer is unauthenticated: a man-in-the-middle dream.
Never disable verification in production.

**Related Terms:** Secret management

### Least privilege
**Definition:** Giving each process/user only the permissions it needs.
A compromised embedding worker that can only read input and write
output is contained; one running as root is a root compromise.

**Related Terms:** Supply-chain attack

### CVE
**Definition:** A cataloged known vulnerability in a package. `pip-audit`
and `osv-scanner` compare your dependency tree against the CVE
databases in CI — a pinned vulnerable dependency is a scheduled
incident.

**Related Terms:** Supply-chain attack

### Supply-chain attack
**Definition:** Malicious artifacts (packages, model files, configs)
injected at load time. `.pkl` model files are the AI-specific vector:
a hijacked model card executes code on your inference server. Verify
hashes and provenance before loading.

**Related Terms:** Pickle RCE, CVE

### Prompt injection
**Definition:** The injection class of the LLM era: untrusted text
(retrieved documents, web content, user profiles) concatenated into a
prompt, whose *instructions* override the system's. Defense shape
mirrors SQL injection: treat model input/output as data, validate tool
arguments, whitelist via dispatch tables, least privilege for tools.

**Related Terms:** Dispatch table, Injection classes

### Dispatch table
**Definition:** `{name: callable}` — resolving an LLM's tool choice
through a dict lookup means the worst the model can do is pick a
registered function. `eval` on model output would execute arbitrary
code. The table is the security boundary.

**Related Terms:** Prompt injection

## Key Concepts Summary

1. **Untrusted input never becomes code or structure.** Parameterized
   SQL, argument-list subprocess, `safe_load`, dispatch tables — the
   pattern is always "input stays data".
2. **Security-relevant randomness is a different tool.** `secrets`, not
   `random`; slow KDFs for passwords; `compare_digest` for comparisons.
3. **Deserialization is a code path.** `pickle.loads` and `yaml.load`
   execute payloads; `.pkl` models are supply-chain vectors.
4. **Logs leak.** Redact credentials; keys live in env/secrets managers.
5. **Model output is untrusted input.** Prompt injection is SQL
   injection wearing an LLM costume; the same defenses apply.

## Practice Terms

1. **Why is `random` unacceptable for tokens?**
   *Answer:* It is a seeded PRNG — reproducible sequences, so an
   attacker who can guess/observe the seed and past outputs can predict
   future tokens. `secrets` uses the OS CSPRNG, which has no such
   relationship.
2. **Why must password hashing be slow?**
   *Answer:* The defense against offline brute force is per-guess cost.
   Fast hashes (MD5/SHA1) allow billions of guesses per second; a KDF
   at ~50 ms per guess makes cracking impractical.
3. **What exactly does `resolve()` + `is_relative_to()` protect?**
   *Answer:* `resolve()` collapses `..` and symlinks into the real
   absolute path; `is_relative_to()` verifies that real path stays
   inside the root. Without both, `../../etc/passwd`-style payloads
   escape.
4. **How is prompt injection like SQL injection?**
   *Answer:* In both, untrusted text is concatenated into a
   "program" (SQL string / prompt) and its content becomes structure
   (SQL clause / instructions). Both are defended by treating the input
   as data: parameter binding, validation, whitelists, least privilege.
5. **What is the safe way to load a downloaded model file?**
   *Answer:* Prefer a serialization format that cannot execute code
   (safetensors/JSON weights); if pickle is unavoidable, load only from
   a trusted artifact store, verify the artifact's cryptographic hash,
   and run in a sandboxed/low-privilege process.
