# Quiz 06: Random Forests & Tabular

## Topic Overview

Ten questions covering fast.ai lesson 6: decision trees, how splits are chosen,
overfitting and the bias-variance tradeoff, bagging and random forests,
n_estimators, out-of-bag error, feature importance, partial dependence, and
practical model choice for tabular data. Answer all ten, then check the Answer
Key.

---

### Question 1
When a decision tree chooses a split at a node, what does it try to minimize?

A. The number of leaf nodes
B. The weighted impurity (e.g., Gini or variance) of the two child nodes
C. The depth of the tree
D. The number of features used

---

### Question 2
What is the prediction returned by a leaf node in a **regression** tree?

A. The majority class of the rows in that leaf
B. A random row's target value
C. The mean target value of the training rows that reached the leaf
D. Zero, always

---

### Question 3
A decision tree with no depth or leaf-size limit achieves ~100% training
accuracy but much lower validation accuracy. This is a classic case of:

A. High bias (underfitting)
B. High variance (overfitting)
C. Data leakage
D. Class imbalance

---

### Question 4
What does the "bootstrap" in bagging refer to?

A. Sampling rows *with replacement* to form each tree's training set
B. Removing outliers before training
C. Scaling all features to zero mean and unit variance
D. Sorting the data by the target column

---

### Question 5
Why does averaging many trees in a random forest reduce error?

A. Each tree has lower bias than a single tree
B. Averaging weakly-correlated errors cancels much of the variance
C. It increases training accuracy on every tree
D. It removes the need for any validation

---

### Question 6
In a random forest, what is the purpose of considering only a random *subset of
columns* at each split (`max_features`)?

A. To speed up training only, with no effect on quality
B. To decorrelate the trees so their errors are more independent
C. To guarantee every feature is used exactly once
D. To reduce the number of rows per tree

---

### Question 7
You increase `n_estimators` from 200 to 5000. What is the most likely outcome?

A. Validation accuracy improves dramatically
B. The model starts to overfit badly
C. Little to no accuracy change, but much longer training time
D. Bias increases sharply

---

### Question 8
What is the **out-of-bag (OOB)** score, and why is it useful?

A. Accuracy on the training rows; it measures memorization
B. Accuracy estimated from rows each tree did not see; free validation
C. The fraction of features that were unused
D. The error on a mandatory separate test set

---

### Question 9
`feature_importances_` in a random forest is computed primarily from:

A. The correlation of each feature with the target
B. The total impurity reduction contributed by each feature across all splits
C. The alphabetical order of the column names
D. The number of missing values in each column

---

### Question 10
For a brand-new tabular dataset, what does fast.ai recommend as the first model
to try, and why?

A. A deep neural net, because it always wins on tabular data
B. Gradient boosting, because it needs no tuning
C. A random forest, because it is robust and very hard to mess up
D. Linear regression, because it is the fastest to train

---

## Answer Key

1. **B** — At each node the tree greedily picks the (column, threshold) split
   that minimizes the weighted impurity of the two resulting groups (Gini or
   entropy for classification, variance/std for regression).

2. **C** — A regression leaf predicts the mean target of the training rows that
   reached it. (A classification leaf uses the majority class / class
   probabilities.)

3. **B** — A perfect train score with a much lower validation score is high
   variance: the tree memorized training-set noise instead of the signal.

4. **A** — A bootstrap sample is drawn *with replacement* from the training
   rows, so each tree sees a slightly different dataset (~63% of unique rows).

5. **B** — Bagging attacks the variance term: averaging many uncorrelated (or
   weakly correlated) errors makes them cancel, while bias stays roughly the
   same.

6. **B** — Restricting each split to a random feature subset forces trees to be
   different, decorrelating them; this decorrelation is what makes averaging
   effective. It also happens to speed up training, but that is secondary.

7. **C** — More trees only reduce variance and do so with steep diminishing
   returns; past the plateau (~100-200) you mostly pay compute for negligible
   gain. It does not overfit or raise bias.

8. **B** — Each tree omits ~37% of rows (its OOB rows); scoring every row with
   only the trees that never saw it yields a validation-quality estimate with no
   separate held-out set. Enable via `oob_score=True`.

9. **B** — Importance is the total (normalized) impurity reduction each feature
   contributes across all splits in all trees. It is biased toward
   high-cardinality features, so corroborate with partial dependence or
   permutation importance.

10. **C** — fast.ai's practical guidance is to start with a random forest: it
    needs minimal preprocessing, rarely overfits catastrophically, gives free
    OOB validation and feature importance, and is very hard to get badly wrong.
