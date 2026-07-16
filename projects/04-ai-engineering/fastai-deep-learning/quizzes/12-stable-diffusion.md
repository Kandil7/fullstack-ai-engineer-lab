# Quiz 12: From Deep Learning Foundations to Stable Diffusion

## Topic Overview

This quiz covers fast.ai Part 2 — the sequel to Practical Deep Learning for Coders — which builds a complete text-to-image pipeline from the ground up. Topics include the miniai framework, ResNets and U-Nets, VAEs and the reparameterisation trick, CLIP and contrastive learning, the DDPM diffusion process, sampling methods, and the full Stable Diffusion pipeline.

---

## Questions

### Question 1

**What is the "miniai" framework built during fast.ai Part 2?**

- A) A production-ready AI deployment platform
- B) A didactic deep learning framework built from scratch in Jupyter notebooks, designed to be readable and modifiable
- C) A Python library for data augmentation
- D) A pre-trained image classification model

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** miniai is a small, pedagogical framework that reimplements tensors, autograd, optimisers, data loaders, and architectures from scratch. Unlike PyTorch or TensorFlow (production frameworks), miniai is designed to be completely understood by one person reading the notebooks.

</details>

---

### Question 2

**What is the reparameterisation trick in a VAE?**

- A) A method for compressing model weights
- B) Expressing a sample as `z = mean + std * epsilon` where epsilon is a standard normal sample, making the sampling step differentiable
- C) A technique for reducing the number of VAE layers
- D) Adding noise to the input during training

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Without the reparameterisation trick, sampling from a distribution is a non-differentiable operation. By writing `z = mean + std * epsilon`, the randomness is isolated in epsilon (which doesn't need gradients), while mean and std (which do) remain deterministic. This allows gradients to flow back through the encoder.

</details>

---

### Question 3

**What compression ratio does Stable Diffusion's VAE achieve?**

- A) 2× (512×512×3 → 256×256×3)
- B) 10× (512×512×3 → 512×512)
- C) 48× (512×512×3 → 64×64×4)
- D) 100× (512×512×3 → 32×32×3)

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Stable Diffusion's VAE compresses a 512×512×3 RGB image (786,432 values) into a 64×64×4 latent tensor (16,384 values) — a 48× compression. The diffusion U-Net operates entirely in this compressed latent space, making the process computationally feasible on consumer GPUs.

</details>

---

### Question 4

**What is the role of skip connections in a U-Net?**

- A) They make the network skip training on easy examples
- B) They preserve high-frequency spatial detail that would otherwise be lost during downsampling
- C) They connect the U-Net to the CLIP text encoder
- D) They reduce the number of parameters

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** As the encoder downsamples the input, spatial resolution decreases and some detail is lost. The skip connections copy feature maps from each encoder layer to the corresponding decoder layer, so the decoder can use both the high-level features (from the bottleneck) and the fine-grained spatial detail (from the skip connections).

</details>

---

### Question 5

**What does the DDPM training objective minimise?**

- A) The pixel-wise MSE between output and target images
- B) The difference between predicted noise and actual noise: `|| ε - ε_θ(x_t, t) ||²`
- C) The KL divergence between the data distribution and the model distribution
- D) The cross-entropy between predicted and true class labels

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The DDPM training objective is surprisingly simple: given a noisy image x_t at timestep t, the U-Net predicts the noise ε that was added. The loss is the mean squared error between the predicted noise and the actual noise. The model never directly predicts the clean image — it always predicts the noise.

</details>

---

### Question 6

**How does DDIM differ from DDPM?**

- A) DDIM trains faster
- B) DDIM has a deterministic reverse process, enabling fewer sampling steps (20-50 vs 1000)
- C) DDIM uses a different network architecture
- D) DDIM does not use a U-Net

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** DDIM (Denoising Diffusion Implicit Models) reformulates the reverse process to be non-Markovian and deterministic given the initial noise. This means you can take larger steps (fewer total steps) during sampling, reducing inference from 1000 steps to 20-50 while maintaining quality. It also enables interpolation between latent vectors.

