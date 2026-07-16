# Lecture 01: Getting Started

## Topic Overview

fast.ai teaches deep learning **top-down**: you train a working, state-of-the-art image classifier in the first few minutes, then peel back the layers to understand *why* it works. This lecture builds a cats-vs-dogs classifier with the `fastai` library, introduces the machine-learning feedback loop that Arthur Samuel described in 1949, and explains how transfer learning lets you get great results from tiny datasets. By the end you will have run a real model, measured its error, and inspected its mistakes.

**Duration:** 2-3 hours
**Difficulty:** Beginner
**Prerequisites:** Basic Python (functions, imports), comfort with the command line, and a Jupyter/Kaggle/Colab environment. No prior deep-learning or math background required.

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the fast.ai top-down teaching philosophy and why you train a model before studying theory.
2. **Contrast** machine learning with traditional programming using Arthur Samuel's weights/performance feedback loop.
3. **Describe** transfer learning and why it makes training on small datasets practical.
4. **Build** a `DataLoaders` object from a labelled image folder using `ImageDataLoaders.from_name_func`.
5. **Train** an image classifier with `vision_learner`, a pretrained `resnet34`, and `fine_tune`.
6. **Evaluate** a model using `error_rate`, `learn.predict`, and a confusion matrix from `ClassificationInterpretation`.
7. **Define** overfitting and explain why fastai always holds out a validation set.
8. **Recognize** that vision, text, tabular, and collaborative-filtering problems share the same fastai workflow.

## Key Concepts

### 1. The Top-Down Teaching Method

Traditional courses start with theory (linear algebra, calculus, gradient descent) and make you wait weeks before touching a real model. fast.ai inverts this: you **train a model in minutes**, see it work, and let curiosity pull you into the details. The mantra is *"train first, understand later."*

```python
# The entire "hello world" of deep learning with fastai.
# Fewer than 10 lines produces a >99% accurate cat/dog classifier.
from fastai.vision.all import *

path = untar_data(URLs.PETS) / "images"

def is_cat(fname: str) -> bool:
    # In the Oxford-IIIT Pets dataset, cat breeds start with an uppercase letter.
    return fname[0].isupper()

dls = ImageDataLoaders.from_name_func(
    path,
    get_image_files(path),
    valid_pct=0.2,
    seed=42,
    label_func=is_cat,
    item_tfms=Resize(224),
)

learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)
```

The philosophy: motivation and context first, foundations second. You learn *deeply* about the parts you actually used.

### 2. Machine Learning vs Traditional Programming

In **traditional programming** a human writes explicit rules: `inputs → program → results`. For hard problems (recognizing a cat) nobody can write those rules by hand.

**Machine learning** replaces the fixed program with a *model* whose behavior is controlled by **weights** (also called parameters). Arthur Samuel (1949) framed it as a feedback loop: adjust the weights automatically based on how well the model performs.

```
        ┌─────────────────────────────────────────────┐
        │                                             │
        ▼                                             │
   ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌───────────┐
   │ inputs  │───▶│  model   │───▶│ results │───▶│performance│
   └─────────┘    └──────────┘    └─────────┘    └───────────┘
                       ▲                               │
                       │                               │
                   ┌───────┐                           │
                   │weights│◀──────────────────────────┘
                   └───────┘        (update weights)
```

- **inputs + weights → model → results**: the model maps inputs to predictions using its current weights.
- **results → performance**: a measure of how good the predictions are.
- **performance → update weights**: an automatic mechanism (gradient descent) nudges the weights to improve performance.

```python
# Conceptual pseudocode of Samuel's loop.
def train_step(inputs, targets, weights):
    results = model(inputs, weights)          # inputs + weights -> results
    performance = loss(results, targets)      # measure how good
    weights = update(weights, performance)    # improve the weights
    return weights
```

### 3. Neural Networks and Why They Are Flexible

A **neural network** is a particular kind of model that, given enough weights, can approximate *any* function (the universal approximation theorem). That flexibility is why the *same* architecture can learn cats-vs-dogs, tumor detection, or handwriting — only the weights differ after training.

```
Input image ─▶ [layer 1] ─▶ [layer 2] ─▶ ... ─▶ [layer n] ─▶ prediction
                  each layer = weights + a simple nonlinearity
```

You do not design the weights; **training** discovers them by repeatedly running Samuel's loop over your labelled examples.

