"""Define the interface for all file data connectors."""

from abc import abstractmethod
from pathlib import Path
from typing import Self

from pipelines.data.connectors.base import BaseConnector
from pipelines.utils.constants import FileFormat


class BaseFileConnector(BaseConnector):
    """Define the interface for all file data connectors."""

    @abstractmethod
    def list_files(
        self: Self,
        directory_path: Path,
        file_format: FileFormat,
    ) -> list[Path]:
        """List all files in directory that match extension.

        :param directory_path: Directory to search.
        :param file_format: Extension to match.
        :return: All files within directory that match extension.
        """
