# ML: Classification - Quiz

## Topic Overview
Classification is supervised learning for predicting discrete categories/labels. This quiz covers logistic regression, decision trees, random forests, SVM, KNN, Naive Bayes, ensemble methods, and classification metrics.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is logistic regression used for?
- **A)** Predicting continuous values
- **B)** Binary classification (predicting probabilities of class membership)
- **C)** Clustering data
- **D)** Dimensionality reduction

**Correct Answer: B** — Despite its name, logistic regression is a classification algorithm that uses the sigmoid function to output probabilities for binary outcomes.

---

### Q2. What function does logistic regression use to map predictions to probabilities?
- **A)** Linear function
- **B)** Sigmoid (logistic) function
- **C)** ReLU function
- **D)** Tanh function

**Correct Answer: B** — The sigmoid function σ(z) = 1/(1+e^(-z)) maps any real number to a value between 0 and 1, interpretable as a probability.

---

### Q3. What is the decision boundary in classification?
- **A)** The training data
- **B)** The surface that separates different classes
- **C)** The test data
- **D)** The loss function

**Correct Answer: B** — The decision boundary is the threshold/region where the model decides which class an observation belongs to.

---

### Q4. What is a confusion matrix?
- **A)** A matrix showing feature correlations
- **B)** A table showing true vs. predicted classifications (TP, TN, FP, FN)
- **C)** A matrix of model weights
- **D)** A visualization of the loss function

**Correct Answer: B** — A confusion matrix summarizes predictions: True Positives, True Negatives, False Positives, and False Negatives.

---

### Q5. What is the formula for accuracy?
- **A)** (TP + TN) / (TP + TN + FP + FN)
- **B)** TP / (TP + FP)
- **C)** TP / (TP + FN)
- **D)** (TP + FP) / (TP + TN + FP + FN)

**Correct Answer: A** — Accuracy = (correct predictions) / (total predictions) = (TP + TN) / (TP + TN + FP + FN).

---

### Q6. When is accuracy NOT a good metric?
- **A)** When classes are balanced
- **B)** When classes are imbalanced (e.g., 99% negative, 1% positive)
- **C)** When the dataset is small
- **D)** When there are many features

**Correct Answer: B** — With imbalanced classes, a model predicting the majority class always can achieve high accuracy but is useless. Precision, recall, or F1 are better.

---

### Q7. What is precision?
- **A)** TP / (TP + FN)
- **B)** TP / (TP + FP)
- **C)** TN / (TN + FP)
- **D)** (TP + TN) / Total

**Correct Answer: B** — Precision = TP / (TP + FP) measures how many predicted positives are actually positive. High precision = low false positive rate.

---

### Q8. What is recall (sensitivity)?
- **A)** TP / (TP + FP)
- **B)** TN / (TN + FP)
- **C)** TP / (TP + FN)
- **D)** (TP + TN) / Total

**Correct Answer: C** — Recall = TP / (TP + FN) measures how many actual positives are correctly identified. High recall = low false negative rate.

---

### Q9. What is the F1 score?
- **A)** The average of precision and recall
- **B)** The harmonic mean of precision and recall
- **C)** The product of precision and recall
- **D)** The difference between precision and recall

**Correct Answer: B** — F1 = 2 × (precision × recall) / (precision + recall). The harmonic mean penalizes extreme differences between precision and recall.

---

### Q10. What is a decision tree?
- **A)** A linear model for regression
- **B)** A tree-like model that makes decisions based on feature splits
- **C)** A neural network architecture
- **D)** A clustering algorithm

**Correct Answer: B** — Decision trees split data recursively based on feature conditions, creating a tree of decisions. Each leaf node represents a class prediction.

---

### Q11. What is the Gini impurity used for in decision trees?
- **A)** Measuring tree depth
- **B)** Measuring the probability of incorrectly classifying a randomly chosen element
- **C)** Calculating feature importance
- **D)** Determining tree size

