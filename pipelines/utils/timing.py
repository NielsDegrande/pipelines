"""Timing decorator to display execution time."""

import datetime
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def _get_full_name(callable_: Callable) -> str:
    """Generate the full name for a function.

    :param callable_: Function or method to get full name for.
    :return: Full name of function.
    """
    if not callable_.__module__:
        return callable_.__qualname__
    return f"{callable_.__module__}.{callable_.__qualname__}"


def timing(callable_: Callable) -> Callable:
    """Time execution of given function.

    :param callable_: Function or method to time.
    :return: Function wrapped with timer.
    """

    @wraps(callable_)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:  # noqa: ANN401
        """Wrap callable with timing."""
        start_time = time.time()
        result = callable_(*args, **kwargs)
        # Round to the nearest second.
        elapsed_seconds = round((time.time() - start_time), 0)
        # Format as a timedelta in HH:MM:SS.
        elapsed_time = datetime.timedelta(seconds=elapsed_seconds)
        log_ = logging.getLogger(__name__)
        log_.info("Run time: %s ran in %s.", _get_full_name(callable_), elapsed_time)
        return result

    return wrapper
