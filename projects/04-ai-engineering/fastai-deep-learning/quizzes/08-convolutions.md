# Quiz 08: Convolutions (CNNs)

## Topic Overview

Test your understanding of convolutions for images: what a kernel computes,
why convolutions beat dense layers on images, stride/padding and the
output-size formula, channels, receptive fields, pooling, batch normalization,
and the shape of a full small CNN. Based on fast.ai lesson 8.

**Difficulty:** Intermediate-Advanced
**Total Questions:** 10

---

### Question 1
What does a single convolution operation compute at one position?
- **A)** The maximum value in the overlapping patch
- **B)** The elementwise product of the kernel and the overlapping patch, summed into one number
- **C)** The dot product of the entire flattened image with a weight vector
- **D)** The average of every pixel in the image

---

### Question 2
Why do convolutions use far fewer parameters than a dense layer for images?
- **A)** They use fewer bits per weight
- **B)** They discard most of the input pixels
- **C)** They share one small kernel across every spatial position (weight sharing)
- **D)** They only run on grayscale images

---

### Question 3
In a trained CNN, where do the kernel values come from?
- **A)** They are hand-designed by the engineer (e.g. Sobel filters)
- **B)** They are fixed random values that never change
- **C)** They are learned parameters updated by gradient descent
- **D)** They are copied from the previous layer's activations

---

### Question 4
Using `out = (n + 2p - k)/s + 1`, what is the output size for `n=28`, `k=3`,
`s=2`, `p=1`?
- **A)** 28
- **B)** 14
- **C)** 26
- **D)** 7

---

### Question 5
What is the difference between `'same'` and `'valid'` padding (stride 1)?
- **A)** `'same'` keeps output size equal to input; `'valid'` uses no padding so output shrinks
- **B)** `'valid'` keeps output size equal to input; `'same'` shrinks it
- **C)** They are identical in every case
- **D)** `'same'` doubles the output size

---

### Question 6
For an RGB input and a conv layer with 32 filters, what is the shape of the
layer's weight tensor (kernel size 3)?
- **A)** `(3, 3, 3)`
- **B)** `(32, 3, 3, 3)`
- **C)** `(3, 32, 3, 3)`
- **D)** `(32, 32, 3, 3)`

---

### Question 7
What is a neuron's *receptive field*?
- **A)** The set of kernels in its layer
- **B)** The region of the original input image that can influence that neuron
- **C)** The learning rate used to train it
- **D)** The number of output channels

---

### Question 8
Which operation forces a feature map of any spatial size down to a fixed size
so the linear head works regardless of input resolution?
- **A)** `nn.Flatten`
- **B)** `nn.BatchNorm2d`
- **C)** `nn.AdaptiveAvgPool2d`
- **D)** `nn.ReLU`

---

### Question 9
What does batch normalization do?
- **A)** Randomly drops activations to regularize the network
- **B)** Normalizes each channel's activations across the batch, then applies a learnable scale and shift
- **C)** Increases the number of output channels
- **D)** Converts logits to probabilities

---

### Question 10
Why do ResNet-style skip connections help train very deep networks?
- **A)** They remove all nonlinearities
- **B)** They add the block's input back to its output, so each block only learns a residual and gradients flow more easily
- **C)** They reduce the number of channels to 1
- **D)** They replace convolutions with dense layers

---

## Answer Key

**1. B** — At each position a convolution multiplies the kernel elementwise
with the overlapping input patch and sums those products into a single output
value; the grid of such values is the feature map.

**2. C** — Convolutions reuse the same small kernel at every position (weight
sharing) and only look at local neighbourhoods, so a 3×3 kernel is 9 weights
regardless of image size, versus a weight per pixel for a dense layer.

**3. C** — In a CNN the kernel entries are learnable parameters initialized
(often randomly) and updated by SGD; the network discovers useful filters like
edge and texture detectors on its own.

**4. B** — `(28 + 2*1 - 3)/2 + 1 = (27)/2 + 1 = 13 + 1 = 14` (integer floor).
Stride-2 convs roughly halve spatial size.

**5. A** — `'valid'` means no padding, so a `k×k` kernel shrinks the output by
`k-1`. `'same'` pads (for stride 1, `p=(k-1)//2`) so the output keeps the input
size.

**6. B** — `nn.Conv2d` weight shape is `(out_channels, in_channels, k, k)`, so
32 filters over 3 input channels with a 3×3 kernel gives `(32, 3, 3, 3)`.

**7. B** — The receptive field is the region of the original image that can
influence a given unit; it grows with depth and downsampling, letting deep
units respond to large, complex patterns.

**8. C** — `nn.AdaptiveAvgPool2d` (e.g. to 1×1) produces a fixed output size for
any input, decoupling the linear head from input resolution. `Flatten` only
reshapes; it does not fix spatial size.

**9. B** — Batch normalization standardizes each channel's activations across
the batch to ~zero mean / unit variance, then applies learnable scale `γ` and
shift `β`, stabilizing and accelerating training.

**10. B** — A skip connection adds the block input to its output (`out = F(x) +
x`), so each block only needs to learn the residual change and gradients can
flow through the identity path, enabling reliable training of very deep nets.
