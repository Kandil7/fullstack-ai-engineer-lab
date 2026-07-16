"""
12 - From Deep Learning Foundations to Stable Diffusion
========================================================
Goal: Understand the key components of modern text-to-image generation.
You will implement simplified versions of the core building blocks:
diffusion steps, VAE reparameterisation, CLIP-style contrastive loss,
and U-Net architecture design.

You will:
  1. Implement one DDPM reverse step.
  2. Implement the VAE reparameterisation trick.
  3. Compute a CLIP-style contrastive loss.
  4. Design a minimal U-Net and count parameters.
  5. Visualise a noise schedule.

Prerequisites:
  pip install torch numpy matplotlib    (matplotlib optional for Ex 5)

Run:
  python 12-stable-diffusion.py
"""

from __future__ import annotations

import math
from typing import Callable

import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================
# 1. DDPM Reverse Step
# ============================================================
def ddpm_step(
    x_t: torch.Tensor,
    noise_pred: torch.Tensor,
    t: int,
    alpha_bar: torch.Tensor,
    beta: torch.Tensor,
    alpha: torch.Tensor,
) -> torch.Tensor:
    """Single reverse diffusion step: x_t -> x_{t-1}.

    Args:
        x_t:         Noisy latent at timestep t. Shape (N, C, H, W).
        noise_pred:  U-Net predicted noise epsilon_theta(x_t, t).
        t:           Current timestep (integer, 0-indexed).
        alpha_bar:   Cumulative product of alpha up to each t. Shape (T,).
        beta:        Noise schedule at each t. Shape (T,).
        alpha:       1 - beta at each t. Shape (T,).

    Returns:
        x_{t-1}: Less noisy latent.
    """
    # Predicted x_0 from current x_t and noise prediction
    x_0_pred = (x_t - torch.sqrt(1 - alpha_bar[t]) * noise_pred) / torch.sqrt(alpha_bar[t])

    # Compute coefficients for mean of q(x_{t-1} | x_t, x_0)
    alpha_bar_prev = alpha_bar[t - 1] if t > 0 else torch.tensor(1.0)
    coeff1 = torch.sqrt(alpha_bar_prev) * beta[t]
    coeff2 = torch.sqrt(alpha[t]) * (1 - alpha_bar_prev)
    mean = (coeff1 * x_0_pred + coeff2 * x_t) / (1 - alpha_bar[t])

    # If t > 0, add noise (otherwise final step, deterministic)
    if t > 0:
        noise = torch.randn_like(x_t)
        std = torch.sqrt(beta[t])
        return mean + std * noise
    return mean


