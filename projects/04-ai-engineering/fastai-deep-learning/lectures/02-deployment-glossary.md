# Glossary: Deployment & the fastai Stack

## Quick Reference Table

| Term | Definition | Key Point |
|------|------------|-----------|
| DataBlock | A blueprint describing how to turn raw sources into model-ready data | Independent of any specific path until `.dataloaders()` |
| DataLoaders | Bundle of a training and a validation `DataLoader` | What you pass to the learner; exposes `.vocab` |
| item_tfms | Per-item transforms run on the CPU | Mainly `Resize` to make items a uniform size |
| batch_tfms | Per-batch transforms run on the GPU | Where fast augmentation belongs |
| Presizing | Resize large on CPU, then augment+crop small on GPU | Avoids repeated lossy interpolation |
| RandomResizedCrop | Random region + scale crop, different each epoch | Fights overfitting; `min_scale` sets coverage |
| Data augmentation | Label-preserving perturbations of training images | `aug_transforms` bundles sensible defaults |
| RandomSplitter | Randomly splits items into train/validation | Set `seed=` for reproducibility |
| export / pickle | `learn.export()` saves model + transforms to `.pkl` | Bundles the inference pipeline |
| load_learner | Loads an exported `.pkl` for inference | No GPU or training code needed |
| inference | Predicting on new data with a trained model | `predict` returns `(label, idx, probs)` |
| Gradio | Python library for quick ML web UIs | `gr.Interface(fn, inputs, outputs)` |
| Hugging Face Spaces | Free hosting for Gradio/Streamlit apps | Runs your app from a Git repo |
| domain shift | Training and production distributions diverge over time | Causes silent accuracy decay |
| drivetrain approach | Objective -> levers -> data -> models design method | Design the product before the model |
| plot_top_losses | Shows the model's most confident mistakes | Surfaces mislabeled/noisy data |

---

## Detailed Definitions

### DataBlock

**Definition:** A declarative blueprint that specifies how to assemble a dataset —
what the inputs and targets are (`blocks`), how to find items (`get_items`), how
to split them (`splitter`), how to label them (`get_y`), and which transforms to
apply. It holds no data itself until you call `.dataloaders(source)`.

## Example
```python
from fastai.vision.all import *
block = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(460),
    batch_tfms=aug_transforms(size=224),
)
dls = block.dataloaders(path)
```

**Related Terms:** DataLoaders, item_tfms, batch_tfms, RandomSplitter

- Reusable across datasets that share the same structure.
- `blocks=(x_block, y_block)` sets the independent and dependent variable types.
- Debug construction with `block.summary(path)`.

### DataLoaders

**Definition:** An object bundling a training `DataLoader` and a validation
`DataLoader`, produced by `DataBlock.dataloaders()`. It is the data interface a
`Learner` consumes, and it carries the class vocabulary in `.vocab`.

## Example
```python
dls = block.dataloaders(path, bs=64)
dls.show_batch(max_n=9)
print(dls.vocab)              # ordered class names
len(dls.train_ds), len(dls.valid_ds)
```

**Related Terms:** DataBlock, inference, vocab

- `dls.vocab` maps predicted indices to human-readable labels.
- `bs=` controls batch size; larger uses more GPU memory.
- Always `show_batch` before training to catch label bugs.

### item_tfms vs batch_tfms

**Definition:** Two transform stages. `item_tfms` run on the **CPU**, one item at
a time, and primarily make every item the same size so items can be collated.
`batch_tfms` run on the **GPU**, on an entire batch at once, and are where
augmentation should live for speed.

## Example
```python
block = DataBlock(
    item_tfms=Resize(460),                         # CPU, per image
    batch_tfms=aug_transforms(size=224, min_scale=0.75),  # GPU, per batch
)
```

**Related Terms:** Presizing, RandomResizedCrop, data augmentation

- Uniform size is required before items can form a batch.
- Putting augmentation on the GPU keeps training fast.
- Validation items skip random augmentation.

### Presizing

**Definition:** fast.ai's two-step resizing strategy: resize each item to a
*larger* square on the CPU, then augment and crop down to the final size on the
GPU. Doing the destructive resize once, oversized, avoids the artifacts of many
small interpolations.

## Example
```python
item_tfms  = Resize(460)                               # step 1: big, CPU
batch_tfms = aug_transforms(size=224, min_scale=0.75)  # step 2: augment+crop, GPU
```

**Related Terms:** item_tfms, batch_tfms, RandomResizedCrop

- Larger intermediate size preserves detail near the edges.
- Combines the two-stage transform pipeline into one coherent idea.
- Standard in fast.ai vision recipes.

### RandomResizedCrop

**Definition:** A transform that selects a random sub-region of an image, at a
random scale, and resizes it to the target dimensions — producing a different
view of each image every epoch.

## Example
```python
item_tfms = RandomResizedCrop(224, min_scale=0.3)
dls.train.show_batch(max_n=4, nrows=1, unique=True)  # same image, 4 crops
```

**Related Terms:** data augmentation, Presizing, batch_tfms

- `min_scale` sets the minimum fraction of the original that a crop must cover.
- The model never sees the exact same picture twice, reducing overfitting.
- Validation uses a deterministic center crop instead.

### Data augmentation

**Definition:** The technique of applying label-preserving random
transformations — rotation, warp, brightness/contrast changes, flips, zoom — to
training data so the model generalizes better. `aug_transforms` packages a
sensible default set.

## Example
```python
batch_tfms = aug_transforms(mult=1.0, do_flip=True, max_rotate=10.0)
```

