# Lecture 02: Deployment & the fastai Stack

## Topic Overview

This lecture is fast.ai's "how to build and ship a model" lesson. In Lecture 01
you trained a working image classifier in a handful of lines. Now you learn how
that magic is assembled: the **`DataBlock`** API that turns raw files into
batched, augmented `DataLoaders`; the counter-intuitive fast.ai workflow of
**cleaning your data *with* a trained model** instead of before it; and how to
**export a `Learner`**, run **inference** on a single image, and wrap it in a
**Gradio** web app you can host for free on **Hugging Face Spaces**.

Along the way you meet the ideas that separate a demo from a product: the
**drivetrain approach** to designing ML systems, and the deployment risks of
**out-of-domain data** and **domain shift**.

**Duration:** 2-3 hours
**Difficulty:** Beginner-Intermediate
**Prerequisites:** Lecture 01

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Construct** a `DataBlock` from `blocks`, `get_items`, `splitter`, `get_y`, `item_tfms`, and `batch_tfms`, then call `.dataloaders(path)`.
2. **Distinguish** `item_tfms` (per-image, on CPU) from `batch_tfms` (per-batch, on GPU) and explain presizing.
3. **Explain** why `RandomResizedCrop` and `aug_transforms` improve generalization through data augmentation.
4. **Gather** your own image dataset and **clean it with the model** using `plot_top_losses` and `ImageClassifierCleaner`.
5. **Export** a trained `Learner` to a pickle and **reload** it with `load_learner` for inference.
6. **Predict** the class of a single image with `learn.predict` and interpret the returned tuple.
7. **Build and launch** a Gradio `Interface` that serves your exported model, and describe hosting it on Hugging Face Spaces.
8. **Apply** the drivetrain approach and reason about out-of-domain data and domain shift when deploying.

---

## Key Concepts

### 1. The DataBlock API

A `DataBlock` is a *blueprint*, not the data itself. It declares how to go from
raw sources to model-ready tensors, and stays independent of any particular
folder. You feed it a source with `.dataloaders(path)` to get `DataLoaders`.

```python
from fastai.vision.all import *

dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock),   # x is an image, y is a category
    get_items=get_image_files,            # how to list inputs
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,                   # label = parent folder name
    item_tfms=Resize(460),                # per-item, CPU
    batch_tfms=aug_transforms(size=224, min_scale=0.75),  # per-batch, GPU
).dataloaders(path, bs=64)

dls.show_batch(max_n=9)
```

Each argument answers one question:

```
raw path ──get_items──▶ list of files
                          │
                          ├─ get_y ─────▶ labels (dependent variable y)
                          ├─ blocks ────▶ typed transforms (Image / Category)
                          ├─ splitter ──▶ train set + validation set
                          ├─ item_tfms ─▶ make every item the same size (CPU)
                          └─ batch_tfms ▶ augment a whole batch at once (GPU)
                          ▼
                     DataLoaders (train_dl + valid_dl)
```

### 2. DataLoaders: what .dataloaders() returns

`DataLoaders` bundles a **training** `DataLoader` and a **validation**
`DataLoader`. It is what you hand to a learner. Inspect it before training so
you catch label or sizing bugs early.

```python
dls.train.show_batch(max_n=4, nrows=1)  # augmented training images
dls.valid.show_batch(max_n=4, nrows=1)  # validation images (no random aug)
print(dls.vocab)                        # the ordered list of class names
len(dls.train_ds), len(dls.valid_ds)    # item counts per split
```

`dls.vocab` is the mapping between the integer the model predicts and the human
label — you will use it again at inference time.

### 3. item_tfms vs batch_tfms and presizing

The two transform stages run in different places for different reasons.
`item_tfms` runs on the **CPU**, one image at a time, and its main job is to make
every image the **same size** so they can be collated into a batch.
`batch_tfms` runs on the **GPU**, on the whole batch at once, which is where fast
augmentation belongs.

