# Lecture 01: Getting Started with Machine Learning

## Topic Overview

Machine Learning (ML) is a subset of Artificial Intelligence (AI) that enables systems to learn from data and improve their performance without being explicitly programmed. This lecture introduces the fundamental concepts of ML, the types of learning paradigms, the ML workflow, and the essential Python libraries used in the field.

Machine Learning is not about programming computers to solve problems — it's about enabling them to *learn* solutions from data. This paradigm shift is what makes ML so powerful for tasks where writing explicit rules would be impractical or impossible.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define Machine Learning and explain why it matters
2. Distinguish between Supervised, Unsupervised, and Reinforcement Learning
3. Understand the difference between Classification and Regression
4. Describe the standard ML workflow from data collection to deployment
5. Load and explore datasets using scikit-learn
6. Build your first ML model using k-Nearest Neighbors
7. Handle numerical and categorical data types
8. Identify the key ML libraries in the Python ecosystem

---

## Key Concepts

### 1. What is Machine Learning?

Machine Learning is the science of getting computers to act without being explicitly programmed. Instead of writing rules manually, we feed data into algorithms that learn patterns and make decisions.

**Traditional Programming:**
```
Input + Rules → Output
```

**Machine Learning:**
```
Input + Output → Rules (Model)
```

**Real-world examples:**
- **Email filtering:** Learning to distinguish spam from legitimate emails
- **Recommendation systems:** Netflix suggesting movies based on viewing history
- **Image recognition:** Identifying objects in photos
- **Voice assistants:** Understanding and responding to speech
- **Medical diagnosis:** Detecting diseases from medical images

### 2. Types of Machine Learning

#### Supervised Learning
The algorithm learns from **labeled data** — each training example comes with an input and the correct output.

- **Classification:** Predicting a discrete category
  - Email → Spam / Not Spam
  - Image → Cat / Dog / Bird
  - Patient → Disease A / Disease B / Healthy

- **Regression:** Predicting a continuous value
  - House features → Price
  - Weather data → Temperature
  - Historical sales → Future revenue

#### Unsupervised Learning
The algorithm finds patterns in **unlabeled data** — there's no correct answer to learn from.

- **Clustering:** Grouping similar data points
  - Customer segmentation
  - Document grouping
  - Gene expression analysis

- **Dimensionality Reduction:** Reducing the number of features
  - Data visualization
  - Feature extraction
  - Noise reduction

#### Reinforcement Learning
The algorithm learns through **trial and error** with rewards and penalties.

- Game playing (Chess, Go, Atari)
- Robotics
- Autonomous vehicles
- Resource management

### 3. The ML Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. Collect  │───▶│  2. Prepare  │───▶│  3. Choose  │
│    Data      │    │    Data      │    │   Model     │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌─────────────┐    ┌───────▼───────┐
│  7. Deploy   │◀──│  6. Tune     │◀──│  4. Train     │
│   Model      │    │  Parameters  │    │   Model      │
└─────────────┘    └─────────────┘    └───────────────┘
                          ▲                    │
                          │              ┌─────▼───────┐
                          └──────────────│  5. Evaluate │
                                         │    Model     │
                                         └─────────────┘
```

**Step 1: Collect Data** — Gather relevant data from databases, APIs, files, or web scraping.

**Step 2: Prepare Data** — Clean, transform, and preprocess data (handle missing values, encode categories, scale features).

**Step 3: Choose Model** — Select an algorithm appropriate for your problem (linear regression, decision tree, neural network, etc.).

**Step 4: Train Model** — Feed training data to the algorithm so it learns patterns.

**Step 5: Evaluate Model** — Test the model on unseen data to measure performance.

**Step 6: Tune Parameters** — Adjust model hyperparameters to improve performance.

**Step 7: Deploy Model** — Put the model into production to make real predictions.

### 4. Scikit-learn Overview

Scikit-learn is the most popular ML library in Python. It provides:

- **Consistent API:** All models follow the same `.fit()`, `.predict()`, `.score()` pattern
- **Wide Algorithm Selection:** Classification, regression, clustering, dimensionality reduction
- **Preprocessing Tools:** Scaling, encoding, feature selection
- **Model Evaluation:** Cross-validation, metrics, hyperparameter tuning
- **Built-in Datasets:** Iris, Boston Housing, Digits, etc.

---

## Code Examples

### Example 1: Generating Sample Data

```python
import numpy as np

# Generate 100 data points with a linear relationship + noise
np.random.seed(42)  # For reproducibility
X = np.random.rand(100, 1) * 10  # Feature: random values 0-10
y = 2 * X.squeeze() + 3 + np.random.randn(100) * 0.5  # Target: y = 2x + 3 + noise

print(f"Generated {len(X)} data points")
print(f"X range: {X.min():.2f} to {X.max():.2f}")
print(f"y range: {y.min():.2f} to {y.max():.2f}")
```

**Explanation:**
- `np.random.seed(42)` ensures the same random numbers every time (reproducibility)
- `X` is a 2D array (required by scikit-learn) with shape `(100, 1)`
- `y` is a 1D array following `y = 2x + 3` with Gaussian noise added
- `.squeeze()` converts X from 2D to 1D for the calculation

### Example 2: Types of Machine Learning

```python
ml_types = {
    "Supervised Learning": "Learns from labeled data (classification, regression)",
    "Unsupervised Learning": "Finds patterns in unlabeled data (clustering, dimensionality reduction)",
    "Reinforcement Learning": "Learns through trial and error with rewards"
}

