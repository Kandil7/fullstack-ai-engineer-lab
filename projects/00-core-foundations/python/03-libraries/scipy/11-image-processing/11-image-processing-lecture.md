# SciPy Lecture 11: Image Processing

## 🎯 Topic Overview

SciPy's `ndimage` module provides powerful multidimensional image processing functions for filtering, morphology, segmentation, and measurement.

## 📚 Learning Objectives

1. Apply filters (Gaussian, median, Sobel) to images
2. Perform morphological operations (dilation, erosion)
3. Label and measure connected components

---

## 1. Image Filtering

```python
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Create sample image
image = np.random.random((100, 100))
image[30:70, 30:70] = 0.8  # Add a bright square

# Add noise
noisy = image + np.random.normal(0, 0.2, image.shape)
noisy = np.clip(noisy, 0, 1)

# Filters
smoothed = ndimage.gaussian_filter(noisy, sigma=2)
median = ndimage.median_filter(noisy, size=5)

# Edge detection
edges = ndimage.sobel(noisy)
edges_magnitude = np.sqrt(edges[0]**2 + edges[1]**2)

print(f"Original mean: {image.mean():.3f}")
print(f"Smoothed mean: {smoothed.mean():.3f}")
```

---

## 2. Morphological Operations

```python
# Create binary image
binary = np.zeros((50, 50))
binary[20:30, 20:30] = 1

# Erosion
eroded = ndimage.binary_erosion(binary, iterations=2)

# Dilation
dilated = ndimage.binary_dilation(binary, iterations=2)

# Opening (erosion then dilation)
opened = ndimage.binary_opening(binary, iterations=2)

# Closing (dilation then erosion)
closed = ndimage.binary_closing(binary, iterations=2)

print(f"Original pixels: {binary.sum()}")
print(f"Eroded pixels: {eroded.sum()}")
print(f"Dilated pixels: {dilated.sum()}")
```

---

## 3. Connected Components

```python
# Label connected components
labeled, num_features = ndimage.label(binary)
print(f"Number of features: {num_features}")

# Find center of mass for each component
centers = ndimage.center_of_mass(binary, labeled, range(1, num_features+1))
print(f"Centers of mass: {centers}")

# Measure properties
from scipy.ndimage import find_objects
slices = find_objects(labeled)
for i, slice_obj in enumerate(slices, 1):
    area = (labeled[slice_obj] == i).sum()
    print(f"Component {i}: area = {area}")
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `gaussian_filter()` | Smoothing |
| `sobel()` | Edge detection |
| `binary_erosion()` | Shrink features |
| `binary_dilation()` | Expand features |
| `label()` | Connected components |
| `center_of_mass()` | Object centroids |
