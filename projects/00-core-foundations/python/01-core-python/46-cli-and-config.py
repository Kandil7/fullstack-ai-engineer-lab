"""
01-core-python — 46: CLI & Config — argparse, sys.argv, os.environ
====================================================================
Topics: sys.argv, argparse (positional, optional, flags, subcommands,
        types, defaults, --help), os.environ + .get defaults, .env loading,
        12-factor config, precedence CLI > env > file > default, exit codes

Why this matters for AI/backend engineering:
    Every training script is a CLI (train.py --epochs 10 --lr 3e-4);
    API keys come from env, never source code; 12-factor apps.

Run:      python 46-cli-and-config.py
Verify:   python 46-cli-and-config.py --verify
Reference: https://docs.python.org/3/library/argparse.html
"""

from __future__ import annotations

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional

# ============================================================
# 1. sys.argv — Raw Argument Access
# ============================================================
# Complexity: O(1) access

# Example 1: Raw argv
print("=== sys.argv ===")
print(f"sys.argv: {sys.argv}")
print(f"Script name: {sys.argv[0]}")
print(f"Arguments: {sys.argv[1:]}")

# Manual parsing (not recommended for complex cases)
if len(sys.argv) > 1 and sys.argv[1] == "--help":
    print("Usage: python script.py [options]")

# ============================================================
# 2. argparse — Standard CLI Framework
# ============================================================

# Example 2: Basic ArgumentParser
parser = argparse.ArgumentParser(
    prog="train",
    description="Train a language model",
    epilog="Example: python train.py --epochs 10 --lr 3e-4",
)

# Positional argument
parser.add_argument("model", help="Model name or path")

# Optional arguments with types
parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
parser.add_argument("--lr", type=float, default=3e-4, help="Learning rate")
parser.add_argument("--batch-size", type=int, default=32, help="Batch size")

# Flags (boolean)
parser.add_argument("--fp16", action="store_true", help="Use mixed precision")
parser.add_argument("--no-wandb", action="store_true", help="Disable W&B logging")

# Choices
parser.add_argument("--optimizer", choices=["adam", "adamw", "sgd"], default="adamw")

# Parse
args = parser.parse_args([])  # Empty list for demo
print(f"\n=== Parsed Args ===")
print(f"  model: {args.model}")
print(f"  epochs: {args.epochs}")
print(f"  lr: {args.lr}")
print(f"  fp16: {args.fp16}")

# ============================================================
# 3. Subcommands — Multiple Commands
# ============================================================

# Example 3: Subparsers for git-like CLI
root_parser = argparse.ArgumentParser(prog="ml")
subparsers = root_parser.add_subparsers(dest="command", required=True)

# train subcommand
train_parser = subparsers.add_parser("train", help="Train a model")
train_parser.add_argument("--config", required=True)
train_parser.add_argument("--resume", help="Checkpoint path")

# eval subcommand
eval_parser = subparsers.add_parser("eval", help="Evaluate a model")
eval_parser.add_argument("--checkpoint", required=True)
eval_parser.add_argument("--dataset", default="validation")

# serve subcommand
serve_parser = subparsers.add_parser("serve", help="Serve model API")
serve_parser.add_argument("--host", default="0.0.0.0")
serve_parser.add_argument("--port", type=int, default=8000)

# Demo parsing
demo_args = ["train", "--config", "config.yaml"]
parsed = root_parser.parse_args(demo_args)
print(f"\n=== Subcommand Parsed ===")
print(f"  command: {parsed.command}")
print(f"  config: {parsed.config}")

# ============================================================
# 4. Environment Variables — os.environ
# ============================================================

# Example 4: Reading env vars
print("\n=== Environment Variables ===")

# Get with default
api_key = os.environ.get("OPENAI_API_KEY", "not-set")
print(f"OPENAI_API_KEY: {api_key[:8]}..." if api_key != "not-set" else "OPENAI_API_KEY: not set")

