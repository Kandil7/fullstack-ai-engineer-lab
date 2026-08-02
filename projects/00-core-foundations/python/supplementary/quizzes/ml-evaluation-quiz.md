# ML: Evaluation Metrics - Quiz

## Topic Overview
Model evaluation is critical for assessing ML model performance and making informed decisions. This quiz covers classification metrics (accuracy, precision, recall, F1, AUC-ROC), regression metrics (MSE, MAE, R²), cross-validation, bias-variance diagnosis, and practical evaluation strategies.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is the purpose of model evaluation?
- **A)** To train the model faster
- **B)** To assess how well the model generalizes to unseen data
- **C)** To increase model complexity
- **D)** To reduce the number of features

**Correct Answer: B** — Model evaluation measures how well a trained model performs on data it hasn't seen, indicating its real-world usefulness.

---

### Q2. What is the accuracy paradox?
- **A)** More accurate models are always better
- **B)** High accuracy can be misleading with imbalanced datasets
- **C)** Accuracy is always the best metric
- **D)** Models can't be accurate

**Correct Answer: B** — With 99% negative class, a model predicting all negatives has 99% accuracy but fails at its actual task. High accuracy ≠ good model for imbalanced data.

---

### Q3. When should you use precision over recall?
- **A)** When false positives are more costly than false negatives
- **B)** When false negatives are more costly than false positives
- **C)** They are always interchangeable
- **D)** When the dataset is balanced

**Correct Answer: A** — Precision matters when false positives are expensive (e.g., spam filter marking legitimate email as spam). High precision = few false alarms.

---

### Q4. When should you use recall over precision?
- **A)** When false positives are costly
- **B)** When false negatives are more costly (e.g., missing a disease diagnosis)
- **C)** When the dataset is small
- **D)** When the model is simple

**Correct Answer: B** — Recall matters when missing positive cases is dangerous (e.g., cancer detection). High recall = few missed positive cases.

---

### Q5. What is the F1 score's range and interpretation?
- **A)** [0, 1] where 1 is perfect balance of precision and recall
- **B)** [0, ∞] where higher is better
- **C)** [-1, 1] where 0 is best
- **D)** [0, 100] where 100 is best

**Correct Answer: A** — F1 ranges from 0 (worst) to 1 (best). It's the harmonic mean of precision and recall, favoring models with both high precision and recall.

---

### Q6. What is cross-validation's main benefit?
- **A)** Faster training
- **B)** More reliable performance estimate than a single train/test split
- **C)** Eliminates need for a test set
- **D)** Increases model accuracy

**Correct Answer: B** — Cross-validation uses multiple train/test splits, providing a more robust estimate of model performance and reducing the variance of the evaluation.

---

### Q7. What is 5-fold cross-validation?
- **A)** Training the model 5 times on the same data
- **B)** Splitting data into 5 folds, using each fold once as test data
- **C)** Using 5 different models
- **D)** Running the model for 5 epochs

**Correct Answer: B** — 5-fold CV splits data into 5 equal parts. Each fold is used as test data once (with the other 4 as training), giving 5 performance estimates.

---

### Q8. What is the Mean Squared Error (MSE)?
- **A)** The average of absolute differences
- **B)** The average of squared differences between predicted and actual values
- **C)** The sum of all errors
- **D)** The maximum error

**Correct Answer: B** — MSE = (1/n) Σ(yᵢ - ŷᵢ)². Squaring penalizes large errors more heavily. Lower MSE = better predictions.

---

### Q9. What is the Root Mean Squared Error (RMSE)?
- **A)** MSE squared
- **B)** The square root of MSE, in the same units as the target variable
- **C)** The average error
- **D)** The median error

**Correct Answer: B** — RMSE = √MSE. It's in the same units as the target (unlike MSE), making it more interpretable. RMSE penalizes large errors more than MAE.

---

### Q10. What is the Mean Absolute Error (MAE)?
- **A)** The average of squared errors
- **B)** The average of absolute differences between predicted and actual values
- **C)** The maximum absolute error
- **D)** The sum of errors

**Correct Answer: B** — MAE = (1/n) Σ|yᵢ - ŷᵢ|. It treats all errors equally (no squaring), making it more robust to outliers than MSE.

---

### Q11. What is the difference between MSE and MAE?
- **A)** They are the same
- **B)** MSE penalizes large errors more; MAE treats all errors equally
- **C)** MAE penalizes large errors more
- **D)** MSE is always smaller

