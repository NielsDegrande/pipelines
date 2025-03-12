"""Utility functions for strings."""

from typing import Any


def to_str(value: Any) -> str | None:  # noqa: ANN401
    """Cast to string if value is not None.

    :param value: Value to cast as string
    :return: String or None.
    """
    return str(value) if value is not None else None