**Related Terms:** RandomResizedCrop, batch_tfms

- Applied to the training set only.
- `mult` scales the intensity of all augmentations at once.
- More augmentation helps small datasets most.

### RandomSplitter

**Definition:** A splitter that randomly partitions items into a training set and
a validation set by a given validation percentage.

## Example
```python
splitter = RandomSplitter(valid_pct=0.2, seed=42)
```

**Related Terms:** DataBlock, DataLoaders

- Pass `seed=` for a reproducible split across runs.
- Alternatives include `GrandparentSplitter` and `FuncSplitter`.
- The validation set must never leak into training.

### export / pickle

**Definition:** `learn.export()` serializes a trained `Learner` — model weights
**and** the inference-time transform pipeline — into a single pickle (`.pkl`)
file for deployment.

## Example
```python
learn.export("model.pkl")     # written to learn.path/model.pkl
```

**Related Terms:** load_learner, inference

- Bundling transforms ensures serving matches training preprocessing.
- The pickle is portable to CPU-only serving machines.
- Do not unpickle files from untrusted sources.

### load_learner

**Definition:** The function that reloads an exported `.pkl` into a ready-to-use
`Learner` for inference, without needing the original training code or a GPU.

## Example
```python
inf = load_learner("model.pkl")
label, idx, probs = inf.predict("photo.jpg")
```

**Related Terms:** export / pickle, inference, Gradio

- Loads on CPU by default — ideal for lightweight servers.
- Call it once at app startup, not per request.
- Retains `inf.dls.vocab` for mapping indices to labels.

### inference

**Definition:** Using a trained model to make predictions on new, unseen data. In
fastai, `learn.predict(x)` returns a tuple of the predicted label, its index in
the vocab, and the full probability tensor.

## Example
```python
pred_class, pred_idx, probs = inf.predict("photo.jpg")
confidence = probs[pred_idx].item()
```

**Related Terms:** load_learner, DataLoaders, domain shift

- Runs the same transforms used during training/validation.
- The probability tensor is ordered to match `dls.vocab`.
- Confidence on out-of-domain input is unreliable.

### Gradio

**Definition:** A Python library for building shareable web UIs for ML models
with minimal code. `gr.Interface` connects an input component and an output
component to a prediction function.

## Example
```python
import gradio as gr
demo = gr.Interface(fn=predict,
                    inputs=gr.Image(type="pil"),
                    outputs=gr.Label(num_top_classes=3))
demo.launch()
```

**Related Terms:** Hugging Face Spaces, load_learner, inference

- The `fn` signature must match the input/output components.
- `gr.Label` renders class probabilities as labeled bars.
- `launch()` starts a local server; Spaces runs it in the cloud.

### Hugging Face Spaces

**Definition:** A free hosting platform for ML demo apps (Gradio, Streamlit,
static, Docker). You push a repo containing your app and requirements, and Spaces
builds and serves it publicly.

## Example
```text
Space repo layout:
  app.py            # builds and launches the gr.Interface
  model.pkl         # the exported learner
  requirements.txt  # fastai, gradio, ...
```

**Related Terms:** Gradio, export / pickle

- No server management required for basic demos.
- The exported `.pkl` and `requirements.txt` must be committed to the repo.
- Great for sharing a portfolio model publicly.

### domain shift

**Definition:** The gradual divergence between the distribution a model was
trained on and the distribution it sees in production, causing accuracy to decay
silently over time.

## Example
```python
# A classifier trained on daytime photos slowly degrades as more
# night-time photos arrive in production — the input domain has shifted.
```

**Related Terms:** inference, drivetrain approach

- Distinct from a one-off out-of-domain input; it is a slow drift.
- Mitigate with monitoring and periodic retraining on fresh data.
- A human-in-the-loop rollout limits damage from unnoticed shift.

### drivetrain approach

**Definition:** A four-step method for designing data products: define the
**objective**, identify the **levers** you can control, determine the **data** you
can collect, then build the **models** that connect levers to the objective.

## Example
```text
Objective: keep viewers watching
Levers:     which video to recommend next
Data:       watch history, engagement signals
Models:     predict watch time given a candidate video
```

**Related Terms:** domain shift, inference

- Forces you to design the product, not just optimize a metric.
- Levers are the actions you can actually take, not predictions.
- Keeps modeling anchored to a real objective.

### plot_top_losses

**Definition:** A `ClassificationInterpretation` method that displays the items
with the highest loss — the model's most confident mistakes — which tend to be
mislabeled, ambiguous, or junk data.

## Example
```python
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_top_losses(6, nrows=2)
```

**Related Terms:** ImageClassifierCleaner, inference

- Used to clean data *after* a quick first model.
- Shows prediction, actual label, loss, and probability per image.
- Pairs with `ImageClassifierCleaner` for interactive relabeling.

---

## Summary

This glossary covers the fastai data and deployment stack: the **DataBlock** and
**DataLoaders** that assemble data; **item_tfms**/**batch_tfms**, **presizing**,
**RandomResizedCrop**, and **data augmentation** that prepare it; **plot_top_losses**
and the model-assisted cleaning workflow; and **export**/**load_learner**,
**inference**, **Gradio**, and **Hugging Face Spaces** that ship it. The
**drivetrain approach**, **out-of-domain data**, and **domain shift** frame the
product and its risks.

**Next:** See Lecture 03 — Neural Net Foundations & SGD, where these ready-made
pieces give way to building the learning machinery from scratch.