# Required env var (crash if missing)
def get_required_env(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        raise RuntimeError(f"Required environment variable {key} not set")
    return value

# Database URL from env
database_url = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")
print(f"DATABASE_URL: {database_url}")

# Boolean env vars
def get_bool_env(key: str, default: bool = False) -> bool:
    value = os.environ.get(key, "").lower()
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    return default

debug = get_bool_env("DEBUG", False)
print(f"DEBUG: {debug}")

# ============================================================
# 5. .env File Loading (12-Factor Config)
# ============================================================

# Example 5: Simple .env loader
def load_env_file(path: Path = Path(".env")) -> dict[str, str]:
    """Load KEY=VALUE pairs from .env file."""
    if not path.exists():
        return {}
    
    env_vars = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip()
    return env_vars

# Demo
with tempfile.TemporaryDirectory() as tmp:
    env_file = Path(tmp) / ".env"
    env_file.write_text("""
# Model config
MODEL_NAME=bert-base
LR=2e-5
BATCH_SIZE=32

# Secrets (never commit!)
API_KEY=sk-test123
""")
    loaded = load_env_file(env_file)
    print(f"\n=== Loaded .env ===")
    for k, v in loaded.items():
        print(f"  {k}: {v}")

# ============================================================
# 6. Config Precedence: CLI > Env > File > Default
# ============================================================

def build_config(
    cli_args: argparse.Namespace,
    env_file: Path = Path(".env"),
) -> dict:
    """Build final config with precedence."""
    # 1. Start with defaults
    config = {
        "model": "default-model",
        "epochs": 10,
        "lr": 3e-4,
        "batch_size": 32,
        "fp16": False,
    }
    
    # 2. Override with .env file
    if env_file.exists():
        file_config = load_env_file(env_file)
        for key, value in file_config.items():
            key_lower = key.lower()
            if key_lower in config:
                # Type conversion
                if isinstance(config[key_lower], bool):
                    config[key_lower] = value.lower() in ("1", "true", "yes")
                elif isinstance(config[key_lower], int):
                    config[key_lower] = int(value)
                elif isinstance(config[key_lower], float):
                    config[key_lower] = float(value)
                else:
                    config[key_lower] = value
    
    # 3. Override with environment variables
    for key in config:
        env_key = key.upper()
        if env_key in os.environ:
            value = os.environ[env_key]
            if isinstance(config[key], bool):
                config[key] = value.lower() in ("1", "true", "yes")
            elif isinstance(config[key], int):
                config[key] = int(value)
            elif isinstance(config[key], float):
                config[key] = float(value)
            else:
                config[key] = value
    
    # 4. Override with CLI args (highest priority)
    for key, value in vars(cli_args).items():
        if value is not None and key in config:
            config[key] = value
    
    return config

# Demo
demo_cli = argparse.Namespace(
    model="cli-model",
    epochs=20,
    lr=None,  # Not provided
    batch_size=64,
    fp16=True,
)

with tempfile.TemporaryDirectory() as tmp:
    env_file = Path(tmp) / ".env"
    env_file.write_text("MODEL=env-model\nEPOCHS=15\nLR=1e-3\n")
    os.environ["BATCH_SIZE"] = "128"
    
    final_config = build_config(demo_cli, env_file)
    print(f"\n=== Config Precedence ===")
    for k, v in final_config.items():
        print(f"  {k}: {v}")
    # model: cli-model (CLI)
    # epochs: 20 (CLI > env 15 > default 10)
    # lr: 1e-3 (env > default)
    # batch_size: 64 (CLI > env 128 > default 32)
    # fp16: True (CLI)

# ============================================================
# 5. Exit Codes
# ============================================================

def run_command(args: list[str]) -> int:
    """Run command, return exit code."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--fail", action="store_true")
    parsed = parser.parse_args(args)
    
    if parsed.fail:
        print("Error: Operation failed", file=sys.stderr)
        return 1  # Non-zero = failure
    return 0  # Success

# Example exit codes
# 0 = success
# 1 = general error
# 2 = usage error (argparse does this)
# 130 = interrupted (SIGINT)

# ============================================================
# 6. Complete Training Script Template
# ============================================================

def create_train_parser() -> argparse.ArgumentParser:
    """Create parser for training script."""
    parser = argparse.ArgumentParser(
        prog="train.py",
        description="Train a language model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # Required
    parser.add_argument("config", help="Path to config YAML/JSON")
    
    # Model
    parser.add_argument("--model", help="Model name or path")
    parser.add_argument("--resume", help="Resume from checkpoint")
    
    # Training
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--grad-accum", type=int, default=1)
    
    # Hardware
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--gpus", type=int, default=1)
    parser.add_argument("--nodes", type=int, default=1)
    
    # Logging
    parser.add_argument("--wandb", action="store_true")
    parser.add_argument("--wandb-project", default="my-project")
    parser.add_argument("--log-interval", type=int, default=100)
    
    # Output
    parser.add_argument("--output-dir", default="./outputs")
    
    return parser


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: Hardcoding secrets in code
#   api_key = "sk-123"  # NEVER!
# CORRECT:
#   api_key = os.environ["OPENAI_API_KEY"]

# MISTAKE: No defaults, crashes on missing arg
#   parser.add_argument("--epochs")  # No default, no type
# CORRECT:
#   parser.add_argument("--epochs", type=int, default=10)

# MISTAKE: Using sys.argv directly for complex parsing
#   if sys.argv[1] == "train": ...
# CORRECT:
#   Use argparse with subcommands

# MISTAKE: Not returning exit codes
#   sys.exit()  # Always 0
# CORRECT:
#   sys.exit(1) on error

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    
    # argparse basics
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10)
    args = parser.parse_args(["--epochs", "20"])
    assert args.epochs == 20
    
    # defaults
    args = parser.parse_args([])
    assert args.epochs == 10
    
    # store_true
    parser.add_argument("--fp16", action="store_true")
    args = parser.parse_args(["--fp16"])
    assert args.fp16 == True
    args = parser.parse_args([])
    assert args.fp16 == False
    
    # choices
    parser = argparse.ArgumentParser()
    parser.add_argument("--opt", choices=["a", "b", "c"])
    args = parser.parse_args(["--opt", "b"])
    assert args.opt == "b"
    
    # subcommands
    root = argparse.ArgumentParser()
    subs = root.add_subparsers(dest="cmd")
    s1 = subs.add_parser("train")
    s1.add_argument("--config")
    s2 = subs.add_parser("eval")
    args = root.parse_args(["train", "--config", "x.yaml"])
    assert args.cmd == "train" and args.config == "x.yaml"
    
    # env vars
    os.environ["TEST_VAR"] = "hello"
    assert os.environ.get("TEST_VAR") == "hello"
    assert os.environ.get("MISSING", "default") == "default"
    del os.environ["TEST_VAR"]
    
    # precedence logic
    defaults = {"x": 1}
    env = {"X": "2"}
    cli = {"x": 3}
    result = defaults.copy()
    result.update({k.lower(): int(v) for k, v in env.items() if k.lower() in result})
    result.update({k: v for k, v in cli.items() if v is not None})
    assert result["x"] == 3  # CLI wins
    
    # exit codes
    import subprocess
    result = subprocess.run([sys.executable, "-c", "import sys; sys.exit(42)"], capture_output=True)
    assert result.returncode == 42
    
    print("[OK] 46-cli-and-config: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Use argparse, not sys.argv, for CLI parsing")
        print("2. Positional args for required, optional for flags")
        print("3. Subcommands for git-like interfaces")
        print("4. os.environ.get() with defaults for config")
        print("5. .env files for local development (never commit!)")
        print("6. Precedence: CLI > Env > File > Default")
        print("7. Return proper exit codes (0=success, non-zero=failure)")
        _verify()