**Correct Answer: B** — MSE squares errors, so large errors contribute disproportionately more. MAE uses absolute values, giving equal weight to all errors.

---

### Q12. What does the AUC-ROC curve represent?
- **A)** Accuracy vs. threshold
- **B)** True Positive Rate vs. False Positive Rate at various thresholds
- **C)** Precision vs. recall
- **D)** Training loss vs. validation loss

**Correct Answer: B** — ROC curves plot TPR (recall) vs. FPR across classification thresholds. AUC = area under this curve; 1.0 = perfect, 0.5 = random guessing.

---

### Q13. What does an AUC of 0.5 indicate?
- **A)** Perfect model
- **B)** The model has no discriminative ability (random guessing)
- **C)** The model is overfitting
- **D)** The model is underfitting

**Correct Answer: B** — AUC = 0.5 means the ROC curve follows the diagonal, indicating the model performs no better than random chance at distinguishing classes.

---

### Q14. What is the bias-variance tradeoff in evaluation?
- **A)** High bias = underfitting; high variance = overfitting; aim for balance
- **B)** Always minimize bias
- **C)** Always minimize variance
- **D)** Bias and variance are unrelated

**Correct Answer: A** — High bias (simple model) leads to underfitting. High variance (complex model) leads to overfitting. The goal is finding the model complexity that minimizes total error.

---

### Q15. What is a learning curve in ML evaluation?
- **A)** A curve showing the learning rate over time
- **B)** A plot of training and validation performance vs. training set size
- **C)** A curve showing the loss function
- **D)** A plot of feature importance

**Correct Answer: B** — Learning curves plot performance (accuracy or loss) against training set size. They help diagnose overfitting, underfitting, and whether more data would help.

---

### Q16. What is the output of this evaluation?
```python
from sklearn.metrics import classification_report
y_true = [0, 1, 1, 0, 1, 1, 0, 0, 1, 1]
y_pred = [0, 1, 0, 0, 1, 1, 1, 0, 1, 0]
print(classification_report(y_true, y_pred, output_dict=True)['weighted avg']['f1-score'])
```
- **A)** 0.60
- **B)** 0.65
- **C)** 0.70
- **D)** 0.75

**Correct Answer: C** — With 6 positives and 4 negatives, the weighted average F1 considers class sizes. Class 0 F1 = 0.667 (support 4) and class 1 F1 = 0.727 (support 6), so (0.667×4 + 0.727×6)/10 ≈ 0.70.

---

### Q17. What is stratified k-fold cross-validation?
- **A)** Random splitting without any constraints
- **B)** Ensuring each fold has approximately the same class distribution as the full dataset
- **C)** Using k different models
- **D)** Training on the full dataset

**Correct Answer: B** — Stratified k-fold preserves class proportions in each fold, crucial for imbalanced datasets where random splitting might create folds with very different class distributions.

---

### Q18. What is the Matthews Correlation Coefficient (MCC)?
- **A)** A measure of correlation between features
- **B)** A balanced metric that accounts for all confusion matrix values, useful for imbalanced datasets
- **C)** A regression metric
- **D)** A clustering metric

**Correct Answer: B** — MCC = (TP×TN - FP×FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN)). It ranges from -1 (total disagreement) to +1 (perfect prediction), balanced even with imbalanced classes.

---

### Q19. What is the difference between train/validation/test sets?
- **A)** They are all the same
- **B)** Train: model fitting; Validation: hyperparameter tuning; Test: final evaluation
- **C)** Train: evaluation; Validation: training; Test: tuning
- **D)** Only train and test are needed

**Correct Answer: B** — Training set fits the model. Validation set tunes hyperparameters and selects models. Test set provides unbiased final performance estimate (used only once).

---

### Q20. What is data leakage in evaluation?
- **A)** Using too much memory
- **B)** When test/validation information inadvertently leaks into the training process
- **C)** Missing data points
- **D)** Having too many features

**Correct Answer: B** — Data leakage occurs when the model has access to test data during training (e.g., scaling before splitting). It leads to overly optimistic performance estimates that fail in production.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | A | 13 | B |
| 4 | B | 14 | A |
| 5 | A | 15 | B |
| 6 | B | 16 | C |
| 7 | B | 17 | B |
| 8 | B | 18 | B |
| 9 | B | 19 | B |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong ML evaluation knowledge
