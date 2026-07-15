# SciPy Lecture 09: Fast Fourier Transform (FFT)

## 🎯 Topic Overview

The FFT transforms signals from time domain to frequency domain, revealing periodic components, frequencies, and spectral characteristics.

## 📚 Learning Objectives

1. Compute FFT and inverse FFT with `scipy.fft`
2. Understand frequency domain representation
3. Apply FFT for signal filtering and analysis

---

## 1. Basic FFT

```python
import numpy as np
from scipy import fft
import matplotlib.pyplot as plt

# Generate signal
fs = 1000  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)
f1, f2 = 50, 120  # Signal frequencies
signal = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)

# Compute FFT
X = fft.fft(signal)
freqs = fft.fftfreq(len(signal), 1/fs)

# Only positive frequencies
pos_mask = freqs >= 0
magnitude = np.abs(X[pos_mask]) / len(signal)

print(f"Peak frequencies: {freqs[pos_mask][magnitude > 0.3]}")
```

---

## 2. Signal Filtering

```python
# Remove high frequency noise
cutoff = 80  # Hz cutoff
X_filtered = X.copy()
X_filtered[np.abs(freqs) > cutoff] = 0

# Inverse FFT
filtered_signal = fft.ifft(X_filtered).real

# Power spectral density
from scipy import signal as sg
f, psd = sg.periodogram(signal, fs)
print(f"Max power at frequency: {f[np.argmax(psd)]:.1f} Hz")
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `fft()` | Forward FFT |
| `ifft()` | Inverse FFT |
| `fftfreq()` | Frequency bins |
| `rfft()` | Real-valued FFT |
| `fftshift()` | Shift zero frequency to center |
