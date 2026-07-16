# Glossary: Convolutions (CNNs)

## Quick Reference Table

| Term | One-Line Definition |
|------|--------------------|
| Convolution | Sliding a small kernel across an input, computing a weighted sum at each position |
| Kernel / Filter | The small grid of (usually learned) weights applied at each position |
| Feature Map | The grid of outputs produced by applying one kernel across the input |
| Stride | How many pixels the kernel jumps between positions |
| Padding | Border of zeros added to control output size (`'same'` vs `'valid'`) |
| Channel | A depth slice of a tensor; RGB input has 3, output channels = number of filters |
| Receptive Field | Region of the original image that can influence a given output unit |
| Weight Sharing | Reusing the same kernel weights at every spatial position |
| Translation Invariance | Detecting a feature the same way wherever it appears |
| `nn.Conv2d` | PyTorch module implementing a learnable 2-D convolution layer |
| Pooling | Downsampling by taking the max or mean over a window |
| Adaptive Pooling | Pooling to a fixed output size regardless of input size |
| Flatten | Collapsing spatial/channel dims into a vector for a linear layer |
| Batch Normalization | Normalizing per-channel activations across a batch, then scaling/shifting |
| ReLU | Nonlinearity `max(0, x)` applied after conv/BN |
| Output Size Formula | `out = (n + 2p - k)/s + 1` |
| CNN | A network built primarily from stacked convolutional layers |

---

## Detailed Definitions

### Convolution

**Definition**: An operation that slides a small kernel across an input tensor
and, at each position, computes the elementwise product of the kernel with the
overlapping input patch and sums it into a single output value.

**Example**:
```python
import torch
import torch.nn.functional as F

image = torch.arange(25.0).reshape(1, 1, 5, 5)   # (N, C, H, W)
kernel = torch.ones(1, 1, 3, 3)                  # simple box filter
out = F.conv2d(image, kernel)                    # 'valid' -> (1, 1, 3, 3)
print(out.shape)  # torch.Size([1, 1, 3, 3])
```

**Related**: Kernel, Feature Map, `nn.Conv2d`

---

### Kernel / Filter

**Definition**: The small grid of weights (e.g. 3×3) applied at every position.
In a CNN these weights are learned parameters. A single conv layer holds many
kernels; each kernel spans all input channels and produces one output channel.

**Example**:
```python
import torch.nn as nn

conv = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3)
print(conv.weight.shape)  # (16, 3, 3, 3): 16 kernels, each 3x3 over 3 channels
```

**Related**: Weight Sharing, Channel, Convolution

---

### Feature Map

**Definition**: The 2-D grid of activations produced by applying one kernel
across the whole input. A conv layer with `C_out` filters produces `C_out`
feature maps stacked along the channel dimension.

**Example**:
```python
# Output of nn.Conv2d(1, 8, 3) on a 28x28 image -> 8 feature maps of 26x26
# shape: (N, 8, 26, 26)
```

**Related**: Channel, Convolution, Receptive Field

---

### Stride

**Definition**: The step size (in pixels) the kernel moves between positions.
Stride 1 visits every position; stride 2 skips every other one and roughly
halves the output spatial size (downsampling).

**Example**:
```python
import torch.nn as nn

nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1)  # 28x28 -> 14x14
```

**Related**: Padding, Output Size Formula, Pooling

---

### Padding

**Definition**: A border of (usually zero) pixels added around the input so
edge pixels are treated fairly and output size can be controlled. `'valid'`
means no padding (output shrinks); `'same'` means enough padding to keep output
size equal to input (for stride 1, `p = (k-1)//2`).

**Example**:
```python
import torch.nn as nn

nn.Conv2d(16, 16, 3, padding=0)  # 'valid': 28 -> 26
nn.Conv2d(16, 16, 3, padding=1)  # 'same' : 28 -> 28
```

**Related**: Stride, Output Size Formula, Convolution

---

### Channel

**Definition**: A depth slice of an image/feature tensor. Input channels
describe the data (RGB = 3, grayscale = 1); output channels equal the number of
filters in the layer. A conv layer maps `C_in -> C_out`.

**Example**:
```python
# input : (N, 3,  H, W)   RGB
# conv  : nn.Conv2d(3, 64, 3)
# output: (N, 64, H', W')  64 feature maps
```

**Related**: Kernel, Feature Map, `nn.Conv2d`

---

### Receptive Field

**Definition**: The region of the *original* input that can influence a
particular output unit. It grows as layers stack and as downsampling occurs,
letting deep units respond to large, complex patterns.

**Example**:
```python
# 3x3 conv -> unit sees 3x3 of the input
# two stacked 3x3 convs -> unit sees ~5x5
# add downsampling -> effective receptive field grows faster
```

**Related**: Feature Map, CNN, Stride

---

### Weight Sharing

**Definition**: Using the same kernel weights at every spatial position rather
than a separate weight per pixel. This slashes parameter count and encodes the
prior that useful features can appear anywhere in the image.

**Example**:
```python
# A dense layer on 28x28: 784 weights per neuron (none reused).
# A 3x3 conv kernel: 9 weights, applied at every position.
```

