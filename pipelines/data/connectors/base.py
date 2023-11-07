"""Define the interface for all data connectors."""

from abc import ABC, abstractmethod
from typing import Self

import pandas as pd


class BaseConnector(ABC):
    """Define the interface for all data connectors."""

    @abstractmethod
    def read_dataframe(
        self: Self,
        data_object_name: str,
        **kwargs: dict,
    ) -> pd.DataFrame:
        """Read DataFrame.

        :param data_object_name: Data object to read.
        :return: Retrieved DataFrame.
        """

    @abstractmethod
    def write_dataframe(
        self: Self,
        data_object_name: str,
        df: pd.DataFrame,
        **kwargs: dict,
    ) -> None:
        """Write DataFrame.

        :param data_object_name: Data object to write.
        :param df: DataFrame to write.
        """