for ml_type, description in ml_types.items():
    print(f"{ml_type}: {description}")
```

### Example 3: Loading the Iris Dataset

```python
from sklearn import datasets

# Load the built-in Iris dataset
iris = datasets.load_iris()

print(f"Dataset shape: {iris.data.shape}")  # (150, 4) — 150 samples, 4 features
print(f"Features: {iris.feature_names}")     # sepal length, sepal width, etc.
print(f"Target classes: {list(iris.target_names)}")  # setosa, versicolor, virginica

# Explore the data
print(f"First 5 samples:\n{iris.data[:5]}")
print(f"First 5 targets: {iris.target[:5]}")
```

**Explanation:**
- The Iris dataset contains 150 flowers with 4 measurements each
- 3 species of iris: setosa (0), versicolor (1), virginica (2)
- `iris.data` is the feature matrix (150×4)
- `iris.target` is the label vector (150,)

### Example 4: Your First ML Model (k-NN)

```python
from sklearn.neighbors import KNeighborsClassifier

# Split data manually (first 100 for training, last 50 for testing)
X_train, X_test = iris.data[:100], iris.data[100:]
y_train, y_test = iris.target[:100], iris.target[100:]

# Create and train the model
knn = KNeighborsClassifier(n_neighbors=3)  # k=3
knn.fit(X_train, y_train)  # Learn from training data

# Make predictions
predictions = knn.predict(X_test)

# Calculate accuracy
accuracy = np.mean(predictions == y_test)
print(f"Model accuracy: {accuracy:.2%}")
```

**Explanation:**
- `KNeighborsClassifier(n_neighbors=3)` creates a k-NN model with k=3
- `.fit(X_train, y_train)` trains the model on labeled data
- `.predict(X_test)` makes predictions on unseen data
- Accuracy = percentage of correct predictions

### Example 5: Encoding Categorical Data

```python
from sklearn.preprocessing import LabelEncoder

categories = np.array(['cat', 'dog', 'bird', 'cat', 'dog'])
le = LabelEncoder()
encoded = le.fit_transform(categories)

print(f"Original: {categories}")
print(f"Encoded: {encoded}")          # [0, 1, 2, 0, 1]
print(f"Classes: {le.classes_}")      # ['bird', 'cat', 'dog']
```

**Explanation:**
- ML models need numerical input, not text
- `LabelEncoder` converts categorical strings to integers
- Alphabetical order determines the encoding: bird=0, cat=1, dog=2
- For non-ordinal categories, consider One-Hot Encoding instead

---

## Common Mistakes to Avoid

1. **Not setting random seeds** — Results won't be reproducible
2. **Testing on training data** — Always split data before evaluation
3. **Ignoring data quality** — Garbage in, garbage out
4. **Using wrong data types** — ML models need numerical input
5. **Skipping exploration** — Always visualize and understand your data first
6. **Assuming more data is always better** — Quality matters more than quantity
7. **Not checking for class imbalance** — Can bias model toward majority class

---

## Best Practices

1. **Set random seeds** for reproducibility: `np.random.seed(42)`
2. **Explore your data** before modeling: `df.describe()`, `df.info()`
3. **Start simple** — begin with basic models before trying complex ones
4. **Use scikit-learn's built-in datasets** to learn and prototype
5. **Understand your problem type** (classification vs. regression) before choosing a model
6. **Document your workflow** — keep notes on what you tried and the results
7. **Learn the API pattern**: `.fit()` → `.predict()` → `.score()`

---

## Practice Exercises

### Exercise 1: Basic Data Generation
Generate 200 data points following `y = 3x - 2` with noise (standard deviation 1.0). Plot the relationship.

### Exercise 2: Dataset Exploration
Load the `load_digits` dataset from scikit-learn. How many samples are there? How many features? What are the target classes?

### Exercise 3: First Model
Using the Iris dataset, train a k-NN classifier with `k=5`. Calculate the accuracy on a test set (last 30 samples).

### Exercise 4: Categorical Encoding
Create a list of 10 colors (`['red', 'blue', 'green', 'red', 'blue', ...]`). Use `LabelEncoder` to convert them to numbers. What mapping was used?

### Exercise 5: ML Workflow
Write pseudocode (or actual code) that follows all 7 steps of the ML workflow for predicting house prices.

---

## Summary

| Concept | Description |
|---------|-------------|
| **Machine Learning** | Systems that learn from data without explicit programming |
| **Supervised Learning** | Learning from labeled data (classification & regression) |
| **Unsupervised Learning** | Finding patterns in unlabeled data (clustering) |
| **Reinforcement Learning** | Learning through trial and error with rewards |
| **Scikit-learn** | Python's go-to ML library with consistent API |
| **Workflow** | Collect → Prepare → Choose → Train → Evaluate → Tune → Deploy |
| **k-NN** | Simple classifier that votes based on k nearest neighbors |

**Key Takeaway:** Machine Learning is about enabling computers to learn from data. Start with understanding your data and problem type, then choose appropriate tools and algorithms. The scikit-learn library provides a consistent, easy-to-use interface for all ML tasks.

---

## Next Lecture

In [Lecture 02: Data Mining](02-data-mining-lecture.md), we'll explore how to discover patterns in large datasets using clustering, association rules, and other data mining techniques.
