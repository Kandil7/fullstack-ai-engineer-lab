# CLI & Configuration — Glossary 46

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `sys.argv` | Attribute | List of command-line words; `argv[0]` is the script name |
| argparse | Module | Stdlib CLI parser: typed args, defaults, `--help`, subcommands |
| positional argument | Concept | Argument taken by position, without `--name` |
| optional argument | Concept | Argument introduced by `--name` |
| `type=` | Argument option | Converts the string to int/float/etc. |
| `required=True` | Argument option | Fails fast when the argument is missing |
| `choices=` | Argument option | Restricts values to an allowed set |
| `action="store_true"` | Argument option | Boolean flag: True if present |
| subcommands | Concept | Nested parsers for multi-mode tools (train/eval/serve) |
| `parse_args()` | Method | Parses argv (or a supplied list) into a namespace |
| `os.environ` | Mapping | Process environment variables — where config lives |
| `.env` file | Concept | Local-dev key=value file, loaded by a tiny parser |
| precedence | Concept | CLI > env > file > default resolution order |
| fail fast | Principle | Validate all config at startup and exit loudly |
| exit code | Concept | 0 = success; non-zero = failure; consumed by CI |
| `sys.stderr` | Stream | Where diagnostics/errors are printed |
| `SystemExit` | Exception | Exits the process with a code/message |
| testable main | Pattern | `def main(argv=None) -> int` so tests pass fake argv |

## Detailed Definitions

### `sys.argv`
**Definition**: The list of words on the command line; `argv[0]` is the script
name, the rest are raw strings.
**Example**:
```python
import sys
print(sys.argv)   # ['train.py', '--epochs', '10']
```
**Related**: argparse, `parse_args()`

### argparse
**Definition**: The standard-library module that turns argument definitions into
parsing, validation, and `--help` text.
**Example**:
```python
import argparse
p = argparse.ArgumentParser()
p.add_argument("--lr", type=float, default=1e-3)
args = p.parse_args()
```
**Related**: positional argument, subcommands

### positional argument
**Definition**: A required-by-position argument declared without `--`; order in
the definition fixes order on the command line.
**Example**:
```python
p.add_argument("dataset_dir")   # python tool.py data/
```
**Related**: optional argument

### optional argument
**Definition**: An argument introduced by `--name`; may have a default and be
omitted.
**Example**:
```python
p.add_argument("--seed", type=int, default=0)
```
**Related**: `type=`, `required=True`

### `type=`
**Definition**: Callable applied to the argument string, converting it (and
raising a readable error on bad input).
**Example**:
```python
p.add_argument("--epochs", type=int)   # "10" -> 10
```
**Related**: `choices=`

### `required=True`
**Definition**: Makes an argument mandatory; parse fails with usage text when
absent.
**Related**: fail fast

### `choices=`
**Definition**: Restricts a value to a set (or range), rejecting anything else
at parse time.
**Example**:
```python
p.add_argument("--seed", type=int, choices=range(0, 100))
```
**Related**: `type=`

### `action="store_true"`
**Definition**: Declares a boolean flag: True when present, False otherwise.
**Example**:
```python
p.add_argument("--verbose", action="store_true")
```
**Related**: optional argument

### subcommands
**Definition**: `add_subparsers` creates nested parsers selected by the first
word — the structure of `git`, `docker`, `uv`.
**Example**:
```python
sub = p.add_subparsers(dest="command", required=True)
sub.add_parser("train").add_argument("--epochs", type=int)
```
**Related**: `parse_args()`

### `parse_args()`
**Definition**: Parses `sys.argv[1:]` (or an explicitly supplied list) into a
namespace of validated values.
**Example**:
```python
args = p.parse_args(["--epochs", "5"])   # testable with fake argv
```
**Related**: `sys.argv`, testable main

### `os.environ`
**Definition**: The process's environment-variable mapping; the 12-factor home
of secrets and deployment config.
**Example**:
```python
import os
key = os.environ.get("OPENAI_API_KEY")
```
**Related**: `.env` file, precedence

### `.env` file
**Definition**: A local `key=value` file loaded into the environment by a small
parser (dev convenience only; never committed, never the production source).
**Example**:
```python
def load_dotenv(path=".env"):
    for line in Path(path).read_text().splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())
```
**Related**: `os.environ`, secrets

### precedence
**Definition**: The resolution order for a config value: CLI > env > config
file > default — each layer fills only what the higher layer left unset.
**Example**:
```python
lr = lr_cli if lr_cli is not None else float(os.environ.get("LR", "1e-3"))
```
**Related**: `os.environ`, defaults

### fail fast
**Definition**: The principle of validating every config dependency at startup
and exiting with a clear message, instead of failing obscurely later.
**Example**:
```python
if not os.environ.get("DATABASE_URL"):
    raise SystemExit("DATABASE_URL is required")
```
**Related**: `required=True`, exit code

### exit code
**Definition**: The integer a process returns; 0 success, non-zero failure —
what CI pipelines branch on.
**Example**:
```python
sys.exit(main())     # main returns int
```
**Related**: `SystemExit`, CI

### `sys.stderr`
**Definition**: The standard error stream; diagnostics and errors go here,
results stay on stdout.
**Example**:
```python
print("error: missing data", file=sys.stderr)
```
**Related**: exit code

### `SystemExit`
**Definition**: The exception that terminates the interpreter; raising it with
a message prints the message and exits non-zero.
**Related**: exit code

### testable main
**Definition**: The pattern `def main(argv: list[str] | None = None) -> int`
that lets unit tests pass a fake argv list and assert on the return code.
**Example**:
```python
def main(argv=None):
    args = parser.parse_args(argv)
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```
**Related**: `parse_args()`, pytest

## Key Concepts Summary

### CLI structure
- `sys.argv` is raw strings — let argparse do the typing
- Positionals for the main input, `--options` for knobs, `store_true` for flags
- Subcommands turn one tool into many modes

### Config discipline
- Secrets and deployment settings come from `os.environ`, never source
- Precedence: CLI > env > file > default
- Validate everything at boot; exit loudly on gaps

### Operability
- Errors to stderr, data to stdout, meaningful exit codes
- `main(argv=None) -> int` keeps the CLI unit-testable

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `sys.argv` — ___
2. `type=` — ___
3. `required=True` — ___
4. subcommands — ___
5. `os.environ` — ___
6. precedence — ___
7. fail fast — ___
8. testable main — ___

A. Convert the argument string to int/float at parse time
B. Environment-variable mapping; the 12-factor config home
C. Raw command-line word list
D. Exit at startup with a clear message when config is missing
E. CLI > env > file > default
F. Nested parsers for multi-mode tools
G. `main(argv=None) -> int` callable from tests
H. Fails parse when the argument is absent

**Answers:** 1-C, 2-A, 3-H, 4-F, 5-B, 6-E, 7-D, 8-G
