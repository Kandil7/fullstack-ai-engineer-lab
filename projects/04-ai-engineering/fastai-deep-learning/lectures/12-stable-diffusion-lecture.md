# Lecture 12: From Deep Learning Foundations to Stable Diffusion

## Topic Overview

Fast.ai's **Part 2** — released in 2022–2023 with over 30 hours of video — is the sequel to Practical Deep Learning for Coders. Where Part 1 taught you to *use* deep learning, Part 2 teaches you to *build it from the ground up*. You will construct your own training framework (called `miniai`) entirely in Jupyter notebooks, implement every component of the modern generative AI stack, and end with a fully functional **Stable Diffusion** pipeline.

This lecture condenses the arc of Part 2 into a single module: from tensors and matrix multiplication in pure Python, through ResNets and U-Nets, through autoencoders and CLIP, to the full diffusion process that powers DALL-E, Midjourney, and Stable Diffusion. By the end you will understand what happens inside a "text-to-image" model at every level of the stack.

**Duration:** 4–6 hours (read + exercises)  
**Difficulty:** Advanced  
**Prerequisites:** Modules 01–08 (especially 03: SGD, 05: From-Scratch, 08: Convolutions)

---

## Learning Objectives

By the end of this lecture you will be able to:

1. **Explain** the Part 2 philosophy — building everything from scratch (the "miniai" framework) rather than treating libraries as black boxes.
2. **Implement** matrix multiplication, tensors, and a minimal autograd system from scratch using Python and Numba.
3. **Trace** the architecture of a ResNet and a U-Net, and explain why each is suited to its task.
4. **Describe** how autoencoders learn latent representations and how the VAE's reparameterisation trick enables sampling.
5. **Explain** contrastive learning and how CLIP embeds images and text into a shared latent space.
6. **Walk through** the DDPM (Denoising Diffusion Probabilistic Model) forward and reverse processes.
7. **Differentiate** sampling methods: DDIM, Euler, ancestral Euler, Heun, LMS.
8. **Assemble** the full Stable Diffusion pipeline: VAE → U-Net → CLIP → Sampler.
9. **Discuss** advanced techniques: Textual Inversion, DreamBooth, and Karras et al. pre-conditioning.
10. **Connect** the generative AI stack to the ethical considerations from Module 09.

---

## Key Concepts

### 1. The Part 2 Philosophy: Build from Scratch

Part 1 taught you the fast.ai high-level API: `DataLoaders → Learner → fine_tune`. Part 2 tears off the covers and builds everything yourself.

The course introduces **miniai** — a small, didactic deep learning framework written entirely in Jupyter notebooks using Python, PyTorch, and Numba. Unlike PyTorch or TensorFlow (which are production frameworks with millions of lines of code), miniai is designed to be *readable and modifiable by one person*. Every line is there for a pedagogical reason.

```text
Part 1 (Modules 01-08):      Part 2 (Module 12):
┌─────────────────────┐      ┌─────────────────────┐
│ vision_learner()    │      │ Your own Learner()  │
│ fine_tune()         │      │ Your own fit()      │
│ DataLoaders         │      │ Your own DataLoader │
│ ResNet (pretrained) │      │ Your own ResNet     │
│ fastai library      │      │ "miniai" framework  │
└─────────────────────┘      └─────────────────────┘
  User-ready                  Built from scratch
```

### 2. Tensors and Matrix Multiplication from Scratch

Before using PyTorch's `torch.mm`, Part 2 implements matrix multiplication in pure Python — then accelerates it with Numba's `@njit` decorator.

```python
from numba import njit
import numpy as np

@njit
def matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Matrix multiply: C[i,j] = sum_k A[i,k] * B[k,j]"""
    m, k1 = A.shape
    k2, n = B.shape
    assert k1 == k2
    C = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            s = 0.0
            for k in range(k1):
                s += A[i, k] * B[k, j]
            C[i, j] = s
    return C
```

The key insight: once you have fast matrix multiplication and an automatic differentiation system (built from the ground up by implementing the chain rule manually for each operation), you have everything you need to train a neural network.

