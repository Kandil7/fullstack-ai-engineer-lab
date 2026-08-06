# Challenge 47 — Quiz: Advanced Exceptions

1. Which is the correct package base pattern?
   - A) raise `Exception` everywhere  (B) one base + subclasses  (C) only ValueError  (D) no custom exceptions
2. `raise X from e` sets:
   - A) `__context__` only  (B) `__cause__`  (C) `__traceback__`  (D) nothing
3. `ExceptionGroup` lets you:
   - A) nest logs  (B) raise many exceptions as one  (C) group threads  (D) retry automatically
4. `except*` handles:
   - A) regular exceptions  (B) exceptions inside a group by type  (C) only the first  (D) BaseException only
5. Retrying a 400 error:
   - A) is harmless  (B) wastes money — it will fail again  (C) is required  (D) fixes it
6. A `return` inside `finally`:
   - A) is ignored  (B) overrides the try's return  (C) raises  (D) is deprecated
7. EAFP stands for:
   - A) Errors Are Forgiven Programmatically  (B) Easier to Ask Forgiveness than Permission  (C) Exception And Failure Prevention  (D) Everything Always Fails Properly
8. Bare `except:` is dangerous because it also catches:
   - A) TypeError  (B) KeyboardInterrupt and SystemExit  (C) only KeyError  (D) nothing extra

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