**Correct Answer: B** — Gini impurity = 1 - Σ(pᵢ²) measures the chance of misclassification. Decision trees split to minimize Gini impurity (or maximize information gain).

---

### Q12. What is a random forest?
- **A)** A single decision tree
- **B)** An ensemble of decision trees trained on random subsets of data and features
- **C)** A linear classifier
- **D)** A neural network

**Correct Answer: B** — Random forest builds multiple decision trees using bootstrapped samples and random feature subsets, then averages their predictions for better generalization.

---

### Q13. What is the main advantage of random forests over single decision trees?
- **A)** Faster training
- **B)** Reduced overfitting through ensemble averaging
- **C)** Better interpretability
- **D)** Requires less data

**Correct Answer: B** — Averaging many trees reduces variance and overfitting. Single trees tend to overfit; random forests generalize better.

---

### Q14. What is the SVM (Support Vector Machine)?
- **A)** A clustering algorithm
- **B)** A classifier that finds the hyperplane maximizing the margin between classes
- **C)** A regression algorithm
- **D)** A dimensionality reduction technique

**Correct Answer: B** — SVM finds the optimal hyperplane that maximizes the margin (distance) between the closest points (support vectors) of different classes.

---

### Q15. What is the kernel trick in SVM?
- **A)** A preprocessing step
- **B)** Transforming data into higher dimensions to find linear separation without explicit transformation
- **C)** A way to reduce features
- **D)** A sampling technique

**Correct Answer: B** — The kernel trick computes dot products in higher-dimensional space without explicitly transforming data, enabling SVM to find non-linear decision boundaries.

---

### Q16. What is K-Nearest Neighbors (KNN)?
- **A)** A parametric learning algorithm
- **B)** A non-parametric algorithm that classifies based on the majority class of k nearest neighbors
- **C)** A neural network
- **D)** A clustering algorithm

**Correct Answer: B** — KNN classifies a new point by finding the k closest training examples and assigning the most common class among them.

---

### Q17. What happens when K=1 in KNN?
- **A)** The model is very general
- **B)** The model overfits (sensitive to noise)
- **C)** The model is optimal
- **D)** The model underfits

**Correct Answer: B** — K=1 means the model classifies based on the single nearest neighbor, making it very sensitive to noise and outliers (high variance, overfitting).

---

### Q18. What is Naive Bayes based on?
- **A)** Decision trees
- **B)** Bayes' theorem with the assumption of feature independence
- **C)** Gradient descent
- **D)** Support vectors

**Correct Answer: B** — Naive Bayes applies Bayes' theorem P(Class|Features) = P(Features|Class) × P(Class) / P(Features) with the "naive" assumption that features are independent given the class.

---

### Q19. What is the AUC-ROC curve?
- **A)** A plot of accuracy vs. threshold
- **B)** A plot of True Positive Rate vs. False Positive Rate at various thresholds
- **C)** A plot of precision vs. recall
- **D)** A plot of loss vs. epochs

**Correct Answer: B** — ROC curves plot TPR (recall) vs. FPR at different classification thresholds. AUC measures the overall ability to distinguish between classes (1.0 = perfect).

---

### Q20. What is the output of this code?
```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=100, n_features=2, random_state=42)
model = LogisticRegression()
model.fit(X, y)
print(model.score(X, y))
```
- **A)** 0.0
- **B)** Always 1.0
- **C)** A value between 0 and 1 representing accuracy
- **D)** Error

**Correct Answer: C** — `model.score()` returns the mean accuracy on the given data. For this linearly separable dataset, accuracy should be close to 1.0.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | B | 13 | B |
| 4 | B | 14 | B |
| 5 | A | 15 | B |
| 6 | B | 16 | B |
| 7 | B | 17 | B |
| 8 | C | 18 | B |
| 9 | B | 19 | B |
| 10 | B | 20 | C |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong classification knowledge
