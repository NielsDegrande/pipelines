# -*- coding: utf-8 -*-
"""Timing decorator to display execution time."""

import datetime
import logging
import time
from functools import wraps
from typing import Callable


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
    def wrapper(*args, **kwargs):
        """Wrap callable with timing."""
        start_time = time.time()
        result = callable_(*args, **kwargs)
        elapsed = str(datetime.timedelta(seconds=round((time.time() - start_time), 0)))
        log_ = logging.getLogger(__name__)
        log_.info(f"Run time: {_get_full_name(callable_)} ran in {elapsed}")
        return result

    return wrapper
