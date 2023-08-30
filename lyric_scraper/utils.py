import functools
import logging
import time

logging.basicConfig(level=logging.INFO)

def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Running '{func.__name__}'.")
        result = func(*args, **kwargs)
        logging.info(f"'{func.__name__}' completed.")
        return result
    return wrapper

def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper