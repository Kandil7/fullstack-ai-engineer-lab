# Glossary: From Deep Learning Foundations to Stable Diffusion

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| miniai | Fast.ai Part 2's didactic deep learning framework built from scratch in notebooks | Designed to be read, not productionised |
| Autograd | Automatic differentiation system built by tracing operations through a computation graph | Enables gradient descent without manual derivatives |
| Reparameterisation Trick | Expressing a VAE sample as `mean + std * epsilon` to keep it differentiable | Makes backpropagation through stochastic nodes possible |
| VAE (Variational Autoencoder) | Encodes inputs to a distribution (mean + variance) then samples for reconstruction | Learns a smooth, continuous latent space |
| Latent Space | Compressed representation of data; in Stable Diffusion: 64×64×4 for a 512×512×3 image | 48× compression makes diffusion practical |
| U-Net | Symmetric encoder-decoder with skip connections between corresponding layers | Preserves spatial detail through down/upsampling |
| Diffusion Model | Gradually adds noise to data (forward) then learns to remove it (reverse) | The foundation of modern image generation |
| DDPM | Denoising Diffusion Probabilistic Model — the original diffusion formulation | 1000-step Markov chain forward/backward |
| DDIM | Denoising Diffusion Implicit Models — deterministic reverse process | 20-50 steps instead of 1000 |
| CLIP | Contrastive Language-Image Pre-training — shared embedding space for images and text | The bridge between language and vision |
| Contrastive Learning | Learning by pulling matching pairs together and pushing non-matching apart | InfoNCE loss maximises mutual information |
| Cross-Attention | Attention from U-Net features to CLIP text embeddings | How the prompt guides image generation |
| Classifier-Free Guidance (CFG) | Extrapolating between conditional and unconditional predictions | Controls prompt adherence strength |
| Textual Inversion | Learning a new embedding vector for a concept from a few images | Personalisation without model fine-tuning |
| DreamBooth | Fine-tuning the full diffusion model on a subject with prior-preservation loss | High-fidelity personalisation |
| LoRA | Low-Rank Adaptation — training small additive matrices instead of full weights | Tiny file sizes, composable |
| Noise Schedule | How noise variance β_t changes over timesteps (linear, cosine, etc.) | Determines training dynamics |
| Karras Pre-conditioning | Scaling network inputs/outputs so the model sees unit-variance data | More stable training, better samples |
| Euler Sampler | First-order ODE solver applied to the diffusion reverse process | Fast, simple sampling |
| Heun Sampler | Second-order ODE solver (improved Euler) | Better quality than Euler at same step count |

---

## Detailed Definitions

### miniai

**Definition:** The pedagogical deep learning framework built entirely in Jupyter notebooks during fast.ai Part 2. Unlike PyTorch or TensorFlow (production frameworks), miniai is designed to be readable and modifiable by one person, teaching every component from tensors and autograd to optimisers and data loaders.

**Related Terms:** autograd, ResNet, U-Net

- Intentionally small: fits in a few notebooks, not millions of lines.
- Uses PyTorch as a backend but reimplements the training loop.
- Demonstrates that you can build a deep learning framework yourself.

---

### Autograd

**Definition:** Automatic differentiation — the system that computes gradients by tracing operations through a computation graph and applying the chain rule backward. Built from scratch in miniai to demystify backpropagation.

**Related Terms:** miniai, reparameterisation trick

- Every tensor operation records its inputs in a graph.
- Backward pass applies the chain rule: `dL/dx = dL/dy * dy/dx`.
- This is how PyTorch's `loss.backward()` works under the hood.

---

### Reparameterisation Trick

