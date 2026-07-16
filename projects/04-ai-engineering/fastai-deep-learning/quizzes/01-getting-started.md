# Quiz 01: Getting Started

## Topic Overview

This quiz covers fast.ai Lesson 1: the top-down teaching philosophy, the machine-learning feedback loop, transfer learning, and the core fastai objects (`DataLoaders`, `vision_learner`, `resnet34`, `fine_tune`). It also checks your understanding of overfitting, validation sets, and how to evaluate and interpret a trained classifier.

## Questions

### Question 1

**What does the fast.ai "top-down" teaching philosophy mean?**

- A) Learn all the math and theory before writing any code
- B) Train a working model first, then learn the underlying theory as needed
- C) Always use the largest available neural network
- D) Start from the output layer and work backward through the network

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** fast.ai deliberately inverts the traditional theory-first order. You build and run a real, accurate model in minutes to stay motivated, then dive into the details of the parts you actually used.

</details>

---

### Question 2

**In Arthur Samuel's framing, what makes machine learning different from traditional programming?**

- A) It runs faster on modern hardware
- B) The model's weights are adjusted automatically based on performance, instead of rules being written by hand
- C) It does not require any input data
- D) It only works for image problems

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Traditional programming means a human writes explicit rules. Machine learning replaces those rules with a model whose weights are updated automatically via the loop: inputs + weights → results → performance → update weights.

</details>

---

### Question 3

**Which sequence correctly describes Samuel's machine-learning feedback loop?**

- A) results → inputs → weights → performance
- B) weights → performance → results → inputs
- C) inputs + weights → model → results → performance → update weights
- D) inputs → results → weights (no feedback)

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The model maps inputs and weights to results; performance measures how good those results are; that performance is used to update the weights, closing the loop.

</details>

---

### Question 4

**Why does transfer learning let you train an accurate classifier on a small dataset?**

- A) It compresses your images so more fit in memory
- B) It starts from a model already trained on a huge dataset, reusing generic learned features
- C) It skips the validation set to save data
- D) It randomly initializes weights for faster convergence

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A pretrained model (e.g. ResNet on ImageNet) already knows generic features like edges and textures. You only retrain the final layers for your task, so far less data and time are needed.

</details>

---

### Question 5

**What does `fine_tune(1)` do to a `vision_learner` built on a pretrained ResNet?**

- A) Trains all layers from random initialization for one epoch
- B) Trains only the pretrained body and discards the head
- C) Trains the new head with the body frozen, then unfreezes and trains all layers
- D) Only evaluates the model without training

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `fine_tune` runs the transfer-learning schedule: a frozen phase (train just the new head) followed by an unfrozen phase (train all layers at a lower learning rate). The argument is the number of unfrozen epochs.

</details>

---

### Question 6

**What is a `DataLoaders` object in fastai?**

- A) A single image transformed to tensor form
- B) The loss function used during training
- C) A bundle of a training `DataLoader` and a validation `DataLoader` that feeds batches to the model
- D) A pretrained set of ResNet weights

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `DataLoaders` (plural) holds both the training and validation loaders and handles labelling, splitting, transforming, and batching the data.

</details>

---

### Question 7

**In the canonical PETS example, what is the role of `error_rate`?**

- A) It is the loss function the optimizer minimizes
- B) It is a human-readable metric reporting the fraction of wrong validation predictions
- C) It sets the learning rate schedule
- D) It controls the train/validation split ratio

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `error_rate` is a metric, not the loss. It reports the fraction of validation examples misclassified (accuracy = 1 − error_rate) and does not drive weight updates. fastai chooses the loss (cross-entropy) automatically.

</details>

---

### Question 8

**Why does fastai always hold out a validation set?**

- A) To speed up training by using less data
- B) To measure performance on unseen data and detect overfitting
- C) Because ResNet requires exactly 20% validation data
- D) To store the pretrained weights

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Metrics reported on the validation set reflect performance on data the model never trained on. Without it you cannot tell whether the model is generalizing or just memorizing (overfitting).

</details>

---

### Question 9

**Which pattern of results across epochs is the clearest sign of overfitting?**

- A) Both training loss and validation error keep decreasing
- B) Training loss keeps decreasing while validation error starts increasing
- C) Training loss increases while validation error decreases
- D) Both training loss and validation error stay constant

**Difficulty:** Hard

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Overfitting means the model is memorizing training data. The training loss keeps falling, but performance on unseen validation data degrades, so validation error rises.

</details>

---

### Question 10

**What does `learn.predict("pet.jpg")` return in fastai 2.7.x?**

- A) Only the predicted class as a string
- B) A tuple of (decoded label, predicted index, probability tensor)
- C) The confusion matrix for the image
- D) The updated model weights

**Difficulty:** Hard

<details><summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `learn.predict` returns three items: the decoded label, its index, and the full tensor of class probabilities. You can read the confidence as `probs[pred_idx]`. To inspect systematic mistakes you would instead use `ClassificationInterpretation`.

</details>

---

## Answer Key

1. B  2. B  3. C  4. B  5. C  6. C  7. B  8. B  9. B  10. B
