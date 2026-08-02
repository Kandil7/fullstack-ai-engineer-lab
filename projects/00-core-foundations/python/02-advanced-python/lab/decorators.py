
# ### Exercise 1: Basic Decorator
# Write a `@debug` decorator that prints the function name, arguments, and return value:

# ```python
# @debug
# def add(a, b):
#     return a + b

# # Expected output:
# # Calling add(3, 5)
# # add returned 8
# ```


# def timer(func: Callable) -> Callable:
#     """Measure execution time of a function."""
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         elapsed = time.perf_counter() - start
#         print(f"  [{func.__name__}] executed in {elapsed:.6f}s")
#         return result
#     return wrapper


# def log_calls(func: Callable) -> Callable:
#     """Log function calls with arguments."""
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         args_str = ", ".join([repr(a) for a in args])
#         kwargs_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
#         all_args = ", ".join(filter(None, [args_str, kwargs_str]))
#         print(f"  Calling {func.__name__}({all_args})")
#         result = func(*args, **kwargs)
#         print(f"  {func.__name__} returned {result!r}")
#         return result
#     return wrapper

import time 
import functools

def debug(func):
    """debug decorator that prints the function name , arguments and return value"""
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        args_str=", ".join([repr(a) for a in args])
        kwargs_str =", ".join([f"{k}={v!r}" for k , v in kwargs.items()])
        all_args=", ".join(filter(None,[args_str,kwargs_str]))
        print(f"Calling {func.__name__}({all_args})")
        result=func(*args,**kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# @debug
# def add(a, b):
#     return a + b

# add(3, 5)