### 3. ResNets: Skip Connections Enable Depth

You met ResNets in Lecture 01 (transfer learning) and Lecture 08 (the ResBlock). Part 2 builds them from scratch, layer by layer, showing that a plain deep net gets *harder* to train as you add layers — but adding skip connections (the identity path) makes deep nets trainable by allowing gradients to flow directly through the network.

```python
import torch.nn as nn

class ResBlock(nn.Module):
    """out = ReLU(x + F(x)). Only needs to learn the residual (change)."""
    def __init__(self, ch: int):
        super().__init__()
        self.conv1 = nn.Conv2d(ch, ch, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(ch)
        self.conv2 = nn.Conv2d(ch, ch, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(ch)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out = out + identity  # The skip connection
        return self.relu(out)
```

This is the architectural innovation that made ResNet-18/34/50/101/152 possible and that powers virtually every modern vision model.

### 4. U-Nets: Encoder-Decoder for Image Generation

A U-Net is a symmetric architecture: an encoder that downsamples (compressing the image to a latent representation) and a decoder that upsamples back to the original resolution, with **skip connections** between corresponding encoder and decoder layers.

```text
    Input image (H, W)
         │
    ┌────┴────┐
    │ Encoder │  Conv + downsampling (H/2, W/2) → (H/4, W/4) → ...
    └────┬────┘
         │      ═══ skip connections ═══
    ┌────┴────┐
    │ Decoder │  Upsampling + Conv (H/4, W/4) → (H/2, W/2) → (H, W)
    └────┬────┘
         │
    Output image (H, W)
```

The skip connections preserve high-frequency details that would otherwise be lost during downsampling — critical for tasks like image segmentation and image generation where spatial fidelity matters.

**In Stable Diffusion, the U-Net operates in the latent space (not pixel space),** denoising a latent representation over many timesteps. This is the key insight that makes diffusion practical: working in a compressed latent space reduces the computational cost by an order of magnitude.

### 5. Autoencoders and Variational Autoencoders (VAEs)

An **autoencoder** learns to compress an input into a lower-dimensional latent representation and then reconstruct it. The VAE adds a probabilistic twist: instead of encoding to a single point, it encodes to a distribution (mean and variance), then samples from that distribution using the **reparameterisation trick**.

```python
import torch
import torch.nn as nn

class VAEEncoder(nn.Module):
    """Encode input to mean + log_var, then sample via reparameterisation."""

    def __init__(self, in_dim: int, latent_dim: int):
        super().__init__()
        self.fc = nn.Linear(in_dim, latent_dim * 2)  # 2x: mean + log_var

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        h = self.fc(x)
        mean, log_var = h.chunk(2, dim=-1)
        # Reparameterisation trick: z = mean + std * epsilon
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        z = mean + std * eps
        return z, mean, log_var
```

**Why the reparameterisation trick?** Without it, the sampling step is non-differentiable, so you cannot backpropagate through it. By expressing the sample as `mean + std * epsilon` (where epsilon is a standard normal sample), the randomness is isolated in epsilon, and gradients flow through the deterministic mean and std paths.

In Stable Diffusion, the VAE compresses a 512×512×3 image (786,432 values) into a 64×64×4 latent (16,384 values) — a 48× compression ratio. This makes diffusion feasible on consumer GPUs.

### 6. CLIP: Contrastive Language-Image Pre-training

CLIP (Contrastive Language-Image Pre-training, OpenAI 2021) is the secret sauce that makes text-to-image generation work. It learns a **shared embedding space** where images and their captions are close together.

```text
         ┌──────────┐     ┌────────────────┐
  Text   │ Text Enc │────▶│   Shared       │
  ──────▶│ (Transf.)│     │   Embedding    │
         └──────────┘     │   Space        │
                         │   (512-dim)    │
         ┌──────────┐     │                │
  Image  │ ImageEnc │────▶│                │
  ──────▶│ (ViT)   │     └────────────────┘
         └──────────┘

Training objective: maximize cosine similarity for matching (image, caption) pairs,
                    minimize it for non-matching pairs (contrastive loss).
```

