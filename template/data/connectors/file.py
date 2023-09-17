# -*- coding: utf-8 -*-
"""Define data connector to interact with files."""

import os
from pathlib import Path

import pandas as pd

from template.data.connectors.base import BaseConnector


class FileConnector(BaseConnector):
    """Define data connector to interact with files."""

    def __init__(self):
        """Initialize data connector."""
        super().__init__()

    def read_dataframe(self, name: str, **kwargs) -> pd.DataFrame:
        """Read DataFrame.

        :param name: Name of data object to read from.
        :return: Retrieved DataFrame.
        """
        if "format" in kwargs:
            name = f"{name}.{kwargs['format']}"
        file_path = Path(name)

        if "path" in kwargs:
            file_path = kwargs["path"] / file_path
        return pd.read_csv(file_path)

    def write_dataframe(self, name: str, df: pd.DataFrame, **kwargs) -> None:
        """Write DataFrame.

        :param name: Name of data object to write to.
        :param df: DataFrame to write.
        """
        if "format" in kwargs:
            name = f"{name}.{kwargs['format']}"

        file_path = Path(name)
        if "path" in kwargs:
            file_path = kwargs["path"] / file_path
        os.makedirs(file_path.parent, exist_ok=True)

        return df.to_csv(file_path, index=False)
