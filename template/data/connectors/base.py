# -*- coding: utf-8 -*-
"""Define the interface for all data connectors."""
from abc import ABC, abstractmethod

import pandas as pd


class BaseConnector(ABC):
    """Define the interface for all data connectors."""

    @abstractmethod
    def read_dataframe(self, name: str, **kwargs) -> pd.DataFrame:
        """Read DataFrame.

        :param name: Name of data object to read from.
        :return: Retrieved DataFrame.
        """
        pass

    @abstractmethod
    def write_dataframe(self, name: str, df: pd.DataFrame, **kwargs) -> None:
        """Write DataFrame.

        :param name: Name of data object to write to.
        :param df: DataFrame to write.
        """
        pass