CLIP is trained on 400 million (image, text) pairs from the internet. After training, the text encoder can guide image generation: the diffusion U-Net attends to CLIP text embeddings to determine what to generate.

In Stable Diffusion, there are **two** levels of text conditioning:
- **Cross-attention** in the U-Net: CLIP text embeddings attend to U-Net feature maps.
- **Classifier-free guidance** (CFG): mixing conditional and unconditional predictions to amplify the effect of the text prompt.

### 7. Diffusion Models (DDPM)

**Denoising Diffusion Probabilistic Models** (Ho et al., 2020) are the foundation. The idea is simple and beautiful:

**Forward process (fixed):** Gradually add Gaussian noise to an image over T timesteps until it becomes pure noise.

**Reverse process (learned):** Train a neural network to predict the noise added at each step, starting from pure noise and stepping backward to recover a clean image.

```text
Forward:  x₀ → x₁ → x₂ → ... → x_T  (add noise, q is known)
           │     │     │           │
           ▼     ▼     ▼           ▼
         noise  more noise        pure noise

Reverse:  x_T → x_{T-1} → ... → x₁ → x₀  (remove noise, p_θ is learned)
           ▲        ▲              ▲     ▲
           │        │              │     │
         U-Net predicts ε_θ(x_t, t) at each step
```

**Key equations (DDPM):**

```text
Forward:  q(x_t | x_{t-1}) = N(x_t; sqrt(1-β_t) * x_{t-1}, β_t * I)
          q(x_t | x_0)      = N(x_t; sqrt(ᾱ_t) * x_0, (1-ᾱ_t) * I)

Reverse:  p_θ(x_{t-1} | x_t) = N(x_{t-1}; μ_θ(x_t, t), σ_t² * I)
          μ_θ(x_t, t) = (1 / sqrt(α_t)) * (x_t - (β_t / sqrt(1-ᾱ_t)) * ε_θ(x_t, t))

Training: minimize L = E_{t, x_0, ε} [ || ε - ε_θ(x_t, t) ||² ]
          where ε ~ N(0, I), and x_t = sqrt(ᾱ_t) * x_0 + sqrt(1-ᾱ_t) * ε
```

In plain English: the training objective is simply to predict the noise that was added. The model is a time-conditioned U-Net that takes a noisy image and a timestep and outputs the predicted noise.

### 8. Sampling Methods

DDPM sampling is slow — it requires 1000 sequential steps. Faster samplers have been developed:

| Sampler | Steps | Quality | Speed |
|---------|-------|---------|-------|
| **DDPM** (Ho et al., 2020) | 1000 | Highest | Slowest |
| **DDIM** (Song et al., 2021) | 50-100 | Very high | 10-20× faster |
| **Euler** (Karras et al., 2022) | 30-50 | High | Very fast |
| **Ancestral Euler** | 30-50 | High | Very fast |
| **Heun (2nd order)** | 20-30 | Higher | Fast |
| **LMS** | 20-50 | High | Fast |

**DDIM** (Denoising Diffusion Implicit Models) is a critical innovation: it makes the reverse process **deterministic** given the initial noise, which means you can take larger steps (fewer total steps) and also **interpolate** between two noise vectors for smooth transitions.

**Karras et al. (2022)** — *Elucidating the Design Space of Diffusion-Based Generative Models* — reformulated the diffusion process with:
- **Pre-conditioning:** Scaling the network inputs/outputs so the model always sees unit-variance data.
- **Better noise schedules:** A shifted log-normal distribution for training timesteps.
- **Higher-order samplers:** Heun's 2nd-order method for fewer steps.

### 9. The Full Stable Diffusion Pipeline

Stable Diffusion (Rombach et al., 2022) combines all the above into a pipeline:

