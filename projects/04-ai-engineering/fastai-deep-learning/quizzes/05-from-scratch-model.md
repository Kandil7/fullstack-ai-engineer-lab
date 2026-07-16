# Quiz 05: From-Scratch Model

## Topic Overview

This quiz checks your understanding of building a model from tensors, following
fast.ai lesson 5: data prep (imputation, log transforms, dummy variables,
normalization), a linear model with sigmoid, the hand-written training loop,
and the jump to a neural net with hidden layers and ReLU. Answer all 10
questions, then check the Answer Key.

---

## Questions

### Question 1

When filling missing values before training, which strategy is typically used
for a numeric column like `Age`?

- A) Fill with the mode
- B) Fill with the median
- C) Fill with zero
- D) Drop every row with any missing value

### Question 2

Why is `torch.log1p(Fare)` preferred over `torch.log(Fare)` for a skewed money
column?

- A) It is faster to compute
- B) `log1p(0)` is `0`, while `log(0)` is `-inf`
- C) It normalizes the column automatically
- D) It converts the column to integers

### Question 3

What does `pd.get_dummies(df, columns=["Sex"])` produce for a `Sex` column
containing `"male"` and `"female"`?

- A) A single column with 0 for male and 1 for female
- B) Two 0/1 columns: `Sex_male` and `Sex_female`
- C) A normalized floating-point column
- D) The original string column, unchanged

### Question 4

Why do we normalize input columns before training?

- A) To make the file smaller on disk
- B) So no single large-magnitude column dominates the gradient
- C) Because sigmoid requires inputs above 1
- D) To remove missing values

### Question 5

How are the linear model's coefficients initialized in the from-scratch version?

- A) `torch.zeros(n)`
- B) `torch.ones(n)`
- C) `torch.rand(n) - 0.5`
- D) `torch.randn(n) * 100`

### Question 6

Which expression is equivalent to the linear model's forward pass
`(indeps * coeffs).sum(axis=1)` for a 1-D coefficient vector?

- A) `indeps @ coeffs`
- B) `indeps + coeffs`
- C) `coeffs.sum() * indeps`
- D) `torch.relu(indeps)`

### Question 7

In the gradient step, why must you call `coeffs.grad.zero_()` after updating?

- A) To free GPU memory
- B) Because PyTorch accumulates gradients across `backward()` calls
- C) To reset the learning rate
- D) It is optional and only affects logging

### Question 8

What is the role of the `sigmoid` at the end of the forward pass?

- A) It computes the loss
- B) It maps the output into `(0, 1)` so it reads as a probability
- C) It normalizes the input columns
- D) It zeroes the gradients

### Question 9

To turn the linear model into a neural net, you insert a hidden layer and a
ReLU. What happens if you stack two matrix multiplies WITHOUT a nonlinearity
between them?

- A) The network trains twice as fast
- B) The two layers collapse into a single equivalent linear map
- C) The gradients become exactly zero
- D) The output is forced to be an integer

### Question 10

When moving from a linear model to a shallow/deep neural net in lesson 5, which
part of the code changes?

- A) The loss function
- B) The training loop and gradient step
- C) Only the prediction function (`calc_preds`) and the initializer
- D) The dataset loading

---

## Answer Key

1. **B** — Numeric columns are imputed with the median (robust to outliers);
   categorical columns use the mode.
2. **B** — `log1p(x) = log(1 + x)`, so a fare of `0` maps to `0` instead of the
   `-inf` that plain `log(0)` produces.
3. **B** — `get_dummies` creates one 0/1 column per category: `Sex_male` and
   `Sex_female`.
4. **B** — Without normalization, a large-scale column (e.g. `Age` 0-80) swamps
   0/1 dummies and dominates the gradient, so the model ignores small-scale
   features.
5. **C** — `torch.rand(n) - 0.5` gives small values centered on zero, a good
   starting point for gradient descent.
6. **A** — Element-wise multiply then sum over the feature axis is exactly the
   dot product `indeps @ coeffs`.
7. **B** — PyTorch accumulates gradients into `.grad`; without zeroing, the next
   step uses the sum of all past gradients and diverges.
8. **B** — `sigmoid(z) = 1/(1+e^-z)` squashes any real number into `(0, 1)`,
   giving a probability for the binary target.
9. **B** — Two consecutive linear maps compose into one linear map; the ReLU
   nonlinearity is what gives depth real representational power.
10. **C** — Only `calc_preds` (the forward pass) and the coefficient
    initializer change; the loss, loop, `backward()`, and step stay identical.
