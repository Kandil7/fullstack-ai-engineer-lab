"""
Challenge 42: pathlib — Starter Code
=====================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations
from pathlib import Path


def checkpoint_path(
    base_dir: Path,
    model_name: str,
    epoch: int,
    metric_name: str,
    metric_value: float,
) -> Path:
    """Construct standardized checkpoint path.

    Format: {base_dir}/{model_name}/epoch_{epoch:04d}_{metric_name}_{metric_value:.4f}.pt
    """
    raise NotImplementedError


def find_latest_checkpoint(checkpoint_dir: Path) -> Path | None:
    """Return most recently modified .pt file, or None if none exist."""
    raise NotImplementedError


def dataset_stats(root: Path) -> dict[str, int]:
    """Return {class_name: image_count} for root/class/*.{jpg,jpeg,png}.

    Must stream — do not materialize full file list.
    """
    raise NotImplementedError