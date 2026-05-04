import logging
from rich.logging import RichHandler

def get_logger(name: str) -> logging.Logger:
    """Return a logger with RichHandler for pretty console output.

    The logger is configured once per process. Subsequent calls return the same
    logger instance. Caller provides a module name for context.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = RichHandler(show_time=True, show_level=True, markup=True)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
