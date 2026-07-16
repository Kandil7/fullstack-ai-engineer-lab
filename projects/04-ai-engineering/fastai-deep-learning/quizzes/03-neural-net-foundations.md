# Quiz 03: Neural Net Foundations (SGD)

## Topic Overview

This quiz tests your understanding of how models learn: the 7-step SGD
process, gradient descent intuition, PyTorch autograd, the training loop,
learning rates, and the jump from a linear function to a neural net via a
ReLU nonlinearity. It corresponds to fast.ai lesson 3.

**Difficulty:** Intermediate
**Questions:** 10
**Time:** ~15 minutes
**Passing Score:** 70% (7/10)

---

### Question 1 [Easy]
**Which sequence correctly lists the SGD process?**

A) predict → init → loss → step → gradients → repeat → stop
B) init → predict → loss → gradients → step → repeat → stop
C) init → loss → predict → step → gradients → repeat → stop
D) init → predict → gradients → loss → step → repeat → stop

**Difficulty:** Easy
**Correct Answer:** B
**Explanation:** The canonical fast.ai 7 steps are: initialize weights,
predict, compute loss, compute gradients, step (update weights), repeat, and
stop. Gradients require the loss first, and the step requires the gradients.

---

### Question 2 [Easy]
**In the update rule, why do we subtract the gradient rather than add it?**

A) The gradient is always negative
B) The gradient points uphill (toward higher loss), so we move opposite it
C) Subtraction is faster than addition in PyTorch
D) It keeps the weights positive

**Difficulty:** Easy
**Correct Answer:** B
**Explanation:** The gradient points in the direction of steepest *increase*
in the loss. To reduce the loss we move in the opposite direction, hence
`weight -= lr * weight.grad`.

---

### Question 3 [Medium]
**For `y = x ** 2` with `x = torch.tensor(4.0).requires_grad_()`, what is
`x.grad` after `y.backward()`?**

A) 4.0
B) 8.0
C) 16.0
D) 2.0

**Difficulty:** Medium
**Correct Answer:** B
**Explanation:** The derivative of `x^2` is `2x`. At `x = 4`, that is
`2 * 4 = 8`. PyTorch's autograd computes this and stores it in `x.grad`.

---

### Question 4 [Medium]
**Why must you call `grad.zero_()` (or `opt.zero_grad()`) each iteration?**

A) To free GPU memory
B) Because PyTorch accumulates (adds to) gradients on each `.backward()`
C) To reset the model weights
D) Because `.backward()` fails otherwise

**Difficulty:** Medium
**Correct Answer:** B
**Explanation:** PyTorch *adds* new gradients into `.grad` rather than
replacing them. Without zeroing, iteration 2 would use the sum of iteration 1
and 2's gradients, corrupting the update. Zeroing keeps each step's gradient
clean.

---

### Question 5 [Medium]
**What happens when the learning rate is set far too high?**

A) Training is very slow but eventually converges
B) The loss oscillates or diverges (often to `nan`) as steps overshoot
C) The gradients become zero
D) The model trains normally but uses more memory

**Difficulty:** Medium
**Correct Answer:** B
**Explanation:** A too-high learning rate makes each step overshoot the
minimum, so the loss bounces around or explodes. A too-low rate is the
opposite problem: safe but painfully slow.

---

### Question 6 [Medium]
**What does the fast.ai learning-rate finder (`lr_find`) do?**

A) Sets the learning rate to a fixed default
B) Increases the lr exponentially over a few batches and plots loss vs. lr
C) Trains the model to completion at every possible lr
D) Computes the optimal lr analytically from the data

**Difficulty:** Medium
**Correct Answer:** B
**Explanation:** `lr_find` starts from a tiny learning rate and ramps it up
exponentially over a handful of mini-batches, recording the loss. You then
pick a rate on the steep downslope, roughly an order of magnitude before the
loss bottoms out.

---

### Question 7 [Medium]
**Which computes the ReLU of a tensor `t` in PyTorch?**

A) `t.mean()`
B) `t.clamp(min=0)`
C) `t.sigmoid()`
D) `t.abs()`

**Difficulty:** Medium
**Correct Answer:** B
**Explanation:** ReLU is `max(t, 0)` — negatives become zero, positives pass
through. `t.clamp(min=0)` (equivalently `torch.nn.functional.relu(t)` or
`torch.max(t, torch.tensor(0.))`) implements this.

---

### Question 8 [Hard]
**Why does stacking two linear layers with no nonlinearity between them gain
no representational power?**

A) PyTorch merges them automatically to save memory
B) The composition of linear functions is itself linear, so it collapses to a single linear layer
C) The second layer's weights are always zero
D) Gradients cannot flow through two layers

**Difficulty:** Hard
**Correct Answer:** B
**Explanation:** `(x @ w1 + b1) @ w2 + b2` is still an affine (linear)
function of `x` and could be written as a single `x @ w + b`. A nonlinearity
like ReLU between the layers is what lets the network model non-linear
functions — the basis of universal approximation.

---

### Question 9 [Hard]
**Why must a parameter update be wrapped in `torch.no_grad()`?**

A) To make the update run on the GPU
B) So the in-place update is not recorded by autograd and does not corrupt the graph
C) To convert the tensor to a NumPy array
D) Because `no_grad()` computes the gradient faster

**Difficulty:** Hard
**Correct Answer:** B
**Explanation:** The weight update `params -= lr * params.grad` is not part of
the model's forward computation. Wrapping it in `torch.no_grad()` stops
autograd from tracking it, avoiding a runtime error about modifying a leaf
variable that requires grad and keeping the computation graph correct.

---

### Question 10 [Medium]
**In the MNIST 3s-vs-7s example, what is the role of the "pixel similarity"
baseline?**

A) It is the final production model
B) It is a simple non-learned benchmark (nearest to average 3 or 7) that the learned classifier should beat
C) It computes the gradients for SGD
D) It replaces the loss function

**Difficulty:** Medium
**Correct Answer:** B
**Explanation:** fast.ai first classifies each image by whether it is closer
to the average 3 or the average 7 (mean pixel difference). This non-learned
baseline sets a bar: a learned SGD classifier is only worthwhile if it beats
this simple approach.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Medium |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Medium |

**Scoring:**
- 9-10 correct: Excellent — you understand the SGD engine.
- 7-8 correct: Good — review learning rates and autograd internals.
- Below 7: Re-read the lecture and run the exercise, especially the
  from-scratch training loop and the ReLU section.
