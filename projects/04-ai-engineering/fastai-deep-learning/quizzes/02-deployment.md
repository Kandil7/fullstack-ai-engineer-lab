# Quiz 02: Deployment & the fastai Stack

## Topic Overview
This quiz covers fast.ai's deployment lesson: the `DataBlock` API and
`DataLoaders`, the difference between `item_tfms` and `batch_tfms`, presizing and
data augmentation, cleaning data with a trained model via `plot_top_losses` and
`ImageClassifierCleaner`, exporting a `Learner` and running inference with
`load_learner`/`predict`, building a Gradio app hosted on Hugging Face Spaces,
and the drivetrain approach with its out-of-domain and domain-shift risks.

---

## Questions

### Question 1
**What does a `DataBlock` represent?**

- A) The trained model weights
- B) A reusable blueprint for turning raw sources into model-ready data
- C) A single batch of images
- D) The GPU memory allocation for training

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A `DataBlock` is a declarative blueprint. It specifies the input/target types (`blocks`), how to find items (`get_items`), how to split (`splitter`), how to label (`get_y`), and which transforms to apply — but it holds no data itself until you call `.dataloaders(source)`. This separation lets the same blueprint work on any matching dataset.
</details>

---

### Question 2
**In `blocks=(ImageBlock, CategoryBlock)`, what does `CategoryBlock` define?**

- A) The image resizing strategy
- B) The dependent variable (the label) as a single category
- C) The batch size
- D) The optimizer

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** In `blocks=(x_block, y_block)`, the first entry describes the independent variable and the second the dependent variable. `ImageBlock` says the input is an image; `CategoryBlock` says the target is a single categorical label. fastai builds the appropriate transforms and the class vocabulary from these types.
</details>

---

### Question 3
**Where do `item_tfms` run, and what is their main job?**

- A) On the GPU, for augmentation
- B) On the CPU, per image, mainly to make items a uniform size
- C) On the GPU, per batch, to normalize pixels
- D) On disk, to compress images

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `item_tfms` run on the CPU, one item at a time. Their primary purpose is to make every image the same size (typically with `Resize`) so items can be collated into a batch. Augmentation, by contrast, belongs in `batch_tfms` on the GPU.
</details>

---

### Question 4
**What is presizing in fastai?**

- A) Resizing all images once before saving them to disk
- B) Resizing items to a large square on CPU, then augmenting/cropping to the final size on GPU
- C) Choosing the model input size before training
- D) Downloading images at a fixed resolution

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Presizing is a two-step strategy: `item_tfms=Resize(460)` produces oversized uniform images on the CPU, then `batch_tfms=aug_transforms(size=224, ...)` augments and crops them down on the GPU. Doing the destructive resize once, oversized, avoids the blurry edges and repeated interpolation artifacts of many small transforms.
</details>

---

### Question 5
**Why does `RandomResizedCrop` help reduce overfitting?**

- A) It makes images smaller so training is faster
- B) It shows the model a different random region/scale of each image every epoch
- C) It removes noisy images from the dataset
- D) It increases the learning rate automatically

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `RandomResizedCrop` selects a random sub-region at a random scale each epoch, so the model effectively never sees the exact same image twice. This variety forces it to learn robust features rather than memorizing specific pixels. `min_scale` controls the minimum fraction of the original a crop must cover.
</details>

---

### Question 6
**What is the key fast.ai insight about when to clean your data?**

- A) Always clean all data by hand before training anything
- B) Never clean data; more noise always helps
- C) Train a quick model first, then use it to find the noisy/mislabeled data
- D) Clean data only after the final model is fully trained

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** fast.ai recommends training a quick baseline model first, then using it to surface bad data. A partly-trained model's highest-loss items concentrate on mislabeled, ambiguous, or junk images. Cleaning by hand beforehand wastes effort on data the model already handles correctly.
</details>

---

### Question 7
**What does `plot_top_losses` display?**

- A) The training loss curve over epochs
- B) The images with the highest loss — the model's most confident mistakes
- C) A histogram of pixel values
- D) The learning rate finder results

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `ClassificationInterpretation.plot_top_losses` shows the items where the model was both wrong and confident (highest loss), along with the prediction, actual label, loss, and probability. These items tend to be mislabeled or ambiguous, making it the starting point for model-assisted data cleaning.
</details>

---

### Question 8
**What does `ImageClassifierCleaner` actually do when you make selections?**

- A) Immediately deletes or moves files on disk
- B) Records your keep/relabel/delete choices, which you then apply in code
- C) Retrains the model automatically
- D) Uploads images to Hugging Face

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `ImageClassifierCleaner` renders per-image dropdowns (Keep / a new label / Delete) but never touches files itself. It records your decisions, which you apply explicitly — e.g. `for i in cleaner.delete(): cleaner.fns[i].unlink()` and `for i, cat in cleaner.change(): shutil.move(...)`. This keeps the destructive step under your control.
</details>

---

### Question 9
**What does `learn.export("model.pkl")` save, and why does that matter?**

- A) Only the raw weights, so you must rebuild transforms manually
- B) The model plus its inference-time transform pipeline, so serving matches training
- C) The entire training dataset
- D) Just the confusion matrix

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `export()` pickles both the model weights and the `DataLoaders` transform pipeline into one `.pkl`. Because the preprocessing travels with the model, `load_learner` at serving time applies exactly the same transforms used during training — avoiding train/serve skew. It also loads fine on CPU-only machines.
</details>

---

### Question 10
**A classifier trained on daytime photos gradually loses accuracy as more night-time photos appear in production. What is this called?**

- A) Overfitting
- B) Domain shift
- C) Vanishing gradients
- D) Data augmentation

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Domain shift is the gradual divergence between the training distribution and the production distribution over time, causing silent accuracy decay. It differs from a one-off out-of-domain input; it is a slow drift. Mitigations include monitoring, periodic retraining on fresh data, and a human-in-the-loop rollout.
</details>

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 6 | C |
| 2 | B | 7 | B |
| 3 | B | 8 | B |
| 4 | B | 9 | B |
| 5 | B | 10 | B |