**Related**: Translation Invariance, Kernel, Convolution

---

### Translation Invariance

**Definition**: The property that a feature is detected the same way regardless
of where it appears in the image, a direct consequence of weight sharing.

**Example**:
```python
# The same edge kernel fires whether the edge is top-left or bottom-right.
```

**Related**: Weight Sharing, Convolution, Pooling

---

### `nn.Conv2d`

**Definition**: PyTorch's learnable 2-D convolution layer. Key arguments:
`in_channels`, `out_channels`, `kernel_size`, `stride`, `padding`. Its
`.weight` tensor has shape `(out_channels, in_channels, k, k)`.

**Example**:
```python
import torch, torch.nn as nn

conv = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
y = conv(torch.randn(8, 1, 28, 28))
print(y.shape)  # torch.Size([8, 32, 28, 28])
```

**Related**: Convolution, Channel, Batch Normalization

---

### Pooling (max / avg)

**Definition**: A parameter-free downsampling operation that takes the maximum
(`MaxPool2d`) or mean (`AvgPool2d`) over each non-overlapping window, shrinking
spatial size while keeping channels fixed.

**Example**:
```python
import torch, torch.nn as nn

pool = nn.MaxPool2d(kernel_size=2)       # 2x2 windows
print(pool(torch.randn(1, 8, 28, 28)).shape)  # (1, 8, 14, 14)
```

**Related**: Stride, Adaptive Pooling, Downsampling

---

### Adaptive Pooling

**Definition**: Pooling that produces a *fixed* output size regardless of input
size, by choosing window sizes automatically. `AdaptiveAvgPool2d(1)` collapses
any spatial map to 1×1, decoupling the linear head from input resolution.

**Example**:
```python
import torch, torch.nn as nn

ap = nn.AdaptiveAvgPool2d(1)
print(ap(torch.randn(4, 64, 7, 7)).shape)  # (4, 64, 1, 1)
```

**Related**: Pooling, Flatten, CNN

---

### Flatten

**Definition**: Reshaping a multi-dimensional tensor into a 2-D `(N, features)`
tensor so it can be fed to a linear (fully connected) layer.

**Example**:
```python
import torch, torch.nn as nn

flat = nn.Flatten()
print(flat(torch.randn(4, 64, 1, 1)).shape)  # (4, 64)
```

**Related**: Adaptive Pooling, CNN, `nn.Conv2d`

---

### Batch Normalization

**Definition**: A layer that normalizes each channel's activations across the
batch to ~zero mean / unit variance, then applies a learnable scale `γ` and
shift `β`. It stabilizes and accelerates training and allows higher learning
rates. In CNNs use `nn.BatchNorm2d`.

**Example**:
```python
import torch, torch.nn as nn

bn = nn.BatchNorm2d(32)
print(bn(torch.randn(8, 32, 14, 14)).shape)  # (8, 32, 14, 14)
```

**Related**: ReLU, `nn.Conv2d`, CNN

---

### ReLU

**Definition**: The Rectified Linear Unit nonlinearity `max(0, x)`. Applied
after conv (and BatchNorm) to introduce nonlinearity cheaply while avoiding the
vanishing-gradient issues of sigmoid/tanh.

**Example**:
```python
import torch, torch.nn.functional as F

print(F.relu(torch.tensor([-2.0, 0.0, 3.0])))  # tensor([0., 0., 3.])
```

**Related**: Batch Normalization, Convolution, CNN

---

### Output Size Formula

**Definition**: The rule for a conv/pool layer's output spatial size:
`out = (n + 2p - k)/s + 1` (floored), where `n` is input size, `p` padding,
`k` kernel size, `s` stride.

**Example**:
```python
# n=28, k=3, s=2, p=1 -> (28 + 2 - 3)//2 + 1 = 14
```

**Related**: Stride, Padding, `nn.Conv2d`

---

### CNN (Convolutional Neural Network)

**Definition**: A network built primarily from stacked convolutional layers
(with activations, normalization, and downsampling) that progressively grows
channels and shrinks spatial size, ending in a linear head. Excels at images by
exploiting locality and weight sharing.

**Example**:
```python
import torch.nn as nn

cnn = nn.Sequential(
    nn.Conv2d(1, 16, 3, stride=2, padding=1), nn.BatchNorm2d(16), nn.ReLU(),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(16, 10),
)
```

**Related**: `nn.Conv2d`, Receptive Field, Batch Normalization

---

## Summary

Convolutions apply small, reusable kernels across an image to build feature
maps, trading the parameter blow-up of dense layers for locality, weight
sharing, and translation invariance. Stride and padding set output size via
`out = (n + 2p - k)/s + 1`; conv layers map `C_in -> C_out`; and real CNNs grow
channels while shrinking space using pooling or stride-2 convs, then flatten
into a linear head. `Conv -> BatchNorm -> ReLU` blocks, adaptive pooling, and
ResNet skip connections are the standard building materials.

**Next:** See [Lecture 09: Data Ethics](09-data-ethics-lecture.md) for feedback loops, bias, disaggregated evaluation, and a pre-ship checklist.
