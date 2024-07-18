"""Define the interface for all file data connectors."""

from abc import abstractmethod
from pathlib import Path
from typing import Self

from pipelines.data.connectors.base import BaseConnector
from pipelines.utils.constants import FileFormat


class BaseFileConnector(BaseConnector):
    """Define the interface for all file data connectors."""

    def _validate_path(
        self: Self,
        path: Path,
    ) -> None:
        """Validate file path.

        :param path: File path to validate.
        :raises: FileNotFoundError if path does not exist
        """
        if not path.exists():
            error_message = f"The path '{path}' does not exist."
            raise FileNotFoundError(error_message)

    @abstractmethod
    def list_files(
        self: Self,
        directory_path: Path,
        file_format: FileFormat | None = None,
    ) -> list[Path]:
        """List all files in directory that match extension.

        :param directory_path: Directory to search.
        :param file_format: Extension to match.
        :return: All files within directory that match extension.
        """

    @abstractmethod
    def copy(
        self: Self,
        source_path: Path,
        target_path: Path,
    ) -> None:
        """Copy files or folders.

        :param source_path: Source path to copy from.
        :param target_path: Target path to copy to.
        """

    @abstractmethod
    def move(
        self: Self,
        source_path: Path,
        target_path: Path,
    ) -> None:
        """Move files or folders.

        :param source_path: Source path to move from.
        :param target_path: Target path to move to.
        """

    @abstractmethod
    def delete(
        self: Self,
        path: Path,
    ) -> None:
        """Delete files or folders.

        :param path: Path to delete.
        """