```text
Text Prompt: "a cat wearing a hat"
      │
      ▼
┌─────────────┐      ┌──────────────┐
│ CLIP Text   │─────▶│ Tokenizer +  │
│ Encoder     │      │ Embeddings   │
└─────────────┘      └──────┬───────┘
                            │
┌──────────────┐           │
│ Random Noise │─▶ U-Net ◀─┘ (cross-attention to CLIP embeddings)
│ (latent)     │    │  conditioned on timestep t
└──────────────┘    │
                    ▼
           ┌────────────────┐
           │ Sampler (DDIM) │  (repeated for each timestep)
           └────────┬───────┘
                    │ denoised latent (64×64×4)
                    ▼
           ┌────────────────┐
           │ VAE Decoder    │  (decodes latent to pixel space)
           └────────┬───────┘
                    │ 512×512×3 image
                    ▼
           "a cat wearing a hat" 🐱🎩
```

**Step by step:**

1. **Encode prompt:** CLIP text encoder converts the prompt into 77 token embeddings.
2. **Generate noise:** Sample random noise in the latent space (64×64×4).
3. **Denoise loop:** For t = T down to 1:
   - U-Net predicts the noise at step t, conditioned on the CLIP embeddings.
   - Sampler produces a less noisy latent: x_{t-1} from x_t.
4. **Decode:** VAE decoder converts the final 64×64×4 latent into a 512×512×3 image.

### 10. Advanced Techniques

**Textual Inversion** (Gal et al., 2022): Learn a new "word" (a new embedding vector) that represents a concept from a few example images. The model weights are frozen; only the embedding is trained.

**DreamBooth** (Ruiz et al., 2023): Fine-tune the entire diffusion model on a few images of a subject (e.g., your dog) with a rare token identifier, plus a prior-preservation loss to prevent overfitting.

**LoRA** (Low-Rank Adaptation): Instead of fine-tuning all weights, train low-rank matrices that are added to the existing weight matrices. Much smaller file size, composable with other LoRAs.

**CFG (Classifier-Free Guidance):** At inference time, compute both a conditional prediction (with prompt) and an unconditional prediction (with empty prompt), then extrapolate: `ε = ε_cond + cfg_scale * (ε_cond - ε_uncond)`. Higher `cfg_scale` means stronger prompt adherence but potentially lower image quality.

---

## Code Examples

### Example 1: A Minimal Diffusion Step

```python
"""Demonstrate one step of the DDPM reverse process."""

from __future__ import annotations

import torch
import torch.nn.functional as F


def ddpm_step(
    x_t: torch.Tensor,
    noise_pred: torch.Tensor,
    t: torch.Tensor,
    alpha_bar: torch.Tensor,
    beta: torch.Tensor,
    alpha: torch.Tensor,
) -> torch.Tensor:
    """Single reverse diffusion step: x_t -> x_{t-1}.

    Args:
        x_t: Noisy latent at timestep t.
        noise_pred: U-Net predicted noise epsilon_theta(x_t, t).
        t: Current timestep (0-indexed, scalar tensor).
        alpha_bar: Cumulative product of (1 - beta) up to t.
        beta: Noise schedule at timestep t.
        alpha: 1 - beta at timestep t.
    """
    # Predicted x_0 from current x_t and noise prediction
    x_0_pred = (x_t - torch.sqrt(1 - alpha_bar[t]) * noise_pred) / torch.sqrt(alpha_bar[t])

    # Compute mean of q(x_{t-1} | x_t, x_0)
    coeff1 = torch.sqrt(alpha_bar[t - 1] if t > 0 else torch.tensor(1.0)) * beta[t]
    coeff2 = torch.sqrt(alpha[t]) * (1 - alpha_bar[t - 1] if t > 0 else torch.tensor(0.0))
    mean = (coeff1 * x_0_pred + coeff2 * x_t) / (1 - alpha_bar[t])

    # If t > 0, add noise (otherwise final step, no noise)
    if t > 0:
        noise = torch.randn_like(x_t)
        std = torch.sqrt(beta[t])
        return mean + std * noise
    return mean
```

### Example 2: A Minimal Time-Conditioned U-Net Block

