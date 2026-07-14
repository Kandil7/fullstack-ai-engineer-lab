# ML: Regression - Quiz

## Topic Overview
Regression is a supervised learning technique for predicting continuous numerical values. This quiz covers linear regression, polynomial regression, regularization methods, evaluation metrics, and practical regression modeling concepts.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is linear regression?
- **A)** A classification algorithm
- **B)** A method to model the relationship between variables by fitting a linear equation
- **C)** A clustering algorithm
- **D)** A dimensionality reduction technique

**Correct Answer: B** — Linear regression models the relationship between a dependent variable and one or more independent variables using a straight line (or hyperplane).

---

### Q2. What is the equation for simple linear regression?
- **A)** y = mx + b (or y = β₀ + β₁x)
- **B)** y = ax² + bx + c
- **C)** y = Σ(wᵢxᵢ) + bias
- **D)** y = sigmoid(Σ(wᵢxᵢ))

**Correct Answer: A** — Simple linear regression fits y = β₀ + β₁x, where β₀ is the intercept and β₁ is the slope coefficient.

---

### Q3. What does the R² (R-squared) metric measure?
- **A)** The number of features
- **B)** The proportion of variance in the dependent variable explained by the model
- **C)** The number of data points
- **D)** The model's training time

**Correct Answer: B** — R² = 1 - (SS_res / SS_tot). It measures how well the model explains the variance. R² = 1 means perfect prediction; R² = 0 means no better than predicting the mean.

---

### Q4. What is the difference between simple and multiple linear regression?
- **A)** Simple uses one feature; multiple uses two or more features
- **B)** Simple is faster; multiple is slower
- **C)** Simple is for classification; multiple is for regression
- **D)** There is no difference

**Correct Answer: A** — Simple linear regression uses one independent variable; multiple linear regression uses two or more: y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ.

---

### Q5. What is the cost function commonly used in linear regression?
- **A)** Cross-entropy loss
- **B)** Mean Squared Error (MSE)
- **C)** Hinge loss
- **D)** KL divergence

**Correct Answer: B** — MSE = (1/n) Σ(yᵢ - ŷᵢ)² measures the average squared difference between actual and predicted values. It's minimized during training.

---

### Q6. What is the effect of outliers on linear regression?
- **A)** No effect
- **B)** Outliers can significantly shift the regression line
- **C)** Outliers improve model performance
- **D)** Outliers are automatically removed

**Correct Answer: B** — Linear regression is sensitive to outliers. A few extreme points can dramatically shift the regression line and reduce model accuracy.

---

### Q7. What is polynomial regression?
- **A)** Using polynomials to classify data
- **B)** Fitting a polynomial equation to capture non-linear relationships
- **C)** A regression that only uses polynomial features
- **D)** An ensemble of linear models

**Correct Answer: B** — Polynomial regression extends linear regression by adding polynomial terms (x², x³, etc.) to model non-linear relationships while still being linear in parameters.

---

### Q8. What problem does regularization solve in regression?
- **A)** Underfitting
- **B)** Overfitting by adding a penalty for large coefficients
- **C)** Slow training
- **D)** Missing data

**Correct Answer: B** — Regularization adds a penalty term to the loss function to prevent large coefficients, reducing overfitting and improving generalization.

---

### Q9. What is the difference between L1 (Lasso) and L2 (Ridge) regularization?
- **A)** L1 adds absolute value penalty; L2 adds squared penalty
- **B)** They are the same
- **C)** L1 is for classification; L2 is for regression
- **D)** L1 adds squared penalty; L2 adds absolute value penalty

**Correct Answer: A** — L1 (Lasso): penalty = λ|β|, which can drive coefficients to zero (feature selection). L2 (Ridge): penalty = λβ², which shrinks coefficients but doesn't zero them.

---

### Q10. What does a negative R² value indicate?
- **A)** The model is perfect
- **B)** The model is worse than simply predicting the mean
- **C)** The data has negative values
- **D)** The model has too many features

**Correct Answer: B** — Negative R² means the model's predictions are worse than just using the mean of the target variable as the prediction.

---

### Q11. What is the output of this code?
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

