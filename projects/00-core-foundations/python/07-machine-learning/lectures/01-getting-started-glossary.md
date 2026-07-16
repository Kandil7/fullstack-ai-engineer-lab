# Glossary: Getting Started with Machine Learning

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Machine Learning | Systems that learn from data | Concept |
| Supervised Learning | Learning from labeled data | Paradigm |
| Unsupervised Learning | Learning from unlabeled data | Paradigm |
| Reinforcement Learning | Learning through rewards/penalties | Paradigm |
| Classification | Predicting discrete categories | Task |
| Regression | Predicting continuous values | Task |
| Feature | Input variable used for prediction | Data |
| Target | Output variable being predicted | Data |
| Model | Mathematical representation learned from data | Algorithm |
| Training | Process of learning from data | Process |
| Prediction | Output of a trained model | Process |
| Accuracy | Percentage of correct predictions | Metric |
| Scikit-learn | Python ML library | Library |
| NumPy | Numerical computing library | Library |
| Pandas | Data manipulation library | Library |
| k-NN | k-Nearest Neighbors algorithm | Algorithm |
| LabelEncoder | Converts categories to numbers | Tool |
| Overfitting | Model learns noise instead of patterns | Problem |
| Underfitting | Model is too simple to capture patterns | Problem |
| Dataset | Collection of data for ML | Data |
| Sample | A single data point | Data |
| Label | The correct answer for a sample | Data |
| Algorithm | Step-by-step procedure for learning | Concept |
| Hyperparameter | Configuration set before training | Concept |
| Parameter | Value learned during training | Concept |

---

## Detailed Definitions

### A

#### Accuracy
**Definition:** The proportion of correct predictions made by a model out of all predictions.

**Formula:**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**Example:**
```python
from sklearn.metrics import accuracy_score
y_actual = [1, 0, 1, 1, 0]
y_predicted = [1, 0, 1, 0, 0]
accuracy = accuracy_score(y_actual, y_predicted)
print(f"Accuracy: {accuracy:.2%}")  # 80.00%
```

**Related Terms:** Precision, Recall, F1 Score, Confusion Matrix

---

### C

#### Classification
**Definition:** A supervised learning task where the goal is to predict a discrete category or class label.

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier
# Predicting if an email is spam (1) or not (0)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)  # y contains 0s and 1s
predictions = model.predict(X_test)  # Predicted classes
```

**Related Terms:** Regression, Supervised Learning, Logistic Regression, Decision Tree

#### Clustering
**Definition:** An unsupervised learning task that groups similar data points together without predefined labels.

**Example:**
```python
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(X)  # Assigns each point to a cluster
```

**Related Terms:** K-Means, Unsupervised Learning, Dimensionality Reduction

---

### D

#### Dataset
**Definition:** A structured collection of data used for training and evaluating ML models. Typically organized as a table with rows (samples) and columns (features/target).

**Example:**
```python
from sklearn.datasets import load_iris
iris = load_iris()
print(f"Shape: {iris.data.shape}")  # (150, 4)
print(f"Features: {iris.feature_names}")
```

**Related Terms:** Feature, Target, Sample, Training Set, Test Set

#### Deep Learning
**Definition:** A subset of ML using neural networks with multiple layers to learn hierarchical representations of data.

**Example:**
```python
# Conceptual — uses libraries like TensorFlow or PyTorch
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

**Related Terms:** Neural Network, Machine Learning, Artificial Intelligence

---

### F

#### Feature
**Definition:** An individual measurable property or characteristic of the data used as input for prediction. Also called an attribute, variable, or dimension.

**Example:**
```python
# In house price prediction:
# Features: square_feet, bedrooms, age, location
X = np.array([
    [1500, 3, 10, 1],  # Sample 1
    [2000, 4, 5, 2]    # Sample 2
])
# Columns 0-3 are features
```

**Related Terms:** Target, Feature Vector, Feature Engineering, Feature Selection

---

### H