```python
"""A minimal time-conditioned residual block for diffusion U-Nets."""

import torch
import torch.nn as nn


class SinusoidalTimeEmbedding(nn.Module):
    """Positional embedding for timesteps (similar to Transformer PE)."""

    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        half = self.dim // 2
        freqs = torch.exp(-torch.arange(half, dtype=torch.float32) * torch.log(torch.tensor(10000.0)) / half)
        args = t[:, None].float() * freqs[None, :].to(t.device)
        return torch.cat([torch.sin(args), torch.cos(args)], dim=-1)


class TimeConditionedResBlock(nn.Module):
    """ResBlock that adds time embedding via scale & shift (FiLM)."""

    def __init__(self, channels: int, time_dim: int):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.norm1 = nn.BatchNorm2d(channels)
        self.norm2 = nn.BatchNorm2d(channels)
        self.time_mlp = nn.Linear(time_dim, channels * 2)  # scale & shift

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor) -> torch.Tensor:
        scale_shift = self.time_mlp(t_emb).unsqueeze(-1).unsqueeze(-1)
        scale, shift = scale_shift.chunk(2, dim=1)

        identity = x
        out = self.norm1(x)
        out = out * (1 + scale) + shift  # FiLM modulation
        out = F.relu(out)
        out = self.conv1(out)

        out = self.norm2(out)
        out = out * (1 + scale) + shift
        out = F.relu(out)
        out = self.conv2(out)

        return out + identity
```

### Example 3: Contrastive Loss (CLIP-Style)

```python
"""Contrastive loss used to train CLIP: maximize agreement for matching pairs."""

import torch
import torch.nn.functional as F


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

    # Similarity matrix: (N, N) where [i,j] = similarity of image i to text j
    logits = (image_embeds @ text_embeds.T) / temperature

    # Targets: diagonal = matching pairs
    labels = torch.arange(N, device=logits.device)

    # Symmetric loss: average of image->text and text->image cross-entropy
    loss_i2t = F.cross_entropy(logits, labels)
    loss_t2i = F.cross_entropy(logits.T, labels)

    return (loss_i2t + loss_t2i) / 2.0
```

---

## Common Mistakes to Avoid

**Mistake 1 — Confusing the VAE latent space with the diffusion space.**

In Stable Diffusion, the VAE compresses *pixels to latents* (once) and the diffusion process operates *entirely in latent space*. The U-Net never sees pixels — it sees 64×64×4 latents. The VAE decoder only runs once at the end.

**Mistake 2 — Not time-conditioning the U-Net.**

A diffusion U-Net must know *which timestep* it is at, because the amount of noise to predict depends on t. The sinusoidal time embedding is passed into each ResBlock — without it, the model cannot tell whether it should remove a little noise (late timestep) or a lot (early timestep).

**Mistake 3 — Using the training noise schedule for sampling.**

DDPM training uses a linear (or cosine) noise schedule over 1000 steps. Sampling can use a *different* schedule (e.g., fewer steps with DDIM) without retraining. The model generalises because it was trained on all noise levels.

**Mistake 4 — Setting CFG scale too high.**

```text
cfg_scale=1.0:  unconditional only = ignores prompt
cfg_scale=7.5:  good default for Stable Diffusion
cfg_scale=15+:  oversaturated, artificial-looking, reduced diversity
```

---

## Best Practices

1. **Build from scratch first** — implement a 1D diffusion on a toy dataset (e.g., swiss roll) before tackling image diffusion.
2. **Use the latent space** — operating on 64×64×4 latents instead of 512×512×3 pixels is what makes diffusion practical.
3. **Start with DDPM, then switch to DDIM** — understand the full-step process before optimising with accelerated samplers.
4. **Normalise the U-Net input** — Karras pre-conditioning ensures the model always sees unit-variance data.
5. **Use mixed precision** — diffusion training is compute-heavy; `torch.cuda.amp` or `accelerate` are essential.
6. **Log samples during training** — diffusion models look like noise for most of training; only the last few hundred steps show structure, so sample frequently.
7. **Separate conditioning from architecture** — the U-Net architecture is general; what changes is how conditioning (CLIP embeddings, timestep) is injected.
8. **Start with a pretrained VAE** — training a VAE from scratch is hard; use a Stable Diffusion VAE or a known checkpoint.
9. **Use `torch.compile`** — for production diffusion, `torch.compile` gives significant speedups on the U-Net forward pass.
10. **Mind the hardware** — Stable Diffusion training requires 8+ GB VRAM; inference can run on 4 GB with memory-efficient attention.

