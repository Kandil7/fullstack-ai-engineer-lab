# Glossary: Getting Started

> Terms from fast.ai Lesson 1. Each detailed entry includes a definition, an example, related terms, and key points.

## Quick Reference Table

| Term | Definition | Key Point |
|------|------------|-----------|
| Machine Learning | Training a model to learn behavior from data instead of explicit rules | Weights are learned, not written |
| Weights (Parameters) | Numbers inside a model that control its behavior | Adjusted automatically during training |
| Neural Network | A flexible model that can approximate almost any function | Same architecture, different learned weights |
| Transfer Learning | Reusing a model pretrained on a large dataset for a new task | Great results from small data |
| Pretrained Model | A model whose weights were already trained (e.g. on ImageNet) | Starting point for fine-tuning |
| ResNet | A family of convolutional architectures (resnet18/34/50…) | `resnet34` is the Lesson 1 default |
| DataLoaders | Object bundling training + validation `DataLoader`s | Feeds batches to the model |
| Learner | Object tying data + model + loss + metrics together | `vision_learner` builds one |
| vision_learner | Constructor for a CV `Learner` (formerly `cnn_learner`) | Adds a fresh head to a pretrained body |
| fine_tune | Training schedule: train head, then unfreeze and train all | The transfer-learning workhorse |
| Epoch | One full pass through the training data | More epochs risk overfitting |
| Learning Rate | Step size for weight updates | Too high diverges, too low crawls |
| Loss vs Metric | Loss is optimized; metric is read by humans | `error_rate` is a metric |
| Validation Set | Held-out data never trained on | Detects overfitting |
| Overfitting | Memorizing training data instead of generalizing | Validation error rises |
| error_rate | Fraction of validation predictions that are wrong | `accuracy = 1 - error_rate` |

## Detailed Definitions

### Machine Learning

**Definition:** A way of getting computers to perform a task by learning from examples rather than by following hand-coded rules. Arthur Samuel (1949) framed it as automatically adjusting a model's **weights** to improve its **performance**.

## Example
```python
# Traditional programming: you write the rules.
def is_even(n): return n % 2 == 0

# Machine learning: you provide examples; training discovers the weights.
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)   # weights are learned from labelled images
```

**Related Terms:** Weights, Neural Network, Loss

- Replaces explicit rules with learned parameters.
- Needs labelled examples (for supervised learning).
- Improves via a feedback loop on measured performance.

---

### Weights (Parameters)

**Definition:** The internal numbers of a model that determine how inputs are transformed into outputs. Training is the process of finding good weight values.

## Example
```python
# Weights live inside the model; you rarely touch them directly.
learn = vision_learner(dls, resnet34, metrics=error_rate)
n_params = sum(p.numel() for p in learn.model.parameters())
print(f"resnet34 has {n_params:,} weights to tune")
```

**Related Terms:** Machine Learning, Learning Rate, Neural Network

- Also called *parameters*.
- Updated by gradient descent using the learning rate.
- Pretrained weights encode reusable knowledge.

---

### Neural Network

**Definition:** A model composed of layers of simple operations plus nonlinearities. With enough weights it can approximate essentially any function (universal approximation theorem).

## Example
```python
learn = vision_learner(dls, resnet34, metrics=error_rate)
print(learn.model)   # inspect the layered architecture
```

**Related Terms:** ResNet, Weights, Transfer Learning

- Flexibility comes from many tunable weights.
- The *same* architecture can learn very different tasks.
- CNNs are neural networks specialized for images.

---

### Transfer Learning

**Definition:** Taking a model trained on one (large) task and adapting it to a different (usually smaller) task. Early layers keep their general features; later layers are retrained.

## Example
```python
# The pretrained ImageNet body is reused; only the head is new.
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)
```

**Related Terms:** Pretrained Model, fine_tune, vision_learner

- Enables strong results from small datasets.
- Dramatically reduces training time and data needs.
- The default and recommended approach in fastai.

---

### Pretrained Model

**Definition:** A model whose weights have already been learned on a large benchmark dataset (e.g. ImageNet). It serves as the starting point for transfer learning.

## Example
```python
# pretrained=True is the default for vision_learner
learn = vision_learner(dls, resnet34, pretrained=True, metrics=error_rate)
```

**Related Terms:** Transfer Learning, ResNet, Learner

- Downloaded automatically on first use.
- Knows generic features: edges, textures, shapes.
- `pretrained=False` forces training from scratch (rarely wanted).

---

### ResNet

**Definition:** "Residual Network" — a family of convolutional neural network architectures using skip connections. Variants are named by depth: `resnet18`, `resnet34`, `resnet50`, `resnet101`, `resnet152`.

## Example
```python
learn18 = vision_learner(dls, resnet18, metrics=error_rate)  # fast, lighter
learn50 = vision_learner(dls, resnet50, metrics=error_rate)  # slower, stronger
```

**Related Terms:** Neural Network, Pretrained Model, vision_learner

- `resnet34` balances speed and accuracy for Lesson 1.
- Deeper variants often score better but train slower.
- Available pretrained on ImageNet.

---

### DataLoaders

**Definition:** A fastai object that holds a training `DataLoader` and a validation `DataLoader`. It handles labelling, splitting, transforming, and batching your data.

## Example
```python
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path),
    valid_pct=0.2, seed=42,
    label_func=is_cat, item_tfms=Resize(224),
)
dls.show_batch(max_n=6)
```

