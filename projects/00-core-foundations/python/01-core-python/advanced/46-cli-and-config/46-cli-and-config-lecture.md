# 01-core-python — 46: CLI & Configuration — The Training-Script Interface

## Topic Overview

Every serious Python tool is a command-line interface: `train.py --epochs 10
--lr 3e-4`, `eval.py --checkpoint runs/best.pt`, `serve.py --port 8080`. And
every serious tool reads its configuration from the environment — never from
source code. `argparse` gives you typed arguments, subcommands, and `--help`
for free; `os.environ` is where API keys and secrets live (12-factor rule:
config in the environment).

For AI and backend engineers this is the daily interface to your own work:
training runs are parameterized CLI invocations, hyperparameters follow
precedence (CLI > env > config file > default), and a missing key fails fast
at startup instead of failing mysteriously at 3 a.m.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read `sys.argv` and explain its shape
2. Build a typed CLI with `argparse`: positionals, optionals, flags, defaults
3. Use `parser.parse_args()` and explain exit behavior on errors
4. Add subcommands (`train`, `eval`, `serve`)
5. Read configuration from `os.environ` with defaults
6. Apply config precedence: CLI > env > file > default
7. Fail fast at startup on missing required config
8. Use exit codes and `sys.stderr` properly
9. Load `.env` files in development without a dependency

## Prerequisites

| Need | Where |
|------|-------|
| Functions and `__main__` | `21-functions.py`, `25-modules.py` lectures |
| Exceptions | `30-try-except.py` lecture |
| Path handling | `42-pathlib` lecture |

## 1. `sys.argv` — The Raw View

`sys.argv` is the list of command-line words; `argv[0]` is the script name:

```python
import sys
print(sys.argv)
```

```bash
python train.py --epochs 10 --lr 3e-4
# ['train.py', '--epochs', '10', '--lr', '3e-4']
```

Everything is a string. You would hand-roll parsing, types, defaults, `--help`,
and error messages — which is exactly what `argparse` already does.

## 2. argparse Basics

```python
import argparse

parser = argparse.ArgumentParser(description="Train an ML model")
parser.add_argument("--epochs", type=int, default=10, help="number of epochs")
parser.add_argument("--lr", type=float, default=1e-3, help="learning rate")
parser.add_argument("--data", required=True, help="path to dataset")
parser.add_argument("--verbose", action="store_true", help="verbose output")

args = parser.parse_args()
print(args.epochs, args.lr, args.data, args.verbose)
```

```bash
python train.py --data data/ --epochs 20
# 20 0.001 data/ False

python train.py                    # error: the following arguments are required: --data
python train.py --help             # auto-generated usage text
```

Key behaviors: `type=` converts strings, `required=True` fails fast, and
`--help` is generated from the definitions — the CLI documents itself.

## 3. Positionals and Type Validation

Positional arguments come without `--`; argparse validates types and ranges for
you:

```python
parser.add_argument("dataset_dir", help="dataset directory (positional)")
parser.add_argument("--seed", type=int, choices=range(0, 100), default=0)
```

```bash
python train.py data/ --seed 42        # OK
python train.py --seed 999             # error: invalid choice
```

`choices` turns a typo into an immediate, readable error.

## 4. Subcommands — One Tool, Many Modes

```python
parser = argparse.ArgumentParser(prog="devmate")
sub = parser.add_subparsers(dest="command", required=True)

train_p = sub.add_parser("train", help="train a model")
train_p.add_argument("--epochs", type=int, default=10)

eval_p = sub.add_parser("eval", help="evaluate a checkpoint")
eval_p.add_argument("--checkpoint", required=True)

args = parser.parse_args()
if args.command == "train":
    print(f"training for {args.epochs} epochs")
elif args.command == "eval":
    print(f"evaluating {args.checkpoint}")
```

```bash
python devmate.py train --epochs 20   # training for 20 epochs
python devmate.py eval --checkpoint runs/best.pt
```

This is the shape of real tools: `git`, `uv`, `docker` are all subcommand CLIs.

## 5. Configuration from the Environment

Secrets and per-environment settings come from the environment, not from args
or source:

```python
import os

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY is not set")

port = int(os.environ.get("PORT", "8080"))     # default, typed
debug = os.environ.get("DEBUG", "").lower() in {"1", "true", "yes"}
```

`os.environ.get(name, default)` never raises; the missing-key check converts a
silent failure into an immediate, explicit one.

## 6. Config Precedence — CLI > Env > File > Default

The rule that prevents "it worked locally": let a lower-precedence layer fill
only what a higher layer left unset.

```python
def resolve(lr_cli, lr_env, lr_file, default=1e-3):
    for candidate in (lr_cli, lr_env, lr_file, default):
        if candidate is not None:
            return candidate
    return default
```

```text
CLI (explicit, per-run)   >  env (per-deployment)   >  file (per-project)
  >  default (in code)
```

## 7. Exit Codes and stderr

Scripts communicate success/failure through exit codes; diagnostics go to
`stderr`, results to `stdout`:

```python
import sys

def main(argv: list[str] | None = None) -> int:
    args = parser.parse_args(argv)
    if not Path(args.data).exists():
        print(f"error: {args.data} does not exist", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

```bash
python train.py --data nope; echo $?   # error: nope does not exist / 2
```

Returning `int` from `main` makes the function testable — pass a fake `argv`
list instead of touching the real process.

## 8. `.env` Files — Dev Convenience, Not a Secret Store

A tiny parser (no dependency needed for a fixed format):

```python
def load_dotenv(path: str = ".env") -> None:
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"'))
```

`.env` is for local development; production secrets belong in the deployment's
secret manager, exposed as real environment variables.

## 9. Production Pattern — Fail-Fast Startup

```python
REQUIRED_ENV = ("OPENAI_API_KEY", "DATABASE_URL")

