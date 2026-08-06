"""Challenge 46 solution — reference implementation with reasoning comments."""
from __future__ import annotations


def parse_key_value(args: list[str]) -> dict[str, str]:
    """Parse --key=value and --key value forms into a dict.

    Raises ValueError for a flag with no value; repeated keys keep the last
    occurrence (later overrides earlier on the command line).
    """
    result: dict[str, str] = {}
    i = 0
    while i < len(args):
        token = args[i]
        if not token.startswith("--"):
            raise ValueError(f"expected a --flag, got {token!r}")
        body = token[2:]
        if "=" in body:
            key, _, value = body.partition("=")
            if not key:
                raise ValueError(f"empty flag name in {token!r}")
            result[key] = value
            i += 1
        else:
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                raise ValueError(f"missing value for {token!r}")
            result[body] = args[i + 1]
            i += 2
    return result


def resolve(layers: list[dict | None]) -> dict:
    """Merge layers so earlier dicts win; fill only missing keys.

    This is the CLI > env > file > default precedence: each layer supplies
    what the higher-precedence layers left unset.
    """
    merged: dict = {}
    for layer in layers:
        if not layer:
            continue
        for key, value in layer.items():
            merged.setdefault(key, value)   # first (highest) layer wins
    return merged


def main(argv: list[str] | None, out, err) -> int:
    """Testable subcommand CLI: train/eval with required args.

    Returns 0 on success, 2 on usage errors; writes results to `out` and
    diagnostics to `err` — never touching the real process.
    """
    args = list(argv) if argv is not None else []
    if not args:
        err.write("usage: tool <train|eval> [options]\n")
        return 2

    command, rest = args[0], args[1:]
    try:
        opts = parse_key_value(rest)
    except ValueError as e:
        err.write(f"error: {e}\n")
        return 2

    if command == "train":
        if "epochs" not in opts:
            err.write("error: train requires --epochs\n")
            return 2
        try:
            epochs = int(opts["epochs"])
        except ValueError:
            err.write(f"error: epochs must be an int, got {opts['epochs']!r}\n")
            return 2
        out.write(f"training {epochs} epochs\n")
        return 0

    if command == "eval":
        if "checkpoint" not in opts or "data" not in opts:
            err.write("error: eval requires --checkpoint and --data\n")
            return 2
        out.write(f"eval {opts['checkpoint']}\n")
        return 0

    err.write(f"error: unknown command {command!r}\n")
    return 2