**Related Terms:** Learner, Validation Set, Epoch

- Plural: bundles both train and valid loaders.
- Serves the model batches, not single items.
- Built by factory methods (`from_name_func`, `from_folder`, `from_df`).

---

### Learner

**Definition:** The central fastai object that combines `DataLoaders`, a model architecture, a loss function, and metrics, and exposes training methods (`fit`, `fine_tune`) and inference (`predict`).

## Example
```python
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)
learn.predict("pet.jpg")
```

**Related Terms:** vision_learner, DataLoaders, Loss vs Metric

- One object owns data, model, optimizer, and callbacks.
- `learn.validate()` reports validation metrics.
- `learn.export()` saves it for deployment.

---

### vision_learner

**Definition:** The constructor that builds a computer-vision `Learner` from `DataLoaders` and an architecture. It replaces the older `cnn_learner` name.

## Example
```python
learn = vision_learner(dls, resnet34, metrics=error_rate)
# Equivalent to the deprecated: cnn_learner(dls, resnet34, metrics=error_rate)
```

**Related Terms:** Learner, ResNet, Transfer Learning

- Attaches a new, correctly-sized head to a pretrained body.
- `metrics=` accepts one or a list of metrics.
- `cnn_learner` still exists as a deprecated alias.

---

### fine_tune

**Definition:** A `Learner` method implementing the standard transfer-learning schedule: first train only the new head with the pretrained body frozen, then unfreeze all layers and train them at a lower learning rate.

## Example
```python
learn.fine_tune(2)                 # 1 frozen epoch + 2 unfrozen epochs
learn.fine_tune(4, base_lr=1e-3)   # control the learning rate
```

**Related Terms:** Epoch, Learning Rate, Transfer Learning

- Different from `fit_one_cycle`, which trains without the freeze phase.
- `freeze_epochs` defaults to 1.
- The go-to method when starting from a pretrained model.

---

### Epoch

**Definition:** One complete pass of the training set through the model. Training usually runs for several epochs.

## Example
```python
learn.fine_tune(3)   # 3 fine-tuning epochs (plus 1 frozen)
```

**Related Terms:** fine_tune, Overfitting, Learning Rate

- Metrics are reported once per epoch.
- Too many epochs can cause overfitting.
- Each epoch is made of many mini-batches.

---

### Learning Rate

**Definition:** The size of the step taken when updating weights during training. It is the most important hyperparameter to get roughly right.

## Example
```python
learn.lr_find()               # suggest a good learning rate
learn.fine_tune(2, base_lr=2e-3)
```

**Related Terms:** Weights, Epoch, fine_tune

- Too high: training diverges or oscillates.
- Too low: training is slow and may underfit.
- `lr_find()` helps pick a sensible value.

---

### Loss vs Metric

**Definition:** The **loss** is the differentiable quantity the optimizer minimizes (fastai chooses it automatically, e.g. cross-entropy). A **metric** is a human-readable score you monitor (e.g. `error_rate`) and it does not drive optimization.

## Example
```python
# error_rate is a METRIC; the loss (cross-entropy) is set for you.
learn = vision_learner(dls, resnet34, metrics=[error_rate, accuracy])
```

**Related Terms:** error_rate, Learner, Validation Set

- Loss must be smooth/differentiable; metrics need not be.
- Metrics can be a list.
- Only the loss affects weight updates.

---

### Validation Set

**Definition:** A portion of the data held out from training and used only to measure performance on unseen examples. fastai always creates one.

## Example
```python
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path),
    valid_pct=0.2, seed=42,          # 20% held out, reproducibly
    label_func=is_cat, item_tfms=Resize(224),
)
```

**Related Terms:** Overfitting, DataLoaders, error_rate

- Never used to update weights.
- Metrics reported during training come from it.
- A fixed `seed` makes the split reproducible.

---

### Overfitting

**Definition:** When a model learns the training data too specifically — including its noise — and therefore performs worse on new data. Detected when validation error rises while training loss keeps falling.

## Example
```python
# Symptom across epochs: train_loss keeps dropping,
# valid_loss / error_rate start increasing -> overfitting.
learn.fine_tune(1)   # start small to avoid it
```

**Related Terms:** Validation Set, Epoch, error_rate

- The central problem in machine learning.
- Combat it with a validation set, fewer epochs, more data, or augmentation.
- Good training accuracy alone proves nothing.

---

### error_rate

**Definition:** A metric giving the fraction of validation examples the model classifies incorrectly. `accuracy = 1 - error_rate`.

## Example
```python
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)
# e.g. error_rate=0.0087 means ~99.13% accuracy
```

**Related Terms:** Loss vs Metric, Accuracy, Validation Set

- Lower is better.
- Computed on the validation set.
- Reported once per epoch during training.

## Summary

1. **Machine learning** learns **weights** from data instead of hand-written rules, following Samuel's inputs→results→performance→update loop.
2. **Neural networks** (like **ResNet**) are flexible function approximators; **transfer learning** from a **pretrained** model gets strong results on small data.
3. **DataLoaders** feed batched train/validation data to a **Learner** built by **vision_learner**; **fine_tune** runs the transfer-learning schedule over several **epochs** at a chosen **learning rate**.
4. You optimize a **loss** but judge quality with a **metric** like **error_rate**, always on a held-out **validation set** to catch **overfitting**.

**Next:** See Lecture 02 — Deployment & the fastai Stack.
