# Challenge 52 — Quiz: Memory & Performance

1. 1M x 768 float32 embeddings ≈:
   - A) 0.3 GB  (B) 3 GB  (C) 30 GB  (D) 300 MB
2. `sys.getsizeof(list)` reports:
   - A) full deep size  (B) header + direct refs only  (C) element sizes  (D) nothing
3. `__slots__` saves memory by:
   - A) compressing values  (B) removing the per-instance dict  (C) using numpy  (D) caching
4. `s += c` in a loop is:
   - A) O(n)  (B) O(n^2)  (C) O(log n)  (D) O(1)
5. The GIL means threads:
   - A) never help  (B) help I/O waits, not CPU loops  (C) help CPU loops  (D) are deprecated
6. Small ints -5..256 are:
   - A) always separate  (B) cached/interned  (C) never equal  (D) floats
7. `is` should be used for:
   - A) value comparison  (B) `None` and singletons  (C) strings  (D) floats
8. `memoryview` slicing is:
   - A) copying  (B) zero-copy  (C) slower  (D) deprecated

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
