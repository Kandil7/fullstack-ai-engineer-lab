"""
Challenge 42: pathlib — Reference Solution
==========================================
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

    Why this approach: uses / operator for cross-platform compatibility,
    f-string for formatting, returns Path for further manipulation.
    """
    filename = f"epoch_{epoch:04d}_{metric_name}_{metric_value:.4f}.pt"
    return base_dir / model_name / filename


def find_latest_checkpoint(checkpoint_dir: Path) -> Path | None:
    """Return most recently modified .pt file, or None if none exist.

    Uses max() with key=stat().st_mtime for O(n) single pass.
    Handles missing directory and permission errors gracefully.
    """
    if not checkpoint_dir.exists() or not checkpoint_dir.is_dir():
        return None

    try:
        checkpoints = list(checkpoint_dir.glob("*.pt"))
    except (PermissionError, OSError):
        return None

    if not checkpoints:
        return None

    return max(checkpoints, key=lambda p: p.stat().st_mtime)


def dataset_stats(root: Path) -> dict[str, int]:
    """Return {class_name: image_count} for root/class/*.{jpg,jpeg,png}.

    Streams results using iterdir() + rglob() per class — never materializes
    full file list. Memory stays O(1) per class regardless of total images.
    """
    if not root.exists() or not root.is_dir():
        return {}

    stats: dict[str, int] = {}
    image_extensions = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

    for class_dir in root.iterdir():
        if not class_dir.is_dir():
            continue

        count = 0
        for img_path in class_dir.rglob("*"):
            if img_path.is_file() and img_path.suffix.lower() in image_extensions:
                count += 1

        if count > 0:
            stats[class_dir.name] = count

    return stats