# Challenge 33: Security Essentials

Harden a tiny credential-store API: timing-safe verify, salted
PBKDF2 hashing, SQL injection resistance, and safe deserialization —
then prove each attack is blocked.

## 🥉 Bronze — Password Store (~15 min)

**Task:** Implement `hash_password(password, salt=None, iterations=100_000)
-> (digest, salt)` using PBKDF2-HMAC-SHA256 with a **fresh random salt**
when none is given, and `verify_password(password, digest, salt,
iterations=100_000) -> bool` using `hmac.compare_digest`.

| Input | Expected |
|-------|----------|
| `hash_password("x")` twice | different digests (random salts) |
| `verify_password("x", ...)` | `True` |
| `verify_password("y", ...)` | `False` |
| digest length | 32 bytes; salt 16 bytes |

**Constraints:** `verify_password` must use `hmac.compare_digest`, never
`==`. n ≤ 10^3 verifications. Never store/return plaintext.

---

## 🥈 Silver — Safe Query Layer (~35 min)

**Task:** Implement `SafeStore` wrapping a sqlite3 in-memory DB with
parameterized queries only:

```python
class SafeStore:
    def __init__(self): ...                      # CREATE TABLE users(id TEXT, name TEXT)
    def add(self, user_id: str, name: str) -> None: ...
    def find(self, user_id: str) -> list[tuple]: ...   # parameterized
```

| Input | Expected |
|-------|----------|
| `add("1", "alice"); find("1")` | `[("1", "alice")]` |
| `find("1' OR '1'='1")` | `[]` (injection blocked) |
| `find("x")` | `[]` |

**Constraints:** no f-string SQL anywhere; all queries use `?`
placeholders. n ≤ 10^3 rows.

---

## 🥇 Gold — Safe Config Loader (~75 min)

**Task:** Implement `load_config(path: Path) -> dict` that parses YAML
with `yaml.safe_load` only, refuses keys outside a whitelist
(`{"model", "batch_size", "retries"}`), and rejects values of the wrong
type (model: str, batch_size: int, retries: int). Plus
`is_safe_path(root: Path, filename: str) -> Path` that resolves and
verifies containment.

**API:**
```python
ALLOWED = {"model", "batch_size", "retries"}

def load_config(path: Path) -> dict: ...
def is_safe_path(root: Path, filename: str) -> Path: ...  # raises ValueError
```

| Input | Expected |
|-------|----------|
| `{"model": "base", "batch_size": 8}` | returns it |
| `{"model": "base", "evil_key": 1}` | raises `ValueError` |
| `{"model": 123}` | raises `ValueError` (wrong type) |
| YAML with `!!python/object/apply:...` | raises `yaml.YAMLError` |
| `is_safe_path(root, "config.yaml")` | resolved `Path` inside root |
| `is_safe_path(root, "../etc/passwd")` | raises `ValueError` |

**Constraints:** `load_config` must use `yaml.safe_load`; `is_safe_path`
must call `.resolve()` before `.is_relative_to()`. No `eval`/`exec`
anywhere. n ≤ 10^2 config keys.

**Follow-up:** how would you add prompt-injection defense to a tool that
reads `load_config` output and passes it to an LLM?

---

## Running

```bash
pytest challenges/33-security-essentials/test_challenge.py -v
```
