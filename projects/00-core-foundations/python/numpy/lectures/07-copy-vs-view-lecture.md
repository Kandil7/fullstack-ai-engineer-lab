# NumPy Lecture 07: Copy vs View

## 🎯 Topic Overview

Understanding the difference between copies and views is crucial in NumPy. A view shares memory with the original array, while a copy creates independent memory. This distinction affects performance, memory usage, and can lead to subtle bugs if misunderstood.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish between copies and views in NumPy
2. Identify which operations create copies vs views
3. Use `np.shares_memory()` to check memory sharing
4. Control when to create copies explicitly
5. Avoid bugs caused by unintended view modifications
6. Optimize memory usage with views

---

## 1. What is a View?

A view is a new array object that shares the same memory as the original array. Modifying a view modifies the original.

### 1.1 Slicing Creates Views

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Slicing creates a view
view = arr[1:3]
print(view)       # [20 30]

# View shares memory with original
print(np.shares_memory(arr, view))  # True

# Modify the view
view[0] = 999
print(arr)        # [ 10 999  30  40  50] — original modified!

# Modify the original
arr[2] = 777
print(view)       # [999 777] — view modified!
```

### 1.2 View Attributes

```python
arr = np.array([1, 2, 3, 4, 5])

# View shares base
view = arr[1:3]
print(view.base is arr)  # True (view is derived from arr)

# View has same dtype
print(view.dtype == arr.dtype)  # True

# View has different shape
print(view.shape)  # (2,)
print(arr.shape)   # (5,)
```

---

## 2. What is a Copy?

A copy is a new array with its own memory. Modifying the copy does not affect the original.

### 2.1 Explicit Copies

```python
arr = np.array([10, 20, 30, 40, 50])

# Explicit copy using .copy()
copy = arr[1:3].copy()
print(copy)       # [20 30]

# Copy does NOT share memory
print(np.shares_memory(arr, copy))  # False

# Modify the copy
copy[0] = 999
print(arr)        # [10 20 30 40 50] — original unchanged!

# Modify the original
arr[2] = 777
print(copy)       # [20 30] — copy unchanged!
```

### 2.2 np.copy()

```python
arr = np.array([1, 2, 3, 4, 5])

# Using np.copy()
copy = np.copy(arr[1:3])
print(np.shares_memory(arr, copy))  # False
```

---

## 3. Operations That Create Copies

### 3.1 Explicit Copy Operations

```python
arr = np.array([1, 2, 3, 4, 5])

# These all create copies
copy1 = arr.copy()
copy2 = np.copy(arr)
copy3 = arr[1:3].copy()

# Fancy indexing creates copies
copy4 = arr[[0, 2, 4]]

# Boolean indexing creates copies
copy5 = arr[arr > 2]

# .astype() creates copies
copy6 = arr.astype(np.float32)

# np.where() creates copies
copy7 = np.where(arr > 3, 0, arr)

print(np.shares_memory(arr, copy1))  # False
print(np.shares_memory(arr, copy4))  # False
print(np.shares_memory(arr, copy5))  # False
```

### 3.2 Operations That Create Views

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Slicing creates views
view1 = arr[0:2]
view2 = arr[:, 1:3]
view3 = arr[::2]

# Reshape creates view (when possible)
view4 = arr.reshape(9)

# Transpose creates view
view5 = arr.T

# ravel creates view (when possible)
view6 = arr.ravel()

print(np.shares_memory(arr, view1))  # True
print(np.shares_memory(arr, view4))  # True
print(np.shares_memory(arr, view5))  # True
```

---

## 4. When Views Are Forced to Copies

### 4.1 Non-contiguous Memory

```python
arr = np.arange(20).reshape(4, 5)

# Non-contiguous slice
view = arr[::2, ::2]
print(view.flags['C_CONTIGUOUS'])  # False

# reshape on non-contiguous array may create copy
copy = view.reshape(4)
print(np.shares_memory(view, copy))  # May be False!
```

### 4.2 Type Casting

```python
arr = np.array([1, 2, 3], dtype=np.int64)

# astype always creates a copy
copy = arr.astype(np.float32)
print(np.shares_memory(arr, copy))  # False
```

---

## 5. Memory Efficiency

### 5.1 Views Save Memory

```python
import sys

arr = np.arange(1000000)

# View — no extra memory
view = arr[::2]
print(f"Original size: {arr.nbytes:,} bytes")
print(f"View size: {view.nbytes:,} bytes")  # Same element count but...
print(f"View base shares memory: {view.base is not None}")  # True

# Copy — duplicates data
copy = arr[::2].copy()
print(f"Copy size: {copy.nbytes:,} bytes")  # Full copy of data
```

### 5.2 Check Memory Sharing