</details>

---

### Question 7

**What is the purpose of the CLIP model in Stable Diffusion?**

- A) It generates the final image
- B) It creates a shared embedding space for images and text, allowing text prompts to guide image generation via cross-attention
- C) It compresses images into a latent space
- D) It removes noise from the latent representation

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** CLIP (Contrastive Language-Image Pre-training) is trained on 400 million (image, text) pairs to produce a shared embedding space. In Stable Diffusion, the CLIP text encoder produces embeddings of the text prompt that are injected into the U-Net via cross-attention layers, guiding the denoising process toward images that match the prompt.

</details>

---

### Question 8

**What is Classifier-Free Guidance (CFG)?**

- A) A method to train without labelled data
- B) Extrapolating between conditional and unconditional predictions to control prompt adherence: ε = ε_uncond + cfg_scale * (ε_cond - ε_uncond)
- C) A guidance method that requires a separate classifier model
- D) Removing the classifier from the diffusion pipeline

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** CFG controls how strongly the model adheres to the prompt. At inference, both a conditional prediction (with prompt) and an unconditional prediction (with empty prompt) are computed. The final prediction is an extrapolation away from the unconditional and toward the conditional. cfg_scale=7.5 is a typical value; higher values increase adherence but can reduce image quality and diversity.

</details>

---

### Question 9

**What is the key innovation of Karras et al. (2022) for diffusion models?**

- A) A new neural network architecture
- B) Pre-conditioning (scaling inputs/outputs so the model sees unit-variance data) and a shifted log-normal noise schedule
- C) Training without any noise
- D) Using GANs instead of diffusion

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Karras et al.'s "Elucidating the Design Space of Diffusion-Based Generative Models" reformulated the diffusion process with pre-conditioning (ensuring the U-Net always sees unit-variance data regardless of noise level) and improved noise schedules (shifted log-normal). These changes make training more stable and enable higher-order samplers (like Heun's method) for better quality with fewer steps.

</details>

---

### Question 10

**In Stable Diffusion, where does the U-Net operate?**

- A) In pixel space, directly on the 512×512 image
- B) In the VAE's latent space, on 64×64×4 tensors
- C) In the frequency domain, on Fourier-transformed images
- D) In the CLIP embedding space

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** This is the crucial insight of latent diffusion: the U-Net never sees pixels. It operates entirely in the compressed latent space produced by the VAE encoder (64×64×4). The VAE decoder only runs once at the end to convert the denoised latent back to a 512×512×3 image. This makes the diffusion process computationally feasible.

</details>

---

### Question 11

**What is the purpose of time conditioning in a diffusion U-Net?**

- A) It tracks how long the model has been training
- B) It tells the U-Net what noise level it is at — different timesteps have different amounts of noise to predict
- C) It schedules when to save checkpoints
- D) It measures inference speed

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The diffusion U-Net must know which timestep it is at because the amount of noise present varies dramatically across timesteps (a lot at early timesteps, a little at late ones). The sinusoidal time embedding is injected into each ResBlock via FiLM modulation (scale and shift), allowing the network to adjust its behaviour based on the noise level.

</details>

---

### Question 12

**What does the contrastive loss in CLIP maximise?**

- A) The similarity between matching image-text pairs while minimising it for non-matching pairs
- B) The accuracy of image classification
- C) The compression ratio of the VAE
- D) The diversity of generated images

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** CLIP uses a contrastive (InfoNCE) loss: for a batch of N (image, text) pairs, it computes cosine similarity between all pairs and then uses cross-entropy where the targets are the diagonal (matching pairs). This pulls matching image-text embeddings together while pushing all other pairs apart. The loss is symmetric (image→text + text→image).

</details>

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 7 | B |
| 2 | B | 8 | B |
| 3 | C | 9 | B |
| 4 | B | 10 | B |
| 5 | B | 11 | B |
| 6 | B | 12 | A |

---

*Generated for fast.ai Deep Learning — Module 12 (From Deep Learning Foundations to Stable Diffusion).*