def check_environment() -> None:
    missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
    if missing:
        raise SystemExit(
            "missing required config: " + ", ".join(missing)
        )

def main(argv: list[str] | None = None) -> int:
    args = parser.parse_args(argv)
    check_environment()
    ...
    return 0
```

A service that validates everything it needs at boot — and exits loudly if
anything is missing — never limps into production half-configured.

## Common Mistakes to Avoid

### Mistake 1: Hard-coding config in source

```python
# WRONG — the key is committed to git
api_key = "sk-..."
# CORRECT — read from the environment, set at deploy time
api_key = os.environ["OPENAI_API_KEY"]
```

### Mistake 2: Parsing `sys.argv` by hand

```python
# WRONG — no --help, no types, no errors
lr = float(sys.argv[sys.argv.index("--lr") + 1])
# CORRECT
args = parser.parse_args()
```

### Mistake 3: Assuming CLI values are typed

```python
# WRONG — argv is strings; "10" + 1 raises
epochs = sys.argv[2] + 1
# CORRECT — argparse type=int converts for you
```

### Mistake 4: Swallowing config errors

```python
# WRONG — start anyway, crash later at a random call site
port = os.environ.get("PORT", "not-a-number")
# CORRECT — parse and validate at startup, exit 2 with a clear message
```

### Mistake 5: Testing via real process invocation only

```python
# WRONG — hard to test; touches the real environment
# CORRECT — main(argv) takes an optional argv list; unit-test with fake argv
```

## Best Practices

1. Every tool gets `argparse` with `--help`, types, and defaults
2. Subcommands for multi-mode tools (train/eval/serve)
3. Secrets from `os.environ`, never source, never args
4. Precedence: CLI > env > file > default
5. Validate required config at startup and exit loudly
6. Print errors to `stderr`, data to `stdout`, use exit codes
7. Make `main(argv=None)` return `int` so it is testable
8. Keep `.env` out of git; document the variables in README
9. Use `choices`, `type`, and `required` to catch mistakes early

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `parse_args()` | O(arguments) | negligible at startup |
| env lookup | O(1) | once per boot, not per request |
| hand-rolled argv parsing | O(n) + bug-prone | never cheaper than argparse |
| missing-config failure | O(1) at boot | vs. obscure failure hours later |

**At scale:** the cost is paid once at startup. The real price of bad CLI/config
design is operational: misconfigured runs, leaked secrets, and support calls.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| typed args | `train.py --epochs --lr --seed` — the standard training interface |
| env config | API keys, model names, DB URLs via 12-factor env |
| subcommands | one tool: `train / eval / serve / export` |
| precedence | per-run overrides vs deployment config vs repo defaults |
| fail-fast boot | a serving container refuses to start without its key |
| exit codes | CI stages depend on exit status of training/eval steps |

**Scale note:** when you run 1,000 training runs a month, the difference between
self-documenting CLIs and ad-hoc scripts is the difference between an auditable
pipeline and an archaeology project. Every run's config should be recoverable
from the command line that launched it.

## Practice Exercises

### Exercise 1: Minimal Trainer CLI (Easy)
Build a parser with `--epochs` (int, default 10), `--lr` (float, default
1e-3), and `--data` (required). Print the resolved values.

### Exercise 2: Config Precedence (Medium)
Implement `resolve(lr_cli, lr_env, lr_file, default)` and verify precedence
order with unit tests (use a fake `argv` list and `monkeypatch`).

### Exercise 3: Subcommand Tool (Hard)
Build a `devmate` tool with `train` and `eval` subcommands, required
`--checkpoint` on eval, `check_environment()` for `OPENAI_API_KEY`, and a
testable `main(argv=None) -> int` that returns 0/2 with messages on stderr.

## Summary

| Concept | Description |
|---------|-------------|
| `sys.argv` | raw string list; `argv[0]` is the script name |
| `argparse` | typed args, defaults, `choices`, subcommands, free `--help` |
| `os.environ` | where secrets and deployment config live |
| precedence | CLI > env > file > default |
| fail fast | validate config at startup, exit loudly |
| exit codes | 0 success, non-zero failure — consumed by CI |
| `.env` | local-dev convenience; secrets live in the deployment |

Every AI tool is a CLI reading config from its environment. Get these two
skills right and every pipeline you ever build starts on solid ground.

## Quick Reference

| Task | Idiom |
|------|-------|
| Typed option | `parser.add_argument("--lr", type=float, default=1e-3)` |
| Required arg | `parser.add_argument("--data", required=True)` |
| Boolean flag | `action="store_true"` |
| Subcommands | `add_subparsers(dest="command", required=True)` |
| Env with default | `os.environ.get("PORT", "8080")` |
| Fail fast | `if not key: raise SystemExit("missing ...")` |
| Testable main | `def main(argv: list[str] \| None = None) -> int` |
| Errors | `print(msg, file=sys.stderr)` |

## Next Steps

Next: **[47-exceptions-advanced](47-exceptions-advanced-lecture.md)** — structured failure handling.
Continues in: **[02-advanced-python — 05 type hints](../../02-advanced-python/lectures/05-type-hints-lecture.md)** and
**[08-mlops — 01 reproducibility](../../../08-mlops/lectures/01-reproducibility-lecture.md)**.
Official docs: https://docs.python.org/3/library/argparse.html