model = LinearRegression()
model.fit(X, y)
print(model.coef_[0])
```
- **A)** 0.6
- **B)** 1.0
- **C)** 0.8
- **D)** 2.0

**Correct Answer: A** — The slope (coefficient) for this data is approximately 0.6, indicating a moderate positive relationship between X and y.

---

### Q12. What is multicollinearity in multiple regression?
- **A)** Having too many features
- **B)** When independent variables are highly correlated with each other
- **C)** When the target variable is correlated with features
- **D)** When data has missing values

**Correct Answer: B** — Multicollinearity occurs when predictor variables are highly correlated, making coefficient estimates unstable and difficult to interpret.

---

### Q13. What is the difference between MSE and MAE?
- **A)** They are the same
- **B)** MSE squares errors (penalizes large errors more); MAE uses absolute errors
- **C)** MSE is for classification; MAE is for regression
- **D)** MAE is always larger than MSE

**Correct Answer: B** — MSE = (1/n)Σ(y-ŷ)² penalizes large errors more heavily. MAE = (1/n)Σ|y-ŷ| treats all errors equally. MSE is more sensitive to outliers.

---

### Q14. What is the purpose of a residual plot in regression?
- **A)** To visualize the regression line
- **B)** To check if the model's assumptions (linearity, homoscedasticity) are met
- **C)** To display the data distribution
- **D)** To show feature importance

**Correct Answer: B** — Residual plots show the difference between actual and predicted values. Patterns in residuals indicate violated assumptions (non-linearity, heteroscedasticity).

---

### Q15. What is Elastic Net regularization?
- **A)** A combination of L1 and L2 regularization
- **B)** Only L1 regularization
- **C)** No regularization
- **D)** A type of neural network

**Correct Answer: A** — Elastic Net combines L1 and L2 penalties: Loss = MSE + αL1 + βL2. It gets L1's feature selection and L2's stability with correlated features.

---

### Q16. When should you use Ridge vs. Lasso regression?
- **A)** Always use Ridge
- **B)** Ridge for many correlated features; Lasso for feature selection
- **C)** Always use Lasso
- **D)** They are interchangeable

**Correct Answer: B** — Ridge is better when many features contribute and are correlated (shrinks all). Lasso is better when you suspect only a few features matter (zeros out irrelevant ones).

---

### Q17. What is the assumption of homoscedasticity?
- **A)** The target variable is normally distributed
- **B)** The variance of residuals is constant across all predicted values
- **C)** Features are independent
- **D)** The relationship is linear

**Correct Answer: B** — Homoscedasticity means residuals have constant variance. Heteroscedasticity (non-constant variance) indicates the model may be missing important patterns.

---

### Q18. What is the adjusted R²?
- **A)** R² adjusted for the number of data points
- **B)** R² adjusted for the number of predictors, penalizing unnecessary features
- **C)** R² multiplied by a constant
- **D)** R² with outliers removed

**Correct Answer: B** — Adjusted R² = 1 - [(1-R²)(n-1)/(n-p-1)], where p is the number of features. It penalizes adding features that don't improve the model.

---

### Q19. What is the output of this prediction?
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3]])
y = np.array([3, 5, 7])

model = LinearRegression()
model.fit(X, y)
print(model.predict([[4]])[0])
```
- **A)** 7.0
- **B)** 8.0
- **C)** 9.0
- **D)** 10.0

**Correct Answer: C** — The model learns y = 1 + 2x (perfect linear relationship). For x=4: y = 1 + 2(4) = 9.0.

---

### Q20. What is the benefit of using Ridge regression when features are highly correlated?
- **A)** It removes correlated features
- **B)** It stabilizes coefficient estimates by shrinking them proportionally
- **C)** It increases model complexity
- **D)** It eliminates the need for regularization

**Correct Answer: B** — Ridge shrinks correlated feature coefficients proportionally, preventing any single coefficient from becoming too large due to multicollinearity.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | A |
| 2 | A | 12 | B |
| 3 | B | 13 | B |
| 4 | A | 14 | B |
| 5 | B | 15 | A |
| 6 | B | 16 | B |
| 7 | B | 17 | B |
| 8 | B | 18 | B |
| 9 | A | 19 | C |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong regression knowledge
