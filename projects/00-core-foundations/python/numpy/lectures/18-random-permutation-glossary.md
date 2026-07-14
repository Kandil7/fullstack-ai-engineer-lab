# Glossary: Random Permutation in NumPy (Lecture 18)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| shuffle() | `np.random.shuffle(arr)` | Shuffle in-place |
| permutation() | `np.random.permutation(arr)` | Return new shuffled array |
| permutation(n) | `np.random.permutation(n)` | Shuffled indices |
| choice() | `np.random.choice(arr, n)` | Random selection |
| replace | `replace=True/False` | Allow duplicates |
| probability | `p=weights` | Selection weights |
| In-place | `shuffle()` | Modifies original |
| Copy | `permutation()` | Returns new array |
| Seed | `np.random.seed(s)` | Reproducibility |
| Stratified | `stratify=y` | Balanced split |

---

## Detailed Definitions

### choice()

**Definition:** Randomly selects one or more elements from a 1D array. Supports sampling with or without replacement, and weighted probabilities.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Single random choice
single = np.random.choice(arr)
print("Single:", single)

# Multiple choices with replacement
with_replace = np.random.choice(arr, size=10, replace=True)
print("With replacement:", with_replace)

# Without replacement (unique)
without_replace = np.random.choice(arr, size=3, replace=False)
print("Without replacement:", without_replace)

# Weighted selection
weights = [0.1, 0.1, 0.1, 0.1, 0.6]
weighted = np.random.choice(arr, size=20, p=weights)
print("Weighted:", weighted)
```

**Related Terms:** shuffle(), permutation(), replace

---

### In-place Operation

**Definition:** An operation that modifies the original array directly without creating a new array. Memory efficient but original data is lost.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print("Before:", arr)

np.random.shuffle(arr)
print("After:", arr)  # Modified in place

# Verify it's the same object
print("Same object:", arr is arr)
```

**Related Terms:** shuffle(), Copy, View

---

### Permutation

**Definition:** A rearrangement of elements in a random order. In NumPy, can return a new array or shuffled indices.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Permutation of array
permuted = np.random.permutation(arr)
print("Permuted:", permuted)
print("Original:", arr)  # Unchanged

# Permutation of indices
indices = np.random.permutation(5)
print("Indices:", indices)
```

**Related Terms:** shuffle(), Random Order, Indices

---

### Probability Weights

**Definition:** Relative probabilities for each element when using random selection. Must sum to 1.

**Example:**
```python
import numpy as np

categories = np.array(["A", "B", "C", "D"])
weights = np.array([0.4, 0.3, 0.2, 0.1])

# Weighted selection
np.random.seed(42)
selected = np.random.choice(categories, size=100, p=weights)

# Count occurrences
unique, counts = np.unique(selected, return_counts=True)
print("Distribution:")
for cat, count in zip(unique, counts):
    print(f"  {cat}: {count}%")
```

**Related Terms:** choice(), Uniform Distribution

---

### Random Order

**Definition:** An arrangement where each element has an equal probability of appearing in any position. Achieved through shuffling or permutation.

**Example:**
```python
import numpy as np

arr = np.arange(10)
print("Original:", arr)

# Create random order
shuffled = np.random.permutation(arr)
print("Random order:", shuffled)

# Verify randomness (statistical test)
np.random.seed(42)
positions = []
for _ in range(1000):
    perm = np.random.permutation(10)
    positions.append(np.where(perm == 0)[0][0])

print(f"Mean position of 0: {np.mean(positions):.2f}")  # ~4.5
```

**Related Terms:** shuffle(), permutation(), Uniform Distribution

---

### replace

**Definition:** A parameter in `np.random.choice()` that determines whether elements can be selected more than once. True allows duplicates, False ensures unique selections.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# With replacement (duplicates possible)
with_replace = np.random.choice(arr, size=10, replace=True)
print("With replacement:", with_replace)

# Without replacement (unique)
without_replace = np.random.choice(arr, size=3, replace=False)
print("Without replacement:", without_replace)
```

**Related Terms:** choice(), Unique Selection

---

### Reproducibility

**Definition:** The ability to generate the same sequence of random numbers given the same seed. Essential for debugging and scientific research.

**Example:**
```python
import numpy as np

# Without seed - different each time
arr1 = np.random.permutation(5)
arr2 = np.random.permutation(5)
print("Different:", not np.array_equal(arr1, arr2))

# With seed - reproducible
np.random.seed(42)
arr1 = np.random.permutation(5)
np.random.seed(42)
arr2 = np.random.permutation(5)
print("Same:", np.array_equal(arr1, arr2))
```

**Related Terms:** seed(), RandomState

---

### Seed

**Definition:** An initial value that determines the sequence of random numbers. Same seed produces the same sequence.

**Example:**
```python
import numpy as np

np.random.seed(42)
arr1 = np.random.permutation(10)

np.random.seed(42)
arr2 = np.random.permutation(10)

print("Same result:", np.array_equal(arr1, arr2))
```

**Related Terms:** Reproducibility, RandomState, default_rng()

---

### Shuffle

**Definition:** To rearrange elements in a random order. In NumPy, `shuffle()` modifies the array in-place.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print("Before:", arr)

np.random.shuffle(arr)
print("After:", arr)  # Modified in place
```

**Related Terms:** permutation(), In-place Operation

---

### Train/Test Split

**Definition:** Dividing a dataset into training and testing subsets for machine learning. Typically 70-80% training, 20-30% testing.

**Example:**
```python
import numpy as np

np.random.seed(42)
X = np.random.randn(100, 5)
y = np.random.randint(0, 2, 100)

# Shuffle and split
indices = np.random.permutation(100)
train_size = 80

X_train, X_test = X[indices[:train_size]], X[indices[train_size:]]
y_train, y_test = y[indices[:train_size]], y[indices[train_size:]]

print(f"Train: {len(X_train)}, Test: {len(X_test)}")
```

**Related Terms:** shuffle(), permutation(), Stratified Split

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| choice() | Random selection from array | `np.random.choice(arr, 5)` |
| In-place | Modifies original array | `np.random.shuffle(arr)` |
| Permutation | Random rearrangement | `np.random.permutation(arr)` |
| Probability Weights | Selection probabilities | `p=[0.1, 0.2, 0.7]` |
| Random Order | Equal probability positions | Shuffled array |
| replace | Allow duplicate selections | `replace=True` |
| Reproducibility | Same seed = same result | `np.random.seed(42)` |
| Seed | Initial value for RNG | `np.random.seed(42)` |
| Shuffle | Rearrange in random order | `np.random.shuffle(arr)` |
| Train/Test Split | ML dataset division | 80/20 split |

---

**Back to Lecture:** [18 - Random Permutation](18-random-permutation-lecture.md)