# ============================================================
# 2. VAE Reparameterisation
# ============================================================
class VAEEncoder(nn.Module):
    """A minimal VAE encoder showing the reparameterisation trick.

    The encoder outputs mean and log-variance, then samples a latent
    using: z = mean + exp(0.5 * log_var) * epsilon.
    This keeps the sampling step differentiable.
    """

    def __init__(self, in_dim: int = 784, latent_dim: int = 20) -> None:
        super().__init__()
        self.fc = nn.Linear(in_dim, latent_dim * 2)  # 2x: mean + log_var

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Encode input and sample from the latent distribution.

        Returns:
            z:       Sampled latent vector.
            mean:    Mean of the latent distribution.
            log_var: Log-variance of the latent distribution.
        """
        h = self.fc(x)
        mean, log_var = h.chunk(2, dim=-1)

        # Reparameterisation trick: make sampling differentiable
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        z = mean + std * eps

        return z, mean, log_var


def kl_divergence(mean: torch.Tensor, log_var: torch.Tensor) -> torch.Tensor:
    """KL divergence between N(mean, var) and N(0, 1).

    Closed form: 0.5 * sum(1 + log_var - mean^2 - exp(log_var)).
    This regularises the latent space toward a standard normal.
    """
    return -0.5 * torch.sum(1 + log_var - mean**2 - torch.exp(log_var), dim=-1).mean()


# ============================================================
# 3. CLIP-Style Contrastive Loss
# ============================================================
def contrastive_loss(
    image_embeds: torch.Tensor,
    text_embeds: torch.Tensor,
    temperature: float = 0.07,
) -> torch.Tensor:
    """Contrastive loss (InfoNCE) for a batch of N (image, text) pairs.

    Args:
        image_embeds: (N, D) L2-normalised image embeddings.
        text_embeds:  (N, D) L2-normalised text embeddings.
        temperature:  Scale factor for logits.

    Returns:
        Scalar loss.
    """
    N = image_embeds.shape[0]

    # Similarity matrix: (N, N) where [i,j] = sim(image_i, text_j)
    logits = (image_embeds @ text_embeds.T) / temperature

    # Targets: diagonal = matching pairs
    labels = torch.arange(N, device=logits.device)

    # Symmetric loss: average of image->text and text->image cross-entropy
    loss_i2t = F.cross_entropy(logits, labels)
    loss_t2i = F.cross_entropy(logits.T, labels)

    return (loss_i2t + loss_t2i) / 2.0


# ============================================================
# 4. U-Net Parameter Counter
# ============================================================
def unet_channel_sizes(
    in_channels: int = 4,
    base_channels: int = 64,
    multipliers: list[int] | None = None,
) -> list[int]:
    """Compute channel sizes for each U-Net block level.

    Example:
        in=4, base=64, multipliers=[1, 2, 4, 4]
        => [64, 128, 256, 256] for both encoder and decoder
    """
    if multipliers is None:
        multipliers = [1, 2, 4, 4]
    return [base_channels * m for m in multipliers]


def count_unet_params(
    in_channels: int = 4,
    base_channels: int = 64,
    n_blocks: int = 4,
) -> int:
    """Estimate the number of parameters in a minimal diffusion U-Net.

    Each block: 2 convs (3x3) + 2 BN + time_mlp.
    Skip connections link encoder to decoder at each level.
    """
    total = 0
    ch = unet_channel_sizes(in_channels, base_channels)

    # Initial convolution: in_channels -> ch[0]
    total += in_channels * ch[0] * 3 * 3 + ch[0]

    for i in range(n_blocks):
        c = ch[i]
        # Two 3x3 convs per ResBlock
        conv_params = 2 * (c * c * 3 * 3 + c)
        # Two BatchNorm (2 params each: gamma, beta)
        bn_params = 2 * (2 * c)
        # Time embedding MLP: c -> 2*c (for FiLM scale & shift)
        time_mlp = c * (2 * c) + (2 * c)
        total += conv_params + bn_params + time_mlp

        if i < n_blocks - 1:
            # Down/upsampling conv between levels (skip connections at each level)
            next_c = ch[i + 1]
            total += c * next_c * 3 * 3 + next_c  # down conv

    # Final convolution: ch[0] -> in_channels
    total += ch[0] * in_channels * 3 * 3 + in_channels

    return total


# ============================================================
# 5. Main Demonstration
# ============================================================
def _safe(x: str) -> str:
    """Sanitise for cp1252 terminals."""
    return x.replace("\u2192", "->").replace("\u03b2", "beta").replace("\u03b5", "eps")


def make_linear_noise_schedule(T: int = 1000, beta_start: float = 1e-4, beta_end: float = 0.02) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Create a linear noise schedule (as used in original DDPM)."""
    beta = torch.linspace(beta_start, beta_end, T)
    alpha = 1.0 - beta
    alpha_bar = torch.cumprod(alpha, dim=0)
    return beta, alpha, alpha_bar


