# Lecture 08: Convolutions (CNNs)

## Topic Overview

Dense (fully connected) layers treat every input pixel as unrelated to its
neighbours and give each one its own weight. For a modest 28×28 image that is
already 784 weights *per neuron*; for a real photo it explodes. Worse, a
pattern learned in the top-left corner has to be re-learned from scratch in the
bottom-right. **Convolutions** fix both problems. A convolution slides a small
grid of weights — a **kernel** — across the image, computing a weighted sum at
every position. The same kernel is reused everywhere (**weight sharing**), it
only looks at a local neighbourhood (**locality**), and it responds the same
way wherever a feature appears (**translation invariance**).

This lecture builds convolutions bottom-up, exactly as fast.ai lesson 8 does on
MNIST: first the arithmetic of a hand-designed edge detector on a tiny patch,
then the realization that the kernel numbers can be *learned*, then stride,
padding, and channels, and finally a full small CNN in PyTorch with pooling,
batch normalization, and a linear head — with a note on ResNet skip
connections for going deeper.

**Duration:** 3-4 hours
**Difficulty:** Intermediate-Advanced
**Prerequisites:** Lectures 01-05

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what a convolution computes and work the arithmetic of a kernel over a single image patch by hand
2. Justify why convolutions suit images using locality, weight sharing, and translation invariance
3. Describe how kernels move from hand-designed filters to *learned* parameters inside a CNN
4. Compute output spatial size for any stride/padding and distinguish `'same'` from `'valid'`
5. Reason about input channels vs. output channels and how a conv layer maps `C_in -> C_out`
6. Build convolutions in PyTorch with `F.conv2d` and `nn.Conv2d`, stacking layers that grow channels while shrinking spatial size
7. Apply pooling, stride-2 convs, adaptive pooling, flatten, ReLU, and batch normalization in a working CNN
8. Explain the receptive field, feature hierarchy (edges → textures → objects), and how ResNet skip connections enable depth

---

## Key Concepts

### 1. A convolution is a sliding weighted sum

A kernel is a small weight grid (commonly 3×3). Place it over the top-left of
the image, multiply overlapping cells elementwise, sum them into **one** output
number, then slide right by the stride and repeat. The full grid of outputs is
a **feature map**.

```python
# One output pixel = sum(kernel * patch)
# Kernel K (3x3) sitting on image patch P (3x3):
#
#   Image (5x5)                Kernel (3x3)
#   ┌──┬──┬──┬──┬──┐           ┌──┬──┬──┐
#   │P │P │P │  │  │           │k │k │k │
#   ├──┼──┼──┼──┼──┤           ├──┼──┼──┤
#   │P │P │P │  │  │  ⊙ slide  │k │k │k │  -> one number
#   ├──┼──┼──┼──┼──┤           ├──┼──┼──┤
#   │P │P │P │  │  │           │k │k │k │
#   ├──┼──┼──┼──┼──┤           └──┴──┴──┘
#   │  │  │  │  │  │
#   ├──┼──┼──┼──┼──┤
#   │  │  │  │  │  │
#   └──┴──┴──┴──┴──┘
#
# Output[0,0] = P[0,0]*k[0,0] + P[0,1]*k[0,1] + ... + P[2,2]*k[2,2]
```

### 2. A concrete edge-detector kernel

A vertical-edge kernel has a negative column, a zero column, and a positive
column. On a flat (constant) patch the positives and negatives cancel to ~0; on
a patch straddling a light/dark boundary they do **not** cancel, so the output
lights up.

```python
# Vertical Sobel-style kernel:            Flat patch -> ~0
#   ┌────┬───┬────┐                        ┌───┬───┬───┐
#   │ -1 │ 0 │ +1 │                        │ 5 │ 5 │ 5 │
#   ├────┼───┼────┤                        ├───┼───┼───┤
#   │ -2 │ 0 │ +2 │                        │ 5 │ 5 │ 5 │
#   ├────┼───┼────┤                        ├───┼───┼───┤
#   │ -1 │ 0 │ +1 │                        │ 5 │ 5 │ 5 │
#   └────┴───┴────┘                        └───┴───┴───┘
#  (-1*5 -2*5 -1*5) + (0) + (+1*5 +2*5 +1*5) = 0
#
#  Edge patch (dark|light) -> strong response:
#   ┌───┬───┬────┐
#   │ 0 │ 0 │ 10 │   left=-? cancels little, right=+ large
#   ├───┼───┼────┤   sum = (0) + 0 + (10+20+10) = +40   <-- edge!
#   │ 0 │ 0 │ 10 │
#   ├───┼───┼────┤
#   │ 0 │ 0 │ 10 │
#   └───┴───┴────┘
```

