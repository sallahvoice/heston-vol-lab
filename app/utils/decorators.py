import time
from functools import wraps
from app.core.logger import get_logger


logger = get_logger(__name__)

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(__name__)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        logger.info(f"{func.__name__} took {(end - start) * 1000:.8f} ms to execute")
        
        return result
    return wrapper


def log_optimizer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(__name__)

        result = func(*args, **kwargs)

        logger.info(
            f"Optimization finished | success={result.success}"
            f"| iterations={result.nit} | error={result.fun}"
        )

        return result
    return wrapper

#retry function as a decorator?