# ML: Fundamentals - Quiz

## Topic Overview
Machine Learning fundamentals cover the core concepts, types of learning, data preparation, feature engineering, and the ML pipeline. This quiz tests your understanding of the building blocks needed before diving into specific algorithms.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is Machine Learning?
- **A)** Programming computers with explicit rules
- **B)** Systems that learn patterns from data to make predictions or decisions
- **C)** A type of database management
- **D)** A graphics rendering technique

**Correct Answer: B** — ML enables computers to learn from data and improve on tasks without being explicitly programmed for each scenario.

---

### Q2. Which of the following is an example of supervised learning?
- **A)** Grouping customers by purchasing behavior
- **B)** Predicting house prices from features
- **C)** An robot learning to walk in a simulation
- **D)** Reducing the dimensionality of data

**Correct Answer: B** — Supervised learning uses labeled data (input-output pairs) to learn a mapping. Predicting house prices uses known price labels during training.

---

### Q3. What is the difference between classification and regression?
- **A)** Classification predicts categories; regression predicts continuous values
- **B)** Classification is unsupervised; regression is supervised
- **C)** They are the same thing
- **D)** Regression predicts categories; classification predicts numbers

**Correct Answer: A** — Classification assigns discrete labels (spam/not spam), while regression predicts continuous values (price, temperature).

---

### Q4. What is unsupervised learning?
- **A)** Learning with labeled data
- **B)** Learning patterns from unlabeled data
- **C)** Learning through reward signals
- **D)** Learning from human feedback

**Correct Answer: B** — Unsupervised learning finds hidden patterns in data without predefined labels, such as clustering or dimensionality reduction.

---

### Q5. What is overfitting?
- **A)** The model performs well on training data but poorly on unseen data
- **B)** The model performs poorly on both training and test data
- **C)** The model is too simple to capture patterns
- **D)** The model has no parameters

**Correct Answer: A** — Overfitting occurs when a model memorizes training data (including noise) instead of learning generalizable patterns.

---

### Q6. What is underfitting?
- **A)** The model is too complex
- **B)** The model performs well on test data
- **C)** The model is too simple to capture the underlying pattern
- **D)** The model memorizes training data

**Correct Answer: C** — Underfitting happens when a model is too simple (e.g., linear model for non-linear data) and fails to capture the data's structure.

---

### Q7. What is a feature in machine learning?
- **A)** The output variable
- **B)** An input variable used for prediction
- **C)** The algorithm used
- **D)** The evaluation metric

**Correct Answer: B** — Features are the input variables (columns) that the model uses to make predictions. Also called attributes, predictors, or independent variables.

---

### Q8. What is a training set used for?
- **A)** Evaluating model performance
- **B)** Tuning hyperparameters
- **C)** Teaching the model by fitting it to known data
- **D)** Making final predictions on production data

**Correct Answer: C** — The training set is used to fit (train) the model so it learns the relationship between features and target.

---

### Q9. Why do we split data into training and test sets?
- **A)** To reduce computation time
- **B)** To evaluate how well the model generalizes to unseen data
- **C)** To increase the dataset size
- **D)** To make the algorithm faster

**Correct Answer: B** — Train/test splitting ensures we evaluate the model on data it hasn't seen, measuring real-world generalization ability.

---

### Q10. What is the typical train/test split ratio?
- **A)** 50/50
- **B)** 70/30 or 80/20
- **C)** 90/10
- **D)** 10/90

**Correct Answer: B** — Common splits are 70/30 or 80/20 (train/test). Cross-validation provides more robust evaluation by using multiple splits.

---

### Q11. What is feature engineering?
- **A)** Choosing the best algorithm
- **B)** Creating, selecting, or transforming input variables to improve model performance
- **C)** Tuning model hyperparameters
- **D)** Collecting more data

**Correct Answer: B** — Feature engineering involves creating new features, selecting relevant ones, and transforming existing ones to help the model learn better.

---

### Q12. What is the curse of dimensionality?
- **A)** Models work better with more features
- **B)** High-dimensional data becomes sparse, making distance metrics less meaningful
- **C)** Too few features lead to underfitting
- **D)** Data collection is expensive

**Correct Answer: B** — As dimensions increase, data points become more spread out, distance metrics lose meaning, and models need exponentially more data.

---

### Q13. What is cross-validation?
- **A)** Training multiple models simultaneously
- **B)** Splitting data into multiple train/test folds for more robust evaluation
- **C)** Combining multiple algorithms
- **D)** Using both supervised and unsupervised learning

**Correct Answer: B** — K-fold cross-validation splits data into K folds, training on K-1 and testing on 1, rotating through all folds for reliable performance estimates.

---

### Q14. What is the bias-variance tradeoff?
- **A)** More bias always means better models
- **B)** Balancing model simplicity (bias) with complexity (variance) for optimal generalization
- **C)** There is no tradeoff; always minimize bias
- **D)** Variance only matters in unsupervised learning

**Correct Answer: B** — High bias (simple model) causes underfitting; high variance (complex model) causes overfitting. The goal is finding the optimal balance.

---

### Q15. What is normalization?
- **A)** Removing duplicate data
- **B)** Scaling features to a standard range (e.g., [0, 1])
- **C)** Adding more features
- **D)** Removing outliers

**Correct Answer: B** — Normalization scales features to a fixed range (typically [0,1]) using min-max scaling: X_norm = (X - X_min) / (X_max - X_min).

---

### Q16. What is the difference between normalization and standardization?
- **A)** They are the same
- **B)** Normalization scales to [0,1]; standardization centers to mean=0, std=1
- **C)** Standardization is for categorical data
- **D)** Normalization is only for images

**Correct Answer: B** — Normalization (min-max) scales to [0,1]. Standardization (z-score) transforms to zero mean and unit variance: z = (X - μ) / σ.

---

### Q17. What is a loss function?
- **A)** The accuracy of the model
- **B)** A function that measures how far predictions are from actual values
- **C)** The training speed
- **D)** The number of parameters

**Correct Answer: B** — A loss function quantifies prediction error. Models minimize this function during training (e.g., MSE for regression, cross-entropy for classification).

---

### Q18. What is gradient descent?
- **A)** A classification algorithm
- **B)** An optimization algorithm that iteratively adjusts parameters to minimize the loss function
- **C)** A data preprocessing technique
- **D)** A regularization method

**Correct Answer: B** — Gradient descent computes the gradient of the loss function and updates parameters in the opposite direction, iteratively reducing error.

---

### Q19. What is the difference between batch, stochastic, and mini-batch gradient descent?
- **A)** They are all the same
- **B)** Batch uses all data; stochastic uses one sample; mini-batch uses a subset
- **C)** Batch is fastest; stochastic is slowest
- **D)** Mini-batch uses the full dataset

**Correct Answer: B** — Batch GD uses all training samples per update (stable but slow). Stochastic GD uses one sample (noisy but fast). Mini-batch GD uses small subsets (balanced).

---

### Q20. What is a hyperparameter?
- **A)** A parameter learned from data during training
- **B)** A setting configured before training that controls the learning process
- **C)** The output of the model
- **D)** A feature in the dataset

**Correct Answer: B** — Hyperparameters are set before training (e.g., learning rate, number of layers, k in KNN) and control how the model learns. Parameters are learned during training.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | A | 13 | B |
| 4 | B | 14 | B |
| 5 | A | 15 | B |
| 6 | C | 16 | B |
| 7 | B | 17 | B |
| 8 | C | 18 | B |
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

**Target:** 80%+ to demonstrate strong ML fundamentals knowledge
