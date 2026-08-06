# Challenge 44 — Quiz: Logging

1. What is the default root threshold if you do not configure anything?
   - A) DEBUG  (B) INFO  (C) WARNING  (D) ERROR
2. `logger.exception("x")` logs at which level?
   - A) INFO  (B) WARNING  (C) ERROR  (D) CRITICAL
3. Duplicate log lines usually come from:
   - A) too many handlers on one logger  (B) propagation to the root  (C) both  (D) neither
4. Lazy `%s` formatting:
   - A) is slower  (B) formats only when the record is emitted  (C) breaks messages  (D) is deprecated
5. `propagate=False` on a logger means:
   - A) records stop at this logger  (B) the logger logs nothing  (C) handlers are removed  (D) level resets
6. Which is the correct per-module idiom?
   - A) `logging.info(...)`  (B) `logger = logging.getLogger(__name__)`  (C) `print(...)`  (D) `logging.basicLogger`
7. Structured logging means:
   - A) colorful output  (B) machine-readable fields (e.g. JSON)  (C) sorted timestamps  (D) fewer lines
8. `logging.config.dictConfig` is used to:
   - A) rotate files  (B) declare loggers/handlers/formatters  (C) measure latency  (D) catch exceptions

**Answers:** 1-C, 2-C, 3-B, 4-B, 5-A, 6-B, 7-B, 8-B