**Presizing** is fast.ai's two-step trick: first resize items to a *larger*
square (e.g. 460), then on the GPU do the augment-and-crop down to the final
size (e.g. 224). Doing the destructive resize once, large, avoids the blurry
edges and repeated interpolation you get from many small transforms.

```python
# Presizing: big on CPU, augment + shrink on GPU
item_tfms  = Resize(460)                               # step 1 (CPU)
batch_tfms = aug_transforms(size=224, min_scale=0.75)  # step 2 (GPU)
```

```
CPU:  [varied sizes] ─Resize(460)─▶ [460x460]  (uniform, over-sized)
GPU:  [460x460] ─aug_transforms(size=224)─▶ [224x224]  (rotate/warp/crop/flip)
```

### 4. RandomResizedCrop and data augmentation

`RandomResizedCrop` grabs a *different* random region of each image every epoch
and scales it to the target size. The model therefore never sees exactly the
same picture twice, which fights overfitting. `min_scale` sets how much of the
original the crop must cover.

**Data augmentation** is the broader family of label-preserving perturbations —
rotation, warp, brightness/contrast, and flips — that `aug_transforms` bundles
with sensible defaults.

```python
item_tfms = RandomResizedCrop(224, min_scale=0.3)  # aggressive random crops
batch_tfms = aug_transforms(mult=1.0)              # rotate/warp/light/flip

# Visualize the SAME image augmented 4 different ways:
dls.train.show_batch(max_n=4, nrows=1, unique=True)
```

Augment the training set only; the validation set uses a plain center crop so
metrics stay comparable across epochs.

### 5. Clean your data WITH the model (not before)

The signature fast.ai insight of this lesson: **train a quick model first, then
let it tell you which data is bad.** A partly-trained model's biggest losses are
concentrated on mislabeled, ambiguous, or junk images — exactly what you want to
find. Cleaning by hand *before* modeling wastes effort on data the model handles
fine anyway.

```python
learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(2)                       # a quick first pass is enough

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_top_losses(5, nrows=1)       # the model's most confident mistakes
```

```
train quick model ─▶ find highest-loss items ─▶ relabel / delete ─▶ retrain
        ▲                                                              │
        └──────────────────────  iterate  ◀───────────────────────────┘
```

### 6. plot_top_losses and ImageClassifierCleaner

`plot_top_losses` shows the images the model got most wrong *and* was most
confident about. `ImageClassifierCleaner` turns that into an interactive GUI:
for each image you choose **Keep**, a **new label**, or **Delete**. The widget
never edits files itself — it records your choices, and you apply them.

```python
from fastai.vision.widgets import ImageClassifierCleaner

cleaner = ImageClassifierCleaner(learn)
cleaner  # renders dropdowns per image in the notebook

# Apply the decisions the widget recorded:
for idx in cleaner.delete():
    cleaner.fns[idx].unlink()
for idx, cat in cleaner.change():
    shutil.move(str(cleaner.fns[idx]), path / cat)
```

### 7. Export, load_learner, and inference

Training and serving are separate worlds. `learn.export()` pickles the model
**and** its inference-time transforms (the `DataLoaders` pipeline) into one
`.pkl`. In production you call `load_learner` — no training code, no GPU
required — and `predict` on new inputs.

```python
learn.export("model.pkl")               # writes to learn.path/model.pkl

# ... later, in a totally separate process / server ...
inf = load_learner("model.pkl")
pred_class, pred_idx, probs = inf.predict("unknown.jpg")
print(pred_class)                        # e.g. 'grizzly'
print(probs[pred_idx].item())            # confidence for that class
```

`predict` returns a 3-tuple: the **label string**, the **index into the vocab**,
and the **full probability tensor** over every class.

### 8. The drivetrain approach and deployment risk

Before writing code, fast.ai asks you to design the *product* with the
**drivetrain approach**: state the **objective**, identify the **levers** you can
actually pull, list the **data** you can collect, and only then build the
**models** that connect levers to objective.

