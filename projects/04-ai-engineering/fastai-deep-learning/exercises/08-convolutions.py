"""
fast.ai Exercise 08 - Convolutions (CNNs)
=========================================

Goal:
    Build convolutions from the ground up with pure PyTorch on the CPU:
    apply a hand-made edge-detection kernel to a small tensor, verify the
    output-size formula, then assemble a tiny CNN on MNIST-shaped random
    data and run one forward pass.

Topics covered:
    - Applying a kernel with F.conv2d and reading the feature map
    - Stride / padding and the formula out = (n + 2p - k)/s + 1
    - Channels: mapping C_in -> C_out with nn.Conv2d
    - A small CNN (Conv -> BatchNorm -> ReLU) with adaptive pooling + head

Prerequisites:
    pip install torch      # CPU build is fine; no GPU required

Run:
    python 08-convolutions.py
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


# =============================================================================
# Exercise 1: Apply a hand-made vertical edge-detection kernel
# =============================================================================
# A vertical-edge kernel has a negative left column and a positive right
# column. On a flat patch the response is ~0; on a light/dark boundary it
# lights up.
#
# EXERCISE: build the (1, 1, 3, 3) vertical-edge kernel and convolve `image`.
#   Kernel rows: [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]
#   Use F.conv2d with default stride/padding ('valid').
# =============================================================================
def detect_vertical_edges(image: torch.Tensor) -> torch.Tensor:
    """Return the feature map from a vertical edge kernel over `image`."""
    # image arrives shaped (1, 1, H, W)
    kernel = torch.tensor(
        [[-1.0, 0.0, 1.0],
         [-2.0, 0.0, 2.0],
         [-1.0, 0.0, 1.0]]
    ).reshape(1, 1, 3, 3)
    return F.conv2d(image, kernel)


# =============================================================================
# Exercise 2: Output-size formula
# =============================================================================
# out = (n + 2p - k) / s + 1  (integer floor division)
#
# EXERCISE: implement the formula. It should return an int.
# =============================================================================
def conv_output_size(n: int, k: int, stride: int, padding: int) -> int:
    """Compute the output spatial size of a conv/pool layer."""
    return (n + 2 * padding - k) // stride + 1


# =============================================================================
# Exercise 3: A single conv layer maps C_in -> C_out
# =============================================================================
# EXERCISE: create an nn.Conv2d with `in_ch` input channels, `out_ch` filters,
# a 3x3 kernel and padding=1 ('same' for stride 1), then apply it to `x`.
# =============================================================================
def apply_conv_layer(
    x: torch.Tensor, in_ch: int, out_ch: int
) -> torch.Tensor:
    """Run x (N, in_ch, H, W) through a same-size 3x3 conv layer."""
    conv = nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1)
    return conv(x)


# =============================================================================
# Exercise 4: Build a tiny CNN for MNIST-shaped data
# =============================================================================
# Grow channels while shrinking spatial size via stride-2 convs, then collapse
# with adaptive pooling and classify with a linear head.
#
# EXERCISE: complete the Sequential model so a (N, 1, 28, 28) input yields
# (N, 10) logits. Use the conv_block helper for each downsampling stage.
# =============================================================================
def conv_block(in_ch: int, out_ch: int) -> nn.Sequential:
    """Conv (stride-2 downsample) -> BatchNorm -> ReLU."""
    return nn.Sequential(
        nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True),
    )


def build_tiny_cnn(n_classes: int = 10) -> nn.Sequential:
    """A small CNN: 28 -> 14 -> 7 -> 4 -> 1, then a linear head."""
    return nn.Sequential(
        conv_block(1, 16),          # 28 -> 14
        conv_block(16, 32),         # 14 -> 7
        conv_block(32, 64),         # 7  -> 4
        nn.AdaptiveAvgPool2d(1),    # 4  -> 1 (any size -> 1x1)
        nn.Flatten(),               # (N, 64, 1, 1) -> (N, 64)
        nn.Linear(64, n_classes),   # classification head
    )


# =============================================================================
# Demonstration / self-check
# =============================================================================
def main() -> None:
    torch.manual_seed(0)

    # --- Exercise 1: edge detection ------------------------------------------
    print("=" * 60)
    print("Exercise 1: vertical edge detection")
    image = torch.tensor(
        [[0.0, 0.0, 10.0, 10.0, 10.0],
         [0.0, 0.0, 10.0, 10.0, 10.0],
         [0.0, 0.0, 10.0, 10.0, 10.0],
         [0.0, 0.0, 10.0, 10.0, 10.0],
         [0.0, 0.0, 10.0, 10.0, 10.0]]
    ).reshape(1, 1, 5, 5)
    feature_map = detect_vertical_edges(image)
    print("feature map:\n", feature_map[0, 0])
    # The boundary column should show a strong response; flat regions ~0.
    assert feature_map.shape == (1, 1, 3, 3)
    assert feature_map[0, 0, 0, 0].item() == 40.0

    # --- Exercise 2: output-size formula -------------------------------------
    print("=" * 60)
    print("Exercise 2: output-size formula")
    print("n=5,k=3,s=1,p=0 ->", conv_output_size(5, 3, 1, 0))    # 3
    print("n=5,k=3,s=1,p=1 ->", conv_output_size(5, 3, 1, 1))    # 5 (same)
    print("n=28,k=3,s=2,p=1 ->", conv_output_size(28, 3, 2, 1))  # 14
    assert conv_output_size(5, 3, 1, 0) == 3
    assert conv_output_size(5, 3, 1, 1) == 5
    assert conv_output_size(28, 3, 2, 1) == 14

    # --- Exercise 3: channels ------------------------------------------------
    print("=" * 60)
    print("Exercise 3: C_in -> C_out")
    x = torch.randn(4, 3, 16, 16)          # 4 RGB images
    out = apply_conv_layer(x, in_ch=3, out_ch=8)
    print("input :", tuple(x.shape))
    print("output:", tuple(out.shape))     # (4, 8, 16, 16), same H/W
    assert out.shape == (4, 8, 16, 16)

    # --- Exercise 4: tiny CNN ------------------------------------------------
    print("=" * 60)
    print("Exercise 4: tiny CNN forward pass")
    model = build_tiny_cnn(n_classes=10)
    batch = torch.randn(8, 1, 28, 28)      # fake MNIST batch
    logits = model(batch)
    n_params = sum(p.numel() for p in model.parameters())
    print("logits:", tuple(logits.shape))  # (8, 10)
    print("params:", n_params)
    assert logits.shape == (8, 10)

    print("=" * 60)
    print("All checks passed.")


if __name__ == "__main__":
    main()