### 4. Transfer Learning

Training a network from scratch needs millions of images and huge compute. **Transfer learning** sidesteps this: start from a model already trained on a large dataset (ImageNet, ~1.3M images), then adapt it to your task. The early layers already know generic features (edges, textures, shapes); you only need to re-teach the final layers your specific classes.

```python
# resnet34 arrives PRETRAINED on ImageNet.
# vision_learner downloads those weights and swaps in a fresh "head"
# sized for YOUR number of classes.
learn = vision_learner(dls, resnet34, metrics=error_rate)

# fine_tune() runs two phases:
#   1. freeze the pretrained body, train only the new head for 1 epoch
#   2. unfreeze everything and train all layers at a lower learning rate
learn.fine_tune(epochs=1)
```

This is why you can hit 99% accuracy on a few thousand images in a minute: you are standing on the shoulders of a model that already learned to see.

### 5. DataLoaders: Getting Data Into the Model

Models train on **batches** of data, not one image at a time. A `DataLoaders` bundles a *training* `DataLoader` and a *validation* `DataLoader`, handling labelling, splitting, resizing, and batching.

```python
dls = ImageDataLoaders.from_name_func(
    path,                       # root folder of images
    get_image_files(path),     # list of image paths
    valid_pct=0.2,             # hold out 20% for validation
    seed=42,                   # reproducible split
    label_func=is_cat,         # how to derive a label from a filename
    item_tfms=Resize(224),     # resize every item to 224x224
    bs=64,                     # batch size (images per step)
)

dls.show_batch(max_n=6)        # sanity-check your data + labels visually
```

`ImageDataLoaders` is a high-level factory. Under the hood it uses the flexible **DataBlock** API, which you will meet in a later lecture.

### 6. Learner and fine_tune

A `Learner` ties together three things: the `DataLoaders`, the model architecture, and a **loss function**, plus the **metrics** you want reported. `vision_learner` is the convenience constructor for computer-vision `Learner`s.

```python
learn = vision_learner(
    dls,
    resnet34,               # architecture (18/34/50/101/152 variants exist)
    metrics=error_rate,     # human-readable score, printed each epoch
)

learn.fine_tune(2)          # transfer-learning training schedule
```

Two terms that are easy to confuse:
- **Loss**: what the optimizer minimizes; must be smoothly differentiable (e.g. cross-entropy). Chosen automatically by fastai.
- **Metric**: what *you* read to judge quality (e.g. `error_rate`, `accuracy`). It does not affect training.

One full pass over all training data is one **epoch**. `fine_tune(2)` does 1 frozen epoch + 2 unfrozen epochs by default.

### 7. Making and Interpreting Predictions

Once trained, ask the model about a new image with `learn.predict`, and inspect systematic mistakes with `ClassificationInterpretation`.

```python
# Single-image prediction
pred_class, pred_idx, probs = learn.predict("mystery_pet.jpg")
print(f"Prediction: {pred_class}; confidence: {probs[pred_idx]:.4f}")

# Where does the model go wrong?
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix(figsize=(6, 6))
interp.plot_top_losses(9)   # the 9 most confidently-wrong images
```

`learn.predict` returns a triple: the decoded label, its index, and the full probability tensor across classes.

### 8. Overfitting and the Validation Set

**Overfitting** is when a model memorizes the training data instead of learning general patterns — it scores well on data it has seen and poorly on new data. This is the single most important failure mode in machine learning.

```
error
  │                              ╭─ validation error (starts rising = overfitting)
  │  ╲                          ╱
  │   ╲___                _____╱
  │       ╲______________╱      ╲___ training error (keeps falling)
  └──────────────────────────────────▶ epochs
```

fastai **always** holds out a validation set (`valid_pct=0.2` above) and reports metrics on it, so the number you see reflects performance on *unseen* data. You never tune against the training error alone.

```python
# The validation split is not optional in fastai — it is baked in.
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path),
    valid_pct=0.2,   # 20% held out and NEVER trained on
    seed=42,
    label_func=is_cat,
    item_tfms=Resize(224),
)
```

## Code Examples

### Example 1: Full Cats-vs-Dogs Pipeline

