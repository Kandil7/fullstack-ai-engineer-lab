# SciPy Lecture 09: FFT — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| FFT | Fast Fourier Transform | `fft.fft(signal)` |
| IFFT | Inverse FFT | `fft.ifft(X)` |
| Frequency Domain | Signal representation by frequency | `fft.fftfreq(n, dt)` |
| Time Domain | Signal representation by time | Original signal |
| Power Spectrum | Squared magnitude of FFT | `periodogram(signal, fs)` |
| Nyquist Frequency | Maximum detectable frequency | `fs / 2` |
| Sampling Rate | Samples per second (Hz) | `fs = 1000` |
| Aliasing | Frequency folding artifact | Occurs above Nyquist |
| `fftfreq()` | Frequency bin centers | `freqs = fftfreq(N, 1/fs)` |
| `fftshift()` | Center zero frequency | `fft.fftshift(X)` |
| `rfft()` | Real-valued FFT (faster) | `fft.rfft(signal)` |