```python
arr = np.array([1, 2, 3, 4, 5])

view = arr[1:3]
copy = arr[1:3].copy()

# Method 1: np.shares_memory()
print(np.shares_memory(arr, view))   # True
print(np.shares_memory(arr, copy))   # False

# Method 2: Check base attribute
print(view.base is arr)   # True
print(copy.base is arr)   # False

# Method 3: Check memory address
print(arr.ctypes.data == view.ctypes.data)  # True
print(arr.ctypes.data == copy.ctypes.data)  # False
```

---

## 6. Common Bugs and How to Avoid Them

### Bug 1: Unintended Modification

```python
arr = np.array([1, 2, 3, 4, 5])

# BUG — modifying view modifies original
temp = arr[1:3]
temp[0] = 999
print(arr)  # [ 1 999  3  4  5] — unexpected!

# FIX — use .copy()
temp = arr[1:3].copy()
temp[0] = 999
print(arr)  # [1 2 3 4 5] — unchanged
```

### Bug 2: Chained Indexing

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# BUG — chained indexing creates copy, doesn't modify original
arr[0:2][0:2] = 0
print(arr)  # Unchanged!

# FIX — use direct indexing
arr[0:2, 0:2] = 0
print(arr)
# [[0 0 3]
#  [0 0 6]
#  [7 8 9]]
```

### Bug 3: Broadcasting with Views

```python
arr = np.array([1, 2, 3, 4, 5])

# View
view = arr[1:3]

# Broadcasting may create temporary copy
view + np.array([10, 20])  # This is fine

# But assignment with broadcasting
# view[:] = view + np.array([10, 20])  # Modifies original!
```

---

## 7. Best Practices

1. **Use `.copy()`** when you need independent data
2. **Check `np.shares_memory()`** if unsure about memory sharing
3. **Avoid modifying views** unless you intend to modify the original
4. **Use direct indexing** instead of chained indexing for assignment
5. **Be careful with `reshape()`** — it may create a copy if needed
6. **Prefer views** for performance when you don't need copies
7. **Document memory behavior** in functions that return views

---

## 8. Practice Exercises

### Exercise 1: View vs Copy
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Create a view and a copy
view = arr[1:4]
copy = arr[1:4].copy()

# Modify the view
view[0] = 999

# Question: What is arr now? What about copy?
print(f"arr: {arr}")      # [ 10 999  30  40  50]
print(f"copy: {copy}")    # [20 30 40]

# Verify memory sharing
print(f"shares_memory(arr, view): {np.shares_memory(arr, view)}")   # True
print(f"shares_memory(arr, copy): {np.shares_memory(arr, copy)}")   # False
```

### Exercise 2: Operations Creating Views
```python
arr = np.arange(20).reshape(4, 5)

# Which of these create views?
operations = [
    arr[0:2],
    arr[:, 1:3],
    arr[::2],
    arr.T,
    arr.reshape(20),
    arr.ravel(),
    arr.flatten(),  # This creates a copy!
]

for i, op in enumerate(operations):
    is_view = np.shares_memory(arr, op)
    print(f"Operation {i}: {'View' if is_view else 'Copy'}")
```

### Exercise 3: Memory Efficiency
```python
import sys

arr = np.arange(1000000)

# Compare memory usage
view = arr[::2]
copy = arr[::2].copy()

print(f"Original: {arr.nbytes:,} bytes")
print(f"View: {view.nbytes:,} bytes (but shares memory)")
print(f"Copy: {copy.nbytes:,} bytes (independent)")
```

### Exercise 4: Bug Detection
```python
# Find and fix the bug
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# This doesn't work as expected
arr[0:2][0:2] = 0
print("After chained indexing:", arr)

# Fix it
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr[0:2, 0:2] = 0
print("After direct indexing:", arr)
```

---

## 9. Summary

| Operation | Creates | Memory | Modifies Original? |
|-----------|---------|--------|---------------------|
| `arr[1:3]` | View | Shared | Yes |
| `arr[1:3].copy()` | Copy | Independent | No |
| `arr[[0, 2, 4]]` | Copy | Independent | No |
| `arr[arr > 0]` | Copy | Independent | No |
| `arr.reshape(n)` | View | Shared | Yes |
| `arr.T` | View | Shared | Yes |
| `arr.ravel()` | View | Shared | Yes |
| `arr.flatten()` | Copy | Independent | No |
| `arr.astype(dtype)` | Copy | Independent | No |
| `np.where(cond, x, y)` | Copy | Independent | No |

### Key Takeaways

1. **Views** share memory with the original — modifications affect both
2. **Copies** have independent memory — modifications are isolated
3. **Slicing** creates views; **fancy/boolean indexing** creates copies
4. Use **`.copy()`** when you need independent data
5. Use **`np.shares_memory()`** to check memory sharing
6. **Avoid modifying views** unless you intend to modify the original
7. **Views are more memory-efficient** than copies

---

## 🔗 Next Lecture

→ [08-array-shape-lecture.md](./08-array-shape-lecture.md) — Array Shape
