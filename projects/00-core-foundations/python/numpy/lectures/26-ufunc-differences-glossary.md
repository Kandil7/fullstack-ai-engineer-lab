# Glossary: Difference Ufuncs (Lecture 26)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| diff() | `np.diff(arr)` | First discrete difference |
| diff(n=2) | `np.diff(arr, n=2)` | Second order difference |
| axis | Parameter | Diff along axis |
| prepend | Parameter | Add values before diff |
| append | Parameter | Add values after diff |
| First Difference | Δx[i] = x[i+1] - x[i] | Rate of change |
| Second Difference | Δ²x[i] | Acceleration |
| Edge Detection | Finding transitions | Signal processing |
| Discrete Derivative | Approximate derivative | Numerical analysis |

---

## Detailed Definitions

### append

**Definition:** A parameter in `np.diff()` that adds values to the end of the array before computing differences. Results in an extra difference at the end.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 35, 55])
diff_append = np.diff(arr, append=100)
print("diff(append=100):", diff_append)
# Output: [10 15 20 45]
```

**Related Terms:** prepend, diff()

---

### axis

**Definition:** A parameter that specifies the axis along which to compute differences. Default is -1 (last axis).

**Example:**
```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6]])

print("Diff axis=1:\n", np.diff(arr2d, axis=1))
# [[1 1]
#  [1 1]]

print("Diff axis=0:\n", np.diff(arr2d, axis=0))
# [[3 3]
#  [3 3]]
```

**Related Terms:** diff(), Shape

---

### Cumulative Sum

**Definition:** The running total of an array. Inverse operation of diff. Used to reconstruct arrays from differences.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 35, 55])
diffs = np.diff(arr)
reconstructed = np.concatenate([[arr[0]], np.cumsum(diffs)])
print("Original:", arr)
print("Reconstructed:", reconstructed)
# Match!
```

**Related Terms:** diff(), cumsum()

---

### Discrete Derivative

**Definition:** An approximation of the derivative using finite differences. Calculated as Δx/Δt for evenly spaced data.

**Example:**
```python
import numpy as np

time = np.array([0, 1, 2, 3, 4])
position = np.array([0, 10, 30, 60, 100])

velocity = np.diff(position) / np.diff(time)
print("Velocity:", velocity)  # [10 20 30 40]
```

**Related Terms:** diff(), Derivative

---

### diff()

**Definition:** Calculates the n-th discrete difference along the given axis. Returns array of length len(arr) - n.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])
print("1st diff:", np.diff(arr))      # [3 5 7 9]
print("2nd diff:", np.diff(arr, n=2))  # [2 2 2]
```

**Related Terms:** cumsum(), Prepend, Append

---

### Edge Detection

**Definition:** Identifying points in a signal where the value changes significantly. Useful in signal processing and computer vision.

**Example:**
```python
import numpy as np

signal = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0])
edges = np.diff(signal)
rise = np.where(edges == 1)[0] + 1
fall = np.where(edges == -1)[0] + 1
print("Rise edges:", rise)
print("Fall edges:", fall)
```

**Related Terms:** Signal Processing, Transition

---

### First Difference

**Definition:** The difference between consecutive elements: Δx[i] = x[i+1] - x[i]. Represents the rate of change.

**Example:**
```python
import numpy as np

arr = np.array([10, 15, 25, 40, 60])
first_diff = np.diff(arr)
print("First difference:", first_diff)
# Output: [ 5 10 15 20]
```

**Related Terms:** Second Difference, Rate of Change

---

### Higher-Order Difference

**Definition:** Differences of differences. Second difference measures acceleration, third difference measures jerk, etc.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])
print("1st:", np.diff(arr))      # [3 5 7 9]
print("2nd:", np.diff(arr, n=2))  # [2 2 2]
print("3rd:", np.diff(arr, n=3))  # [0 0]
```

**Related Terms:** First Difference, diff()

---

### Prepend

**Definition:** A parameter in `np.diff()` that adds values to the beginning of the array before computing differences. Results in an extra difference at the start.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 35, 55])
diff_prepend = np.diff(arr, prepend=0)
print("diff(prepend=0):", diff_prepend)
# Output: [10 10 15 20]
```

**Related Terms:** append, diff()

---

### Rate of Change

**Definition:** How quickly a value changes over time or space. Calculated using first difference.

**Example:**
```python
import numpy as np

prices = np.array([100, 102, 101, 105, 103])
changes = np.diff(prices)
print("Rate of change:", changes)
# Output: [ 2 -1  4 -2]
```

**Related Terms:** First Difference, Velocity

---

### Second Difference

**Definition:** The difference of the first difference. Measures acceleration or curvature. For a quadratic sequence, it's constant.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])  # n^2
second_diff = np.diff(arr, n=2)
print("Second difference:", second_diff)
# Output: [2 2 2]  # Constant for n^2
```

**Related Terms:** First Difference, Acceleration

---

### Signal Processing

**Definition:** The analysis and manipulation of signals (time series data). Diff is used for edge detection and change analysis.

**Example:**
```python
import numpy as np

# Detect changes in signal
signal = np.array([0, 0, 1, 1, 0, 0, 1, 0])
changes = np.diff(signal)
print("Changes:", changes)
# Output: [0 1 0 -1 0 1 -1]
```

**Related Terms:** Edge Detection, Diff

---

### Transition

**Definition:** A point where a signal changes from one state to another (e.g., 0 to 1 or 1 to 0).

**Example:**
```python
import numpy import np

signal = np.array([0, 0, 1, 1, 0, 0])
transitions = np.where(np.diff(signal) != 0)[0] + 1
print("Transitions at:", transitions)
# Output: Transitions at: [2 4]
```

**Related Terms:** Edge Detection, Signal Processing

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| append | Add values after | `np.diff(arr, append=100)` |
| axis | Direction of operation | `np.diff(arr, axis=0)` |
| Cumulative Sum | Running total (inverse of diff) | `np.cumsum(diffs)` |
| Discrete Derivative | Approximate derivative | `np.diff(x) / np.diff(t)` |
| diff() | Calculate differences | `np.diff(arr)` |
| Edge Detection | Find transitions | `np.where(np.diff(sig) != 0)` |
| First Difference | Δx[i] = x[i+1] - x[i] | `np.diff(arr)` |
| Higher-Order | Diff of diff | `np.diff(arr, n=2)` |
| Prepend | Add values before | `np.diff(arr, prepend=0)` |
| Rate of Change | How fast values change | `np.diff(prices)` |
| Second Difference | Δ²x[i] | `np.diff(arr, n=2)` |
| Signal Processing | Analyze time series | Edge detection |
| Transition | Change between states | 0→1 or 1→0 |

---

**Back to Lecture:** [26 - Difference Ufuncs](26-ufunc-differences-lecture.md)