```python
"""
End-to-end image classifier on the Oxford-IIIT Pets dataset.
Faithful to the fastai 2.7.x API.
"""
from fastai.vision.all import *


def build_pet_dls(seed: int = 42, img_size: int = 224, bs: int = 64) -> DataLoaders:
    """Download PETS and build a cat-vs-dog DataLoaders."""
    path = untar_data(URLs.PETS) / "images"

    def is_cat(fname: str) -> bool:
        # Cat breeds in this dataset use a leading uppercase letter.
        return fname[0].isupper()

    return ImageDataLoaders.from_name_func(
        path,
        get_image_files(path),
        valid_pct=0.2,
        seed=seed,
        label_func=is_cat,
        item_tfms=Resize(img_size),
        bs=bs,
    )


def train_classifier(dls: DataLoaders, epochs: int = 1) -> Learner:
    """Create a pretrained ResNet learner and fine-tune it."""
    learn = vision_learner(dls, resnet34, metrics=error_rate)
    learn.fine_tune(epochs)
    return learn


if __name__ == "__main__":
    dls = build_pet_dls()
    dls.show_batch(max_n=6)          # visual sanity check
    learn = train_classifier(dls, epochs=1)

    # Report final validation metric
    loss, err = learn.validate()
    print(f"Validation loss={loss:.4f}  error_rate={err:.4f}  accuracy={1 - err:.4%}")
```

### Example 2: Predict and Interpret

```python
"""
Use a trained Learner to predict on a new image and inspect mistakes.
"""
from fastai.vision.all import *


def predict_one(learn: Learner, image_path: str) -> None:
    """Print the model's prediction and confidence for a single image."""
    pred_class, pred_idx, probs = learn.predict(image_path)
    confidence = probs[pred_idx].item()
    print(f"{image_path} -> {pred_class} ({confidence:.2%} confident)")


def inspect_errors(learn: Learner, k: int = 9) -> ClassificationInterpretation:
    """Plot the confusion matrix and the k most confident mistakes."""
    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix(figsize=(6, 6))
    interp.plot_top_losses(k, nrows=3)
    return interp


if __name__ == "__main__":
    # Assumes `learn` was trained as in Example 1 and an image is available.
    # predict_one(learn, "some_pet.jpg")
    # interp = inspect_errors(learn)
    pass
```

### Example 3: The Same Four Lines, Four Domains

```python
"""
fastai gives every domain a nearly identical high-level workflow:
build DataLoaders -> build Learner -> fine_tune / fit.
"""
# --- Vision (segmentation) ---------------------------------------------
from fastai.vision.all import *
camvid = untar_data(URLs.CAMVID_TINY)
dls_seg = SegmentationDataLoaders.from_label_func(
    camvid, bs=8,
    fnames=get_image_files(camvid / "images"),
    label_func=lambda o: camvid / "labels" / f"{o.stem}_P{o.suffix}",
    codes=np.loadtxt(camvid / "codes.txt", dtype=str),
)
learn_seg = unet_learner(dls_seg, resnet34)
# learn_seg.fine_tune(8)

# --- Text (sentiment) --------------------------------------------------
from fastai.text.all import *
imdb = untar_data(URLs.IMDB)
dls_txt = TextDataLoaders.from_folder(imdb, valid="test")
learn_txt = text_classifier_learner(dls_txt, AWD_LSTM, metrics=accuracy)
# learn_txt.fine_tune(4, 1e-2)

# --- Tabular -----------------------------------------------------------
from fastai.tabular.all import *
adult = untar_data(URLs.ADULT_SAMPLE)
dls_tab = TabularDataLoaders.from_csv(
    adult / "adult.csv", path=adult, y_names="salary",
    cat_names=["workclass", "education", "marital-status"],
    cont_names=["age", "fnlwgt", "education-num"],
    procs=[Categorify, FillMissing, Normalize],
)
learn_tab = tabular_learner(dls_tab, metrics=accuracy)
# learn_tab.fit_one_cycle(3)

# --- Collaborative filtering ------------------------------------------
from fastai.collab import *
ratings = pd.read_csv(untar_data(URLs.ML_SAMPLE) / "ratings.csv")
dls_collab = CollabDataLoaders.from_df(ratings, bs=64)
learn_collab = collab_learner(dls_collab, y_range=(0.5, 5.5))
# learn_collab.fine_tune(10)
```

## Common Mistakes to Avoid

### Mistake 1: Judging the Model on Training Data