### 3. Why convolutions beat dense layers on images

```python
# Dense layer on a 28x28 image, 1 neuron:
#   weights = 28*28 = 784   (and none are reused)
#
# Conv layer, one 3x3 kernel:
#   weights = 3*3 = 9       (reused at EVERY position)
#
# Three properties fall out for free:
#   locality              -> a pixel only interacts with its neighbours
#   weight sharing        -> 9 numbers scan the whole image
#   translation invariance-> a cat in the corner fires the same kernel
```

Far fewer parameters means less overfitting and far less compute, while weight
sharing bakes in the prior that *image statistics are the same everywhere*.

### 4. Kernels are learned, not hand-designed

The Sobel numbers above were chosen by a human. In a CNN the kernel entries are
**parameters** initialized randomly and updated by SGD (Lecture 03). The
network *discovers* that edge detectors are useful — plus blob, corner, and
texture detectors we would never have written by hand.

```python
import torch.nn as nn

conv = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3)
# conv.weight has shape (16, 1, 3, 3) -> 16 learnable 3x3 kernels
# These start random and are optimized during training.
print(conv.weight.shape)  # torch.Size([16, 1, 3, 3])
```

### 5. Stride, padding, and the output-size formula

Stride `s` is how far the kernel jumps each step. Padding `p` adds a border of
zeros so edge pixels get equal treatment. For input size `n`, kernel `k`:

```
out = (n + 2p - k) / s + 1        (floor the division)
```

```python
# 'valid' padding (p=0): output shrinks by (k-1)
#   n=5, k=3, s=1, p=0 -> (5 - 3)/1 + 1 = 3
#
# 'same' padding: choose p so output == input (for s=1, p=(k-1)/2)
#   n=5, k=3, s=1, p=1 -> (5 + 2 - 3)/1 + 1 = 5
#
# stride-2 downsampling halves spatial size:
#   n=28, k=3, s=2, p=1 -> (28 + 2 - 3)/2 + 1 = 14
#
#   valid (p=0, s=1)          same (p=1, s=1)
#   ┌──┬──┬──┬──┬──┐          0 0 0 0 0 0 0
#   │  │  │  │  │  │          0 ┌──┬──┬──┐ 0
#   │  │  │  │  │  │  -> 3x3   0 │  │  │  │ 0  -> 5x5
#   └──┴──┴──┴──┴──┘          0 └──┴──┴──┘ 0
```

### 6. Channels: C_in -> C_out

A colour image has 3 input channels (R, G, B). Each kernel spans **all** input
channels and produces **one** output channel; the number of output channels
equals the number of filters. So a conv layer maps `C_in` channels to `C_out`
channels, and each kernel has shape `(C_in, k, k)`.

```python
# RGB input, 32 filters, 3x3 kernels:
#   input : (N, 3,  H, W)
#   weight: (32, 3, 3, 3)   # 32 kernels, each spans 3 input channels
#   output: (N, 32, H', W') # 32 feature maps stacked along channel dim
conv = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
```

### 7. Receptive field and the feature hierarchy

A neuron's **receptive field** is the region of the *original* image that can
influence it. Stacking convs (and downsampling) grows it: layer 1 sees 3×3,
layer 2 sees ~5×5, and so on. Zeiler & Fergus's feature visualizations showed
early layers learn edges and colours, middle layers learn textures and parts,
and deep layers learn whole objects.

```python
# Receptive field grows with depth:
#   layer 1 (3x3)     layer 2 (3x3 on top)    layer 3 ...
#   ┌───┐             ┌───────┐               ┌───────────┐
#   │▓▓▓│  sees 3x3   │▓▓▓▓▓  │  sees ~5x5    │  whole     │  sees ~7x7+
#   └───┘             └───────┘               │  object    │
#   edges             textures/parts          └───────────┘  objects
```

### 8. Downsampling, pooling, and the linear head

