"""Define the interface for all data connectors."""
from abc import ABC, abstractmethod
from typing import Self

import pandas as pd


class BaseConnector(ABC):
    """Define the interface for all data connectors."""

    @abstractmethod
    def read_dataframe(
        self: Self,
        name: str,
        **kwargs: dict,
    ) -> pd.DataFrame:
        """Read DataFrame.

        :param name: Name of data object to read from.
        :return: Retrieved DataFrame.
        """

    @abstractmethod
    def write_dataframe(
        self: Self,
        name: str,
        df: pd.DataFrame,
        **kwargs: dict,
    ) -> None:
        """Write DataFrame.

        :param name: Name of data object to write to.
        :param df: DataFrame to write.
        """