def main() -> None:
    torch.manual_seed(42)
    T = 100
    beta, alpha, alpha_bar = make_linear_noise_schedule(T)

    print("=" * 60)
    print("1. DDPM Reverse Step")
    print("=" * 60)

    # Simulate a tiny latent: 1x4x8x8
    x_t = torch.randn(1, 4, 8, 8)
    noise_pred = torch.randn_like(x_t)  # stand-in for U-Net output
    t = T // 2

    x_prev = ddpm_step(x_t, noise_pred, t, alpha_bar, beta, alpha)
    print(f"Input shape:  {tuple(x_t.shape)}")
    print(f"Output shape: {tuple(x_prev.shape)}")
    print(f"Input mean:   {x_t.mean().item():.4f}, std: {x_t.std().item():.4f}")
    print(f"Output mean:  {x_prev.mean().item():.4f}, std: {x_prev.std().item():.4f}")
    print(f"Step reduces noise (std decreases): {x_prev.std().item() < x_t.std().item()}")
    print()

    print("=" * 60)
    print("2. VAE Reparameterisation Trick")
    print("=" * 60)

    vae = VAEEncoder(in_dim=784, latent_dim=20)
    dummy_input = torch.randn(4, 784)
    z, mean, log_var = vae(dummy_input)
    kl = kl_divergence(mean, log_var)
    print(f"Input:  (4, 784)")
    print(f"Latent: {tuple(z.shape)}")
    print(f"Mean:   {mean[0, :5].tolist()}")
    print(f"LogVar: {log_var[0, :5].tolist()}")
    print(f"KL loss: {kl.item():.4f}")
    print(f"KL loss > 0 (regularisation active): {kl.item() > 0}")
    print()

    print("=" * 60)
    print("3. Contrastive (CLIP-Style) Loss")
    print("=" * 60)

    N, D = 8, 64
    img_emb = F.normalize(torch.randn(N, D), dim=-1)
    txt_emb = F.normalize(torch.randn(N, D), dim=-1)
    loss = contrastive_loss(img_emb, txt_emb, temperature=0.07)
    print(f"Batch size: {N}, Embed dim: {D}")
    print(f"Contrastive loss: {loss.item():.4f}")

    # Perfect alignment: loss should be lower
    aligned_loss = contrastive_loss(img_emb, img_emb, temperature=0.07)
    print(f"Loss (aligned pairs): {aligned_loss.item():.4f} (should be lower)")
    print()

    print("=" * 60)
    print("4. U-Net Parameter Count")
    print("=" * 60)

    for base_ch in [32, 64, 128]:
        params = count_unet_params(in_channels=4, base_channels=base_ch)
        print(f"base_channels={base_ch:>4}: {params:>10,} parameters")
    print()

    print("=" * 60)
    print("5. Noise Schedule Analysis")
    print("=" * 60)

    beta_full, alpha_full, alpha_bar_full = make_linear_noise_schedule(T=1000)
    # Find timestep where 50% signal is destroyed
    half_idx = int(torch.searchsorted(alpha_bar_full, torch.tensor(0.5)))
    print(f"Linear schedule: beta from {beta_full[0]:.6f} to {beta_full[-1]:.6f}")
    print(f"50% signal destroyed at timestep: {half_idx}/{len(alpha_bar_full)}")
    print(f"Alpha_bar[0]:   {alpha_bar_full[0]:.4f} (near 1 = clean)")
    print(f"Alpha_bar[500]: {alpha_bar_full[500]:.4f}")
    print(f"Alpha_bar[-1]:  {alpha_bar_full[-1]:.4f} (near 0 = pure noise)")
    print()

    # EXERCISE 1: Modify ddpm_step to return both x_{t-1} AND the predicted x_0.
    # Verify that x_0_pred looks like a cleaner version of x_t.

    # EXERCISE 2: Build a full VAE (encoder + decoder) and train it on MNIST
    # for 10 epochs. Plot samples from the latent space.

    # EXERCISE 3: Increase the temperature in contrastive_loss from 0.07 to 1.0.
    # How does the loss change? What happens to the gradient?

    # EXERCISE 4: Add skip connections to the U-Net parameter count and
    # compare the total with and without them.

    # EXERCISE 5: Replace the linear noise schedule with a cosine schedule:
    #   alpha_bar[t] = cos((t/T + s) / (1 + s) * pi/2)^2
    # where s=0.008. At what timestep is 50% destroyed now?


if __name__ == "__main__":
    main()