To turn spatial feature maps into a class prediction, a CNN progressively
**increases channels** (richer features) while **decreasing spatial size**
(coarser location), then collapses to a vector for a linear classifier.
Downsampling is done with **pooling** (max/avg over a window) or **stride-2
convs**. **Adaptive pooling** forces any spatial size down to a fixed target
(e.g. 1×1) so the head works for any input resolution.

```python
import torch.nn.functional as F

# Downsample options (input 4x4 -> 2x2):
#   max pool 2x2                 avg pool 2x2
#   ┌──┬──┬──┬──┐  take max      take mean of each 2x2 block
#   │1 │3 │2 │0 │  of each  ->   -> smaller feature map
#   │4 │2 │1 │5 │  2x2 block
#   └──┴──┴──┴──┘   => [[4,5],...]
#
# Adaptive pool to 1x1 then flatten -> linear head:
#   (N, C, H, W) --AdaptiveAvgPool2d(1)--> (N, C, 1, 1)
#                --flatten-->             (N, C)
#                --Linear(C, n_classes)-> (N, n_classes)
```

### 9. Batch normalization

**Batch normalization** normalizes each channel's activations across the batch
to roughly zero mean / unit variance, then applies a learnable scale (`γ`) and
shift (`β`). It smooths the loss landscape, allows higher learning rates, acts
as mild regularization, and reduces sensitivity to weight initialization —
which is why `Conv -> BatchNorm -> ReLU` is the standard CNN block.

```python
# For each channel c, over the batch (and spatial dims):
#   x_hat = (x - mean_c) / sqrt(var_c + eps)
#   y     = gamma_c * x_hat + beta_c        # gamma, beta are learned
bn = nn.BatchNorm2d(num_features=32)  # one gamma/beta pair per channel
```

---

## Code Examples

### Example 1: A hand-made edge detector with `F.conv2d`

```python
import torch
import torch.nn.functional as F

# A tiny 1-channel "image": a vertical light/dark boundary.
image = torch.tensor(
    [[0.0, 0.0, 10.0, 10.0, 10.0],
     [0.0, 0.0, 10.0, 10.0, 10.0],
     [0.0, 0.0, 10.0, 10.0, 10.0],
     [0.0, 0.0, 10.0, 10.0, 10.0],
     [0.0, 0.0, 10.0, 10.0, 10.0]]
)
# conv2d expects (N, C, H, W)
image = image.reshape(1, 1, 5, 5)

# Vertical-edge kernel, shape (out_ch=1, in_ch=1, 3, 3)
vertical_edge = torch.tensor(
    [[-1.0, 0.0, 1.0],
     [-2.0, 0.0, 2.0],
     [-1.0, 0.0, 1.0]]
).reshape(1, 1, 3, 3)

feature_map = F.conv2d(image, vertical_edge)  # 'valid', s=1 -> 3x3
print(feature_map[0, 0])
# The column sitting on the boundary lights up (+40), flat regions ~0:
# tensor([[40., 40.,  0.],
#         [40., 40.,  0.],
#         [40., 40.,  0.]])
```

### Example 2: A small CNN as `nn.Sequential` (MNIST-shaped input)

```python
import torch
import torch.nn as nn

def conv_block(in_ch: int, out_ch: int) -> nn.Sequential:
    """Standard block: stride-2 conv downsamples, then BN, then ReLU."""
    return nn.Sequential(
        nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True),
    )

# Input: (N, 1, 28, 28). Grow channels, shrink spatial size.
model = nn.Sequential(
    conv_block(1, 16),               # 28 -> 14
    conv_block(16, 32),              # 14 -> 7
    conv_block(32, 64),              # 7  -> 4
    nn.AdaptiveAvgPool2d(1),         # 4  -> 1  (any size -> 1x1)
    nn.Flatten(),                    # (N, 64, 1, 1) -> (N, 64)
    nn.Linear(64, 10),               # 10-class head
)

x = torch.randn(8, 1, 28, 28)        # a fake batch of 8 digits
logits = model(x)
print(logits.shape)                  # torch.Size([8, 10])
```

### Example 3: A ResNet-style block with a skip connection

