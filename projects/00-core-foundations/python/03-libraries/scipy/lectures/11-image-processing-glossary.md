# SciPy Lecture 11: Image Processing — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| Gaussian Filter | Smoothing with Gaussian kernel | `ndimage.gaussian_filter(img, sigma=2)` |
| Median Filter | Noise reduction | `ndimage.median_filter(img, size=5)` |
| Sobel Filter | Edge detection | `ndimage.sobel(img)` |
| Erosion | Shrink foreground objects | `ndimage.binary_erosion(binary)` |
| Dilation | Expand foreground objects | `ndimage.binary_dilation(binary)` |
| Opening | Erosion then dilation | `ndimage.binary_opening(binary)` |
| Closing | Dilation then erosion | `ndimage.binary_closing(binary)` |
| Connected Components | Label distinct objects | `ndimage.label(binary)` |
| Center of Mass | Object centroid | `ndimage.center_of_mass(img, labels, idx)` |

### Filtering Comparison

| Filter | Best For | Trade-off |
|--------|----------|-----------|
| Gaussian | General smoothing | Blurs edges |
| Median | Salt-and-pepper noise | Preserves edges |
| Sobel | Edge detection | Sensitive to noise |