```python
# ❌ BAD: measuring on data the model trained on hides overfitting
learn.fine_tune(20)                 # train a lot
preds, _ = learn.get_preds(dl=dls.train)   # peeking at TRAINING data
# "Wow, 100% accuracy!" — meaningless, the model memorized these.

# ✅ GOOD: always evaluate on the held-out validation set
learn.fine_tune(1)
loss, err = learn.validate()        # uses the validation DataLoader
print(f"validation error_rate={err:.4f}")
```

### Mistake 2: Skipping the Validation Split

```python
# ❌ BAD: no validation set -> no way to detect overfitting
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path), valid_pct=0.0,   # everything is training
    label_func=is_cat, item_tfms=Resize(224),
)

# ✅ GOOD: hold out a reproducible validation set
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path), valid_pct=0.2, seed=42,
    label_func=is_cat, item_tfms=Resize(224),
)
```

### Mistake 3: Training From Scratch Instead of Fine-Tuning

```python
# ❌ BAD: throwing away pretrained knowledge, then wondering why it's slow/bad
learn = vision_learner(dls, resnet34, pretrained=False, metrics=error_rate)
learn.fit_one_cycle(1)              # random init needs tons of data + time

# ✅ GOOD: leverage transfer learning (pretrained=True is the default)
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)                  # adapts ImageNet features to your task
```

## Best Practices

1. **Train first, understand later** — run a working model before diving into theory.
2. Always keep a **validation set** and read metrics from it, never from training data.
3. Set a fixed `seed` so your train/valid split (and results) are reproducible.
4. Start with **transfer learning** (`pretrained=True`) and a proven architecture like `resnet34`.
5. Call `dls.show_batch()` before training to confirm images and labels line up.
6. Prefer `error_rate`/`accuracy` as human-readable **metrics**; let fastai pick the **loss**.
7. Begin with a small number of epochs (`fine_tune(1)`); increase only if validation error is still falling.
8. Watch for **overfitting**: stop when validation error stops improving even though training loss keeps dropping.
9. Use `ClassificationInterpretation` (`plot_confusion_matrix`, `plot_top_losses`) to understand failures, not just the score.
10. Use a GPU (Kaggle, Paperspace, or Colab) — CNN training on CPU is impractically slow.

## Practice Exercises

### Exercise 1: Cat-vs-Dog in Under 10 Lines
Reproduce the PETS classifier from scratch. Confirm you reach an `error_rate` below 0.05 after `fine_tune(1)`.

### Exercise 2: Breed Classification
Change the `label_func` to classify all 37 pet *breeds* (hint: `RegexLabeller(r'(.+)_\d+.jpg$')`). Compare the error rate against the binary task.

### Exercise 3: Interpret the Mistakes
Build a `ClassificationInterpretation`, plot the confusion matrix, and identify the two breeds most often confused with each other.

### Exercise 4: Try a Different Architecture
Swap `resnet34` for `resnet18` and `resnet50`. Note the trade-off between training time and error rate.

### Exercise 5: A Second Domain
Pick tabular (`ADULT_SAMPLE`) or text (`IMDB`) and get a model training with the four-line workflow. Observe how similar the code is to the vision case.

## Summary

1. fast.ai is **top-down**: you train a real, accurate model first and learn the theory as you need it.
2. Machine learning replaces hand-written rules with a **model** whose **weights** are tuned automatically via Samuel's loop: *inputs + weights → model → results → performance → update weights*.
3. **Neural networks** are flexible enough to learn almost any task; **training** finds the weights.
4. **Transfer learning** starts from a model pretrained on ImageNet, so you get excellent results from small datasets quickly — this is what `fine_tune` exploits.
5. The core fastai objects are **`DataLoaders`** (batched train + validation data), **`Learner`** (data + architecture + loss + metrics), and helpers like `vision_learner` and `resnet34`.
6. Evaluate with a **metric** (`error_rate`) on a **validation set**, predict with `learn.predict`, and diagnose with `ClassificationInterpretation`.
7. **Overfitting** is the central danger; fastai always holds out a validation set so your reported numbers reflect unseen data.
8. Vision, text, tabular, and collaborative filtering all share the same build-DataLoaders → build-Learner → fine_tune workflow.

**Next lecture:** Lecture 02 — Deployment & the fastai Stack, where you turn this trained model into a shareable application and learn how the fastai layers fit together.
