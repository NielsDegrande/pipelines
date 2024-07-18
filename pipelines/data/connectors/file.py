"""Define data connector to interact with files."""

import shutil
from pathlib import Path
from typing import Self

import pandas as pd

from pipelines.data.connectors.base_file import BaseFileConnector
from pipelines.utils.constants import FORMAT_TO_OPTIONS, FileFormat
from pipelines.utils.file import get_file_format, get_file_path
from pipelines.utils.string import to_str


class FileConnector(BaseFileConnector):
    """Define data connector to interact with files."""

    def _validate_path(
        self: Self,
        path: Path,
    ) -> None:
        """Validate path.

        :param path: Path to validate.
        :raises: FileNotFoundError if path does not exist
        """
        if not path.exists():
            error_message = f"The path '{path}' does not exist."
            raise FileNotFoundError(error_message)

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
        self._validate_path(directory_path)

        file_paths = [
            file_path for file_path in directory_path.rglob("*") if file_path.is_file()
        ]
        if file_format:
            return [
                file_path
                for file_path in file_paths
                if file_path.suffix.lower() == file_format
            ]
        return file_paths

    def read_dataframe(
        self: Self,
        data_object_name: str,
        **kwargs: dict,
    ) -> pd.DataFrame:
        """Read DataFrame.

        :param data_object_name: Data object to read.
        :raises: NotImplementedError if file format is not implemented yet.
        :return: Retrieved DataFrame.
        """
        file_format = get_file_format(to_str(kwargs.get("format")))
        file_path = get_file_path(
            to_str(kwargs.get("path")),
            data_object_name,
            file_format,
        )
        match file_format:
            case FileFormat.CSV:
                return pd.read_csv(
                    file_path,
                    **FORMAT_TO_OPTIONS[file_format],
                )
            case _:
                error_message = f"File format {file_format} not implemented yet"
                raise NotImplementedError(error_message)

    def write_dataframe(
        self: Self,
        data_object_name: str,
        df: pd.DataFrame,
        **kwargs: dict,
    ) -> None:
        """Write DataFrame.

        :param data_object_name: Data object to write.
        :param df: DataFrame to write.
        :raises: NotImplementedError if file format is not implemented yet.
        """
        file_format = get_file_format(to_str(kwargs.get("format")))
        file_path = get_file_path(
            to_str(kwargs.get("path")),
            data_object_name,
            file_format,
        )
        file_path.parent.mkdir(parents=True, exist_ok=True)
        match file_format:
            case FileFormat.CSV:
                return df.to_csv(
                    file_path,
                    index=False,
                    **FORMAT_TO_OPTIONS[file_format],
                )
            case _:
                error_message = f"File format {file_format} not implemented yet"
                raise NotImplementedError(error_message)

    def copy(
        self: Self,
        source_path: Path,
        target_path: Path,
    ) -> None:
        """Copy files or folders.

        :param source_path: Source path to copy from.
        :param target_path: Target path to copy to.
        """
        self._validate_path(source_path)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, target_path)

    def move(
        self: Self,
        source_path: Path,
        target_path: Path,
    ) -> None:
        """Move files or folders.

        :param source_path: Source path to move from.
        :param target_path: Target path to move to.
        """
        self._validate_path(source_path)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.rename(target_path)

    def delete(
        self: Self,
        path: Path,
    ) -> None:
        """Delete files or folders.

        :param path: Path to delete.
        """
        self._validate_path(path)

        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