```
OBJECTIVE ─▶ LEVERS (controllable actions) ─▶ DATA ─▶ MODELS
   "what outcome do we want?"     "what can we change?"    "what predicts the outcome?"
```

Two risks dominate deployment. **Out-of-domain data** is input unlike anything in
training (a night photo for a daytime-trained classifier), where predictions are
meaningless yet confident. **Domain shift** is the slower version: the world
drifts away from your training distribution over time, so accuracy silently
decays. Mitigate with a human-in-the-loop rollout and ongoing monitoring.

---

## Code Examples

### Example 1: A complete DataBlock -> train -> clean loop

```python
from fastai.vision.all import *

# Assume `path` holds subfolders per class, e.g. path/grizzly, path/black, path/teddy
bears = DataBlock(
    blocks=(ImageBlock, CategoryBlock),          # inputs are images, targets categories
    get_items=get_image_files,                   # recursively collect image paths
    splitter=RandomSplitter(valid_pct=0.2, seed=42),  # reproducible 80/20 split
    get_y=parent_label,                          # label from the containing folder
    item_tfms=Resize(460),                       # presize step 1 (CPU, uniform size)
    batch_tfms=aug_transforms(size=224, min_scale=0.75),  # step 2 (GPU augment+crop)
)

dls = bears.dataloaders(path, bs=32)             # build the DataLoaders
dls.show_batch(max_n=6)                          # sanity-check images + labels

learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(4)                               # quick baseline model

# Use the model to surface bad data
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()                   # where classes get confused
interp.plot_top_losses(6, nrows=2)               # most-confident mistakes -> likely noise
```

### Example 2: Export and single-image inference

```python
from fastai.vision.all import load_learner
from pathlib import Path

# --- training side (run once, on a GPU box) ---
learn.export("bear_classifier.pkl")              # bundles model + transforms

# --- serving side (CPU is fine, no fastai training imports needed) ---
def classify_image(img_path: str) -> dict[str, float]:
    """Return a {class_name: probability} dict for one image."""
    inf = load_learner("bear_classifier.pkl")
    pred, idx, probs = inf.predict(img_path)
    # zip the vocab against the probability tensor for a readable result
    return {cls: float(p) for cls, p in zip(inf.dls.vocab, probs)}

print(classify_image("mystery_bear.jpg"))
# {'black': 0.02, 'grizzly': 0.95, 'teddy': 0.03}
```

### Example 3: A Gradio app served from the exported model

```python
import gradio as gr
from fastai.vision.all import load_learner
from PIL import Image

learn = load_learner("bear_classifier.pkl")      # load once at startup
labels = learn.dls.vocab

def predict(img: Image.Image) -> dict[str, float]:
    """Gradio passes a PIL image; return label->confidence for gr.Label."""
    _, _, probs = learn.predict(img)
    return {labels[i]: float(probs[i]) for i in range(len(labels))}

demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),                 # matches the PIL arg above
    outputs=gr.Label(num_top_classes=3),         # shows top-3 with bars
    title="Bear Classifier",
    examples=["grizzly.jpg", "black.jpg", "teddy.jpg"],
)

if __name__ == "__main__":
    demo.launch()   # local server; on Hugging Face Spaces, Spaces runs this for you
```

---

## Common Mistakes to Avoid

```python
# ❌ BAD: heavy augmentation as an item_tfm — runs slowly on the CPU per image
block = DataBlock(item_tfms=aug_transforms(size=224))  # wrong stage!

# ✅ GOOD: uniform resize on CPU, augment on the GPU in batch_tfms
block = DataBlock(item_tfms=Resize(460),
                  batch_tfms=aug_transforms(size=224, min_scale=0.75))
```

