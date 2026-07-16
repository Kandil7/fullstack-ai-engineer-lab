# SciPy Lecture 12: Input/Output

## 🎯 Topic Overview

SciPy provides input/output functions for reading/writing MATLAB files, WAV audio files, and other scientific data formats.

## 📚 Learning Objectives

1. Read and write MATLAB .mat files
2. Handle audio files (WAV)
3. Work with sparse matrix market format

---

## 1. MATLAB File I/O

```python
from scipy import io
import numpy as np

# Create data
data = {
    'array': np.array([1, 2, 3, 4, 5]),
    'matrix': np.eye(3),
    'string': 'hello',
}

# Save to .mat file
io.savemat('data.mat', data)

# Load from .mat file
loaded = io.loadmat('data.mat')
print(f"Loaded array: {loaded['array']}")
print(f"Loaded matrix:\n{loaded['matrix']}")

# Read MATLAB v5, v7, v7.3 files
# io.loadmat handles .mat versions 5 and 7
# For v7.3, use h5py instead
```

---

## 2. WAV Audio I/O

```python
from scipy.io import wavfile

# Generate audio signal
sample_rate = 44100  # Hz
duration = 2  # seconds
t = np.linspace(0, duration, int(sample_rate * duration))
signal = np.sin(2 * np.pi * 440 * t)  # A4 note (440 Hz)

# Convert to 16-bit PCM
signal_int16 = (signal * 32767).astype(np.int16)

# Write WAV file
wavfile.write('tone.wav', sample_rate, signal_int16)

# Read WAV file
rate, data = wavfile.read('tone.wav')
print(f"Sample rate: {rate} Hz")
print(f"Data shape: {data.shape}")
print(f"Duration: {len(data)/rate:.2f}s")
```

---

## 3. Other I/O Formats

```python
# Matrix Market format (sparse matrices)
from scipy.io import mmread, mmwrite
from scipy.sparse import csr_matrix

sparse_mat = csr_matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
mmwrite('matrix.mtx', sparse_mat)
loaded_sparse = mmread('matrix.mtx')
print(f"Loaded sparse matrix:\n{loaded_sparse.toarray()}")

# ARFF format (Weka data files)
# from scipy.io import arff (deprecated, use pandas.read_csv instead)
```

---

## Summary

```python
from scipy import io, misc

# File I/O summary
io.savemat('file.mat', data_dict)     # Save MATLAB .mat
io.loadmat('file.mat')                 # Load MATLAB .mat
io.wavfile.write('file.wav', rate, sig) # Save WAV audio
io.wavfile.read('file.wav')            # Load WAV audio
```

> **Note**: For CSV, JSON, Excel, or HDF5 files, use `pandas`, `h5py`, or `netCDF4` — they're more feature-rich than SciPy's I/O for those formats.
