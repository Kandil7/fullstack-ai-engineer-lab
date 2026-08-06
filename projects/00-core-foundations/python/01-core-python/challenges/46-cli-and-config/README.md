# Challenge 46: CLI & Configuration

## 🥉 Bronze — Key-Value Parser (~15 min)

**Task:** Implement `parse_key_value(args: list[str]) -> dict[str, str]`
parsing `--key=value` and `--key value` forms (no flag support needed).

| Input | Expected |
|-------|----------|
| `["--lr=1e-3", "--epochs", "10"]` | `{"lr": "1e-3", "epochs": "10"}` |
| `["--data", "x", "--seed=42"]` | `{"data": "x", "seed": "42"}` |
| `["--key"]` (missing value) | raises `ValueError` |

**Constraints:** n ≤ 10^3.

---

## 🥈 Silver — Precedence Merger (~35 min)

**Task:** Implement `resolve(layers: list[dict | None]) -> dict` merging
layers so *earlier* dicts win (CLI > env > file > default), filling only keys
not already present.

| Input | Expected |
|-------|----------|
| `[{"lr": "1e-4"}, {"lr": "1e-3", "seed": "0"}, {"seed": "1"}]` | `{"lr": "1e-4", "seed": "0"}` |
| `[None, {"a": "1"}]` | `{"a": "1"}` |
| `[{}]` | `{}` |

**Constraints:** n ≤ 10^3 dicts. Must not mutate inputs.

---

## 🥇 Gold — Testable Subcommand CLI (~75 min)

**Task:** Implement `main(argv: list[str] | None, out, err) -> int` for a tool
with `train` and `eval` subcommands. `train` requires `--epochs` (int);
`eval` requires `--checkpoint` and `--data`. Missing required args print to
`err` and return 2. Success prints a summary line to `out` and returns 0.

**Signature:**
```python
def main(argv: list[str] | None, out, err) -> int: ...
```

| argv | out contains | return |
|------|--------------|--------|
| `["train", "--epochs", "10"]` | `"training 10 epochs"` | 0 |
| `["eval", "--checkpoint", "best.pt", "--data", "d"]` | `"eval best.pt"` | 0 |
| `["train"]` | — | 2 (message on err) |
| `["eval", "--checkpoint", "best.pt"]` | — | 2 (message on err) |

**Constraints:** 10^3 invocations; must be pure (no real process exit, no
stderr writes outside `err`).

**Follow-up:** how would you add `--verbose` and env-var fallbacks?
(Answer: more layers in `resolve`, a store_true flag.)

---

## Running

```bash
pytest challenges/46-cli-and-config/test_challenge.py -v
```