```python
# ❌ BAD: hand-clean every image before you have any model to guide you
#   (slow, subjective, and wasted on data the model already handles)
clean_all_images_manually(path)   # then train

# ✅ GOOD: train a quick model, then clean the images it fails on
learn.fine_tune(2)
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_top_losses(5)         # relabel/delete only these, then retrain
```

```python
# ❌ BAD: re-load the learner on every request inside the predict function
def predict(img):
    learn = load_learner("model.pkl")   # unpickles from disk every call — slow
    return learn.predict(img)

# ✅ GOOD: load once at startup, reuse the in-memory learner
learn = load_learner("model.pkl")
def predict(img):
    return learn.predict(img)
```

---

## Best Practices

1. Keep the `DataBlock` (blueprint) separate from the data source; pass the path only in `.dataloaders(path)`.
2. Always `show_batch` and check `dls.vocab` before training to catch label/sizing bugs early.
3. Set `seed=` in `RandomSplitter` for reproducible validation splits.
4. Presize: `Resize` large in `item_tfms`, then `aug_transforms(size=...)` in `batch_tfms`.
5. Augment training data only; leave the validation set on a plain center crop.
6. Train a quick baseline before cleaning — let `plot_top_losses` find the noisy data for you.
7. Treat `ImageClassifierCleaner` output as a record of decisions; apply deletes/moves explicitly.
8. `export()` for deployment; it bundles the transform pipeline so serving matches training.
9. Load the learner once at app startup, never per request.
10. Design with the drivetrain approach and monitor for out-of-domain inputs and domain shift after launch.

---

## Practice Exercises

### Exercise 1
Build a `DataBlock` for a 3-class image dataset using `ImageBlock`/`CategoryBlock`,
`get_image_files`, a seeded `RandomSplitter(0.2)`, `parent_label`, `Resize(460)`,
and `aug_transforms(size=224)`. Call `.dataloaders(path)` and `show_batch`.

### Exercise 2
Take one image and call `dls.train.show_batch(unique=True)` to display four
different augmentations of it. Then swap `item_tfms` to
`RandomResizedCrop(224, min_scale=0.3)` and compare.

### Exercise 3
Fine-tune a `resnet18` for 2 epochs, build a
`ClassificationInterpretation`, and use `plot_top_losses(6)` to identify at least
two likely-mislabeled images. Describe how you would fix them.

### Exercise 4
Export the trained learner, reload it with `load_learner` in a fresh
interpreter, and write a `classify_image(path)` function that returns a
`{class: probability}` dictionary using `dls.vocab`.

### Exercise 5
Wrap your loaded learner in a `gr.Interface` with `gr.Image(type="pil")` input
and `gr.Label(num_top_classes=3)` output. Launch it locally, then outline the
steps to host it on Hugging Face Spaces.

---

## Summary

1. A **`DataBlock`** is a reusable blueprint (`blocks`, `get_items`, `splitter`, `get_y`, `item_tfms`, `batch_tfms`) that produces **`DataLoaders`** via `.dataloaders(path)`.
2. **`item_tfms`** run per-image on the CPU (mainly `Resize` for uniform size); **`batch_tfms`** run per-batch on the GPU (augmentation) — the two together implement **presizing**.
3. **`RandomResizedCrop`** and **`aug_transforms`** provide data augmentation that reduces overfitting; augment training data only.
4. Clean data **with** the model: train a quick baseline, then use **`plot_top_losses`** and **`ImageClassifierCleaner`** to find and fix noisy labels.
5. **`learn.export()`** pickles model + transforms; **`load_learner`** + **`predict`** run inference anywhere, returning `(label, index, probs)`.
6. A **Gradio** `gr.Interface` serves the exported learner as a web app, hostable free on **Hugging Face Spaces**.
7. Use the **drivetrain approach** to design ML products and watch for **out-of-domain data** and **domain shift** in production.

**Next lecture:** Lecture 03 — Neural Net Foundations & Stochastic Gradient Descent (SGD): building the learning machinery from scratch.
