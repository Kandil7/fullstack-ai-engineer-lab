# SciPy Lecture 12: Input/Output — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| savemat | Save MATLAB .mat file | `io.savemat('file.mat', data)` |
| loadmat | Load MATLAB .mat file | `io.loadmat('file.mat')` |
| wavfile.write | Save WAV audio | `wavfile.write('file.wav', rate, sig)` |
| wavfile.read | Load WAV audio | `rate, data = wavfile.read('file.wav')` |
| mmwrite | Save Matrix Market format | `mmwrite('file.mtx', sparse_mat)` |
| mmread | Load Matrix Market format | `mmread('file.mtx')` |
| PCM | Pulse Code Modulation (audio format) | `np.int16` for 16-bit audio |
| Sampling Rate | Audio samples per second | 44100 Hz (CD quality) |