#### Hyperparameter
**Definition:** A configuration setting that is specified before training begins and is not learned from data. Used to control the learning process.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
# n_neighbors is a hyperparameter
knn = KNeighborsClassifier(n_neighbors=5)  # Set k=5 before training
knn.fit(X_train, y_train)
```

**Related Terms:** Parameter, Model Configuration, Grid Search

---

### K

#### k-Nearest Neighbors (k-NN)
**Definition:** A simple algorithm that classifies a new data point based on the majority class of its k closest neighbors in the training data.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
prediction = knn.predict(new_sample)
```

**Related Terms:** Classification, Distance Metric, Lazy Learning

---

### L

#### Label
**Definition:** The correct output or target value associated with a training sample. In supervised learning, labels are provided during training.

**Example:**
```python
# Labels for a spam detection task
y = [1, 0, 1, 0, 0, 1]  # 1=spam, 0=not spam
```

**Related Terms:** Target, Class, Annotation, Supervised Learning

#### LabelEncoder
**Definition:** A scikit-learn tool that converts categorical string labels into numerical integers.

**Example:**
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
categories = ['cat', 'dog', 'bird']
encoded = le.fit_transform(categories)  # [1, 2, 0]
print(le.classes_)  # ['bird', 'cat', 'dog']
```

**Related Terms:** One-Hot Encoding, Categorical Data, Preprocessing

---

### M

#### Machine Learning (ML)
**Definition:** A field of AI where systems learn patterns from data to make decisions or predictions without being explicitly programmed.

**Example:**
```python
# Traditional programming
def is_spam(email):
    return "buy now" in email.lower()  # Manual rules

# Machine Learning
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
model.fit(X_train_text, y_train)  # Learns rules from data
prediction = model.predict(X_test_text)
```

**Related Terms:** Artificial Intelligence, Deep Learning, Data Science

#### Model
**Definition:** A mathematical representation learned from data that can make predictions. The result of training an algorithm on a dataset.

**Example:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()  # Create model
model.fit(X_train, y_train)  # Train model
predictions = model.predict(X_test)  # Use model
```

**Related Terms:** Algorithm, Classifier, Regressor, Training

---

### N

#### NumPy
**Definition:** A Python library for numerical computing, providing efficient array operations, mathematical functions, and random number generation. Foundation of the Python ML ecosystem.

**Example:**
```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean())    # 3.0
print(arr.std())     # 1.4142...
print(np.random.rand(3, 3))  # 3x3 random matrix
```

**Related Terms:** Pandas, Scikit-learn, Array, Matrix

---

### O

#### One-Hot Encoding
**Definition:** A technique that converts categorical variables into binary vectors, where only one element is 1 (hot) and the rest are 0 (cold).

**Example:**
```python
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(sparse=False)
categories = [['red'], ['blue'], ['green']]
encoded = encoder.fit_transform(categories)
# [[1, 0, 0],  # red
#  [0, 1, 0],  # blue
#  [0, 0, 1]]  # green
```

**Related Terms:** LabelEncoder, Categorical Data, Dummy Variables

#### Overfitting
**Definition:** When a model learns the training data too well, including noise and outliers, resulting in poor performance on new, unseen data.

**Example:**
```python
# Overfitting example
from sklearn.tree import DecisionTreeClassifier
# No depth limit — will memorize training data
overfit_model = DecisionTreeClassifier(max_depth=None)
overfit_model.fit(X_train, y_train)
print(f"Train accuracy: {overfit_model.score(X_train, y_train):.2%}")  # 100%
print(f"Test accuracy: {overfit_model.score(X_test, y_test):.2%}")    # Lower
```

**Related Terms:** Underfitting, Regularization, Cross-Validation

---

### P

#### Pandas
**Definition:** A Python library for data manipulation and analysis, providing DataFrames for working with structured (tabular) data.

**Example:**
```python
import pandas as pd
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})
print(df.head())
print(df.describe())
```

**Related Terms:** NumPy, DataFrame, Data Cleaning

#### Parameter
**Definition:** A value that is learned from data during the training process. Unlike hyperparameters, parameters are not set manually.

**Example:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)
# These are learned parameters:
print(f"Coefficients (slope): {model.coef_}")  # Learned from data
print(f"Intercept: {model.intercept_}")        # Learned from data
```

**Related Terms:** Hyperparameter, Coefficient, Weight

#### Prediction
**Definition:** The output produced by a trained model when given new, unseen input data.

**Example:**
```python
model.fit(X_train, y_train)
predictions = model.predict(X_test)  # Generate predictions
for pred in predictions:
    print(f"Predicted value: {pred}")