```python
import torch
import torch.nn as nn

class ResBlock(nn.Module):
    """out = ReLU(x + F(x)); the identity path lets gradients flow."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x                          # the "skip"
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out = out + identity                  # add input back in
        return self.relu(out)

# Deep plain nets get *harder* to train; the skip connection makes each
# block only need to learn a residual (the change), so very deep nets
# (ResNet-18/34/50) train reliably.
block = ResBlock(32)
print(block(torch.randn(4, 32, 14, 14)).shape)  # torch.Size([4, 32, 14, 14])
```

---

## Common Mistakes to Avoid

**1. Forgetting the 4-D `(N, C, H, W)` shape**

```python
# BAD: passing a bare 2-D image to a conv
img = torch.randn(28, 28)
F.conv2d(img, kernel)          # RuntimeError: expected 4D input

# GOOD: add batch and channel dims
img = torch.randn(28, 28).reshape(1, 1, 28, 28)
F.conv2d(img, kernel)          # works
```

**2. Mismatching padding when you want `'same'` output**

```python
# BAD: 3x3 conv with no padding silently shrinks every layer
nn.Conv2d(16, 16, kernel_size=3)              # 28 -> 26 -> 24 -> ...

# GOOD: p = (k-1)//2 keeps spatial size for stride-1
nn.Conv2d(16, 16, kernel_size=3, padding=1)   # 28 -> 28
```

**3. Wrong `in_features` into the linear head**

```python
# BAD: hard-guessing the flattened size (brittle, resolution-dependent)
nn.Linear(32 * 7 * 7, 10)      # breaks if input size changes

# GOOD: collapse spatial dims first so the head only sees channels
nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 10))
```

---

## Best Practices

1. Prefer small 3×3 kernels stacked deep over one large kernel — same receptive field, fewer parameters, more nonlinearity.
2. Use `padding=(k-1)//2` for `'same'` behaviour when you want to preserve spatial size on stride-1 convs.
3. Downsample deliberately with stride-2 convs or pooling; roughly double channels each time you halve spatial size.
4. Standardize on the `Conv -> BatchNorm -> ReLU` block; put BatchNorm before the activation.
5. End with `AdaptiveAvgPool2d(1)` + `Flatten` so the linear head is independent of input resolution.
6. Always sanity-check tensor shapes by running one fake batch through the model before training.
7. Normalize inputs (e.g. to mean 0, std 1) so the first conv sees well-scaled data.
8. Reach for a pretrained CNN (transfer learning) before training from scratch on small datasets.
9. Use skip connections (ResNet blocks) once depth grows beyond a handful of layers.
10. Visualize early-layer filters and feature maps to confirm the network is learning sensible edge/texture detectors.

---

## Practice Exercises

1. **By hand:** Apply the horizontal-edge kernel `[[-1,-2,-1],[0,0,0],[1,2,1]]` to a 4×4 patch that has a top-dark/bottom-light boundary and confirm which rows light up.
2. **Output size:** For `n=32, k=5, s=1, p=2` and for `n=32, k=3, s=2, p=1`, compute the output spatial size with the formula, then verify with `nn.Conv2d`.
3. **Channels:** Build a `nn.Conv2d(3, 8, 3, padding=1)`, print `conv.weight.shape`, and explain each dimension.
4. **Downsampling swap:** Take the Example 2 CNN and replace the stride-2 convs with stride-1 convs + `nn.MaxPool2d(2)`; confirm the shapes still reduce 28→14→7 and compare parameter counts.
5. **Skip connection:** Insert the `ResBlock` from Example 3 between two `conv_block`s and confirm the forward pass shape is unchanged where channels match.

---

## Summary

A convolution slides a small kernel across an image, computing a local weighted
sum at each position to build a feature map. Compared to dense layers it wins
through locality, weight sharing, and translation invariance — few parameters,
strong image prior. In a CNN those kernel weights are *learned* by SGD. Stride
and padding control output size via `out = (n + 2p - k)/s + 1`; each conv layer
maps `C_in -> C_out` where output channels = number of filters. Real networks
grow channels while shrinking spatial size, using pooling or stride-2 convs to
downsample and adaptive pooling + flatten to reach a linear head.
`Conv -> BatchNorm -> ReLU` is the workhorse block, the receptive field grows
with depth (edges → textures → objects), and ResNet skip connections let very
deep networks train reliably.

**Next lecture:** [Lecture 09: Data Ethics](09-data-ethics-lecture.md) — feedback loops, bias, disaggregated evaluation, and a practical checklist before you ship a model.