---

## Practice Exercises

### Exercise 1: One-Step DDPM
Implement the `ddpm_step` function from Example 1 and run it for T=5 steps on a random 4×4 "image" tensor. Verify the output changes at each step.

### Exercise 2: U-Net Channel Sizes
Design a minimal U-Net that takes a 64×64×4 latent and outputs a 64×64×4 noise prediction. Use 3 down/up blocks with channel multipliers [1, 2, 4, 4] and skip connections. Count the total parameters.

### Exercise 3: Noise Schedule Visualisation
Plot the `alpha_bar[t]` curve for a linear noise schedule (`beta` from 0.0001 to 0.02 over T=1000 steps). At what timestep is 50% of the signal destroyed?

### Exercise 4: CFG Comparison
Given a conditional noise prediction and an unconditional noise prediction, compute the CFG-adjusted prediction for cfg_scale values of 1.0, 3.0, 7.5, and 15.0. How does the result change?

### Exercise 5: CLIP Embedding Dimensionality
Take a small batch of text prompts (e.g., "a cat", "a dog", "a cat wearing a hat"), compute their CLIP embeddings using `transformers`, and compute the cosine similarity matrix. Which prompt pairs are closest in the embedding space?

---

## Summary

1. **Part 2 builds everything from scratch** — tensors, autograd, optimisers, data loaders, and architectures — in the `miniai` framework.
2. **ResNets** use skip connections to train very deep networks; **U-Nets** use skip connections to preserve spatial detail across an encoder-decoder.
3. **Autoencoders/VAEs** compress images into a latent space; the VAE's reparameterisation trick makes sampling differentiable.
4. **CLIP** learns a shared image-text embedding space via contrastive learning on 400M pairs — this is what enables text-to-image generation.
5. **Diffusion models (DDPM)** gradually add noise to data, then learn to reverse the process by predicting the noise at each timestep.
6. **Faster samplers** (DDIM, Euler, Heun) reduce 1000 steps to 20-50 steps by making the process deterministic or using higher-order integration.
7. **Stable Diffusion** combines a VAE (for compression), a U-Net (for denoising), CLIP (for text conditioning), and a sampler into a complete text-to-image pipeline.
8. **Advanced techniques** — Textual Inversion, DreamBooth, LoRA, CFG — build on the same foundation to enable personalisation and controlled generation.

**Next:** The fast.ai Part 2 course continues with deeper dives into each component. In this lab, carry these foundations forward into the applied tracks: RAG systems (where CLIP-like embeddings power retrieval), agents (where generative models create content), and your capstone projects.

---

## References

- Ho, J., Jain, A., & Abbeel, P. (2020). "Denoising Diffusion Probabilistic Models." *NeurIPS.*
- Song, J., Meng, C., & Ermon, S. (2021). "Denoising Diffusion Implicit Models." *ICLR.*
- Rombach, R., Blattmann, A., et al. (2022). "High-Resolution Image Synthesis with Latent Diffusion Models." *CVPR.*
- Radford, A., Kim, J. W., et al. (2021). "Learning Transferable Visual Models From Natural Language Supervision." *ICML.* (CLIP)
- Karras, T., Aittala, M., et al. (2022). "Elucidating the Design Space of Diffusion-Based Generative Models." *NeurIPS.*
- Kingma, D. P. & Welling, M. (2014). "Auto-Encoding Variational Bayes." *ICLR.* (VAE)
- fast.ai. "From Deep Learning Foundations to Stable Diffusion" (2022–2023). [course.fast.ai](https://course.fast.ai/Lessons/part2.html)
