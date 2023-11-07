"""Define the interface for all file data connectors."""

from abc import abstractmethod
from pathlib import Path
from typing import Self

from pipelines.data.connectors.base import BaseConnector


class BaseFileConnector(BaseConnector):
    """Define the interface for all file data connectors."""

    @abstractmethod
    def list_files(
        self: Self,
        directory_path: Path,
        file_extension: str,
    ) -> list[Path]:
        """List all files in directory that match extension.

        :param directory_path: Directory to search.
        :param file_extension: Extension to match.
        :return: All files within directory that match extension.
        """