**Definition:** A technique that makes stochastic sampling differentiable. Instead of sampling `z ~ N(μ, σ²)` directly (non-differentiable), express it as `z = μ + σ * ε` where `ε ~ N(0, I)`. The randomness is in ε (which doesn't need gradients), while μ and σ (which do) are deterministic.

**Related Terms:** VAE, autograd

- Essential for training VAEs with backpropagation.
- The gradient flows through μ and σ, bypassing the stochastic node.
- Also used in diffusion model sampling.

---

### VAE (Variational Autoencoder)

**Definition:** A generative model that encodes inputs to a probability distribution (parameterised by mean and log-variance) rather than a single point. The decoder samples from this distribution to reconstruct the input. The Kullback-Leibler (KL) divergence regularises the latent space toward a standard normal.

**Related Terms:** reparameterisation trick, latent space, autoencoder

- Loss = reconstruction loss + KL divergence.
- The smooth latent space enables interpolation between samples.
- Stable Diffusion uses a VAE for the initial pixel→latent compression.

---

### Latent Space

**Definition:** A compressed, lower-dimensional representation of data learned by an autoencoder or VAE. In Stable Diffusion, the latent space is 64×64×4 (16,384 values), compared to 512×512×3 pixels (786,432 values) — a 48× compression.

**Related Terms:** VAE, U-Net, diffusion model

- The diffusion process operates entirely in latent space.
- The VAE encoder compresses; the VAE decoder decompresses.
- Latent diffusion makes generative models feasible on consumer GPUs.

---

### U-Net

**Definition:** A symmetric encoder-decoder architecture. The encoder progressively downsamples (reducing spatial size, increasing channels). The decoder progressively upsamples back to the original resolution. **Skip connections** link each encoder layer to its corresponding decoder layer, preserving high-frequency spatial detail.

**Related Terms:** ResNet, diffusion model, cross-attention

- In Stable Diffusion, the U-Net predicts noise at each timestep.
- Cross-attention layers in the U-Net inject CLIP text embeddings.
- The skip connections are what make U-Nets excel at dense prediction tasks.

---

### Diffusion Model

**Definition:** A generative model with two processes: a **forward process** that gradually adds Gaussian noise to data over T timesteps, and a **reverse process** that learns to remove the noise step by step. The model (typically a U-Net) is trained to predict the noise added at each timestep.

**Related Terms:** DDPM, DDIM, noise schedule, U-Net

- Forward process is fixed (known schedule), reverse is learned.
- Training objective: minimise noise prediction error.
- Sampling starts from pure noise and iteratively denoises.

---

### DDPM (Denoising Diffusion Probabilistic Models)

**Definition:** The original diffusion formulation (Ho et al., 2020). A Markov chain that adds Gaussian noise over 1000 timesteps in the forward direction and learns to reverse it. Sampling requires 1000 sequential neural network evaluations.

**Related Terms:** DDIM, noise schedule, diffusion model

- Forward: `q(x_t | x_{t-1}) = N(x_t; sqrt(1-β_t)x_{t-1}, β_t I)`.
- Reverse: `p_θ(x_{t-1} | x_t) = N(x_{t-1}; μ_θ(x_t, t), σ²_t I)`.
- Training: minimise `|| ε - ε_θ(x_t, t) ||²`.

---

### DDIM (Denoising Diffusion Implicit Models)

**Definition:** A reformulation of the diffusion reverse process that makes it **deterministic** given the initial noise. This allows using fewer sampling steps (20-50 instead of 1000) and supports interpolation between latent vectors.

**Related Terms:** DDPM, Euler sampler, diffusion model

- Non-Markovian: the reverse step can depend on x_0 prediction.
- Deterministic: same noise + same prompt = same image (useful for debugging).
- Enables latent interpolation for smooth transitions.

---

### CLIP (Contrastive Language-Image Pre-training)

**Definition:** A model (OpenAI, 2021) trained on 400 million (image, text) pairs using contrastive learning. It produces a shared embedding space where matching images and captions have high cosine similarity. The text encoder becomes the "brain" that guides image generation in Stable Diffusion.

**Related Terms:** contrastive learning, cross-attention, CFG

- Two encoders: text (Transformer) and image (ViT or ResNet).
- Training: maximise similarity for matching pairs, minimise for non-matching.
- Outputs L2-normalised embeddings (typically 512 or 768 dim).

---

### Contrastive Learning

**Definition:** A self-supervised learning paradigm that pulls representations of similar/positive pairs together and pushes negative pairs apart. In CLIP, positive pairs are (image, caption) from the same example; negatives are all other pairs in the batch.

**Related Terms:** CLIP, InfoNCE loss

- InfoNCE loss uses cross-entropy over the similarity matrix.
- Batch size matters: larger batches provide more negatives.
- Temperature controls how "peaky" the similarity distribution is.

---

### Cross-Attention

**Definition:** An attention mechanism where the query comes from one modality (e.g., U-Net features) and the key/value come from another (e.g., CLIP text embeddings). This is how the text prompt controls what the U-Net generates at each spatial location.

**Related Terms:** CLIP, U-Net, CFG

- Q = U-Net features projected to query space.
- K, V = CLIP text embeddings projected to key/value spaces.
- Output = attention-weighted sum of text embeddings, added to U-Net features.

---

### Classifier-Free Guidance (CFG)

**Definition:** A technique to amplify the effect of conditioning. At inference time, compute both the conditional prediction `ε_cond` (with prompt) and the unconditional prediction `ε_uncond` (with empty prompt). The final prediction is: `ε = ε_uncond + cfg_scale * (ε_cond - ε_uncond)`.

**Related Terms:** cross-attention, CLIP, diffusion model

- cfg_scale=1: no guidance (ignores prompt).
- cfg_scale=7.5: typical for Stable Diffusion.
- Higher values increase prompt adherence but reduce diversity.

---

### Noise Schedule

**Definition:** The sequence of variance parameters β_t (or α_t = 1 - β_t) over timesteps t=1:T. Determines how quickly noise is added in the forward process and how the reverse process is structured.

**Related Terms:** DDPM, Karras pre-conditioning, diffusion model

- Linear: β goes from 0.0001 to 0.02 over 1000 steps (DDPM original).
- Cosine: smoother schedule that avoids adding too much noise too early.
- Karras schedule: shifted log-normal distribution for improved training.

---

## Summary

1. **miniai** is the pedagogical framework built from scratch — tensors, autograd, optimisers, everything.
2. **VAEs** compress images into a **latent space** using the **reparameterisation trick**; Stable Diffusion's VAE achieves 48× compression.
3. **U-Nets** with skip connections are the backbone of diffusion, operating in latent space and conditioning on timestep via sinusoidal embeddings.
4. **DDPM** defines the forward (add noise) and reverse (remove noise) processes; training minimises noise prediction error.
5. **DDIM** and other samplers reduce inference steps from 1000 to 20-50.
6. **CLIP** provides text conditioning via **cross-attention**; **CFG** controls prompt adherence strength.
7. **Advanced techniques** (Textual Inversion, DreamBooth, LoRA) enable personalisation without full retraining.