```

**Related Terms:** Inference, Output, Classification, Regression

---

### R

#### Regression
**Definition:** A supervised learning task where the goal is to predict a continuous numerical value.

**Example:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)  # y contains continuous values (e.g., prices)
predictions = model.predict(X_test)  # Predicted prices
```

**Related Terms:** Classification, Linear Regression, Supervised Learning

---

### S

#### Sample
**Definition:** A single data point or observation in a dataset. Also called an instance, record, or example.

**Example:**
```python
# Each row is a sample
X = np.array([
    [1500, 3, 10],  # Sample 1: 1500 sqft, 3 bedrooms, 10 years old
    [2000, 4, 5],   # Sample 2
    [1200, 2, 15]   # Sample 3
])
print(f"Number of samples: {len(X)}")  # 3
```

**Related Terms:** Feature, Target, Instance, Observation

#### Scikit-learn
**Definition:** Python's most popular machine learning library, providing simple and efficient tools for data mining, analysis, and predictive modeling.

**Example:**
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)
score = r2_score(y_test, model.predict(X_test))
```

**Related Terms:** NumPy, Pandas, Machine Learning, Python

#### Supervised Learning
**Definition:** A ML paradigm where the algorithm learns from labeled training data (input-output pairs) to make predictions on new data.

**Example:**
```python
# Labeled data: X (features) + y (correct answers)
X = [[1], [2], [3], [4], [5]]  # Inputs
y = [2, 4, 6, 8, 10]           # Known outputs

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)  # Learn mapping from X to y
model.predict([[6]])  # Predict: array([12.])
```

**Related Terms:** Unsupervised Learning, Classification, Regression, Labels

---

### T

#### Target
**Definition:** The output variable that a model is trying to predict. Also called the label, dependent variable, or response variable.

**Example:**
```python
# In house price prediction
X = df[['square_feet', 'bedrooms']]  # Features
y = df['price']                       # Target (what we predict)
```

**Related Terms:** Feature, Label, Dependent Variable

#### Training
**Definition:** The process of feeding labeled data to a ML algorithm so it can learn the relationship between features and targets.

**Example:**
```python
model = LinearRegression()
model.fit(X_train, y_train)  # This is the training step
# After training, model has learned coefficients
```

**Related Terms:** Fitting, Learning, Model, Epoch

#### Training Set
**Definition:** The subset of data used to train a ML model. Typically 70-80% of the total dataset.

**Example:**
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2  # 80% training, 20% test
)
```

**Related Terms:** Test Set, Validation Set, Train-Test Split

---

### U

#### Underfitting
**Definition:** When a model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and test data.

**Example:**
```python
# Underfitting: linear model on non-linear data
from sklearn.linear_model import LinearRegression
model = LinearRegression()
# Data follows a curve, but we're fitting a straight line
model.fit(X_train, y_train)
print(f"Train R²: {model.score(X_train, y_train):.2f}")  # Low
print(f"Test R²: {model.score(X_test, y_test):.2f}")    # Also low
```

**Related Terms:** Overfitting, Bias, Model Complexity

#### Unsupervised Learning
**Definition:** A ML paradigm where the algorithm finds patterns in data without predefined labels or correct answers.

**Example:**
```python
from sklearn.cluster import KMeans
# No labels provided — algorithm finds natural groups
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(X)  # X has no y labels
```

**Related Terms:** Supervised Learning, Clustering, Dimensionality Reduction

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| Accuracy | `(TP + TN) / Total` | Correct predictions / Total predictions |
| Mean | `Σx / n` | Average of all values |
| Standard Deviation | `√(Σ(x - μ)² / n)` | Spread of data around mean |

---

## Python Import Cheat Sheet

```python
# Core ML libraries
import numpy as np                          # Numerical computing
import pandas as pd                         # Data manipulation
from sklearn import datasets                # Built-in datasets

# Preprocessing
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Models
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier

# Evaluation
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Visualization (optional but recommended)
import matplotlib.pyplot as plt
import seaborn as sns
```
