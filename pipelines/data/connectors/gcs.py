"""Define data connector to interact with GCS."""

from io import StringIO
from pathlib import Path
from typing import Self

import pandas as pd
from google.cloud import storage

from pipelines.data.connectors.base_file import BaseFileConnector
from pipelines.utils.constants import FORMAT_TO_OPTIONS, FileFormat
from pipelines.utils.file import get_file_format, get_file_path_as_str
from pipelines.utils.strings import to_str


class GcsConnector(BaseFileConnector):
    """Define data connector to interact with Google Cloud Storage."""

    def __init__(self: Self, bucket_name: str, path: str) -> None:
        """Initialize data connector.

        :param bucket_name: Name of the GCS bucket.
        """
        self.client = storage.Client()
        self.bucket_name = bucket_name
        # Pyright error: Argument missing for parameter "self" (reportCallIssue).
        self.bucket = self.client.get_bucket(
            bucket_or_name=bucket_name,
        )  # pyright: ignore[reportCallIssue]
        self.path = Path(path)

    def _validate_path(self: Self, path: Path) -> None:
        """Validate path.

        :param path: Path to validate.
        :raises: FileNotFoundError if path does not exist
        """
        blobs = self.bucket.list_blobs(prefix=path, max_results=1)
        if not blobs:
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
        directory_path = self.path / directory_path
        self._validate_path(directory_path)

        blobs = self.bucket.list_blobs(prefix=directory_path)
        blob_names = [blob.name for blob in blobs]
        if file_format:
            return [name for name in blob_names if name.lower().endswith(file_format)]
        return blob_names

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
        file_path = get_file_path_as_str(
            self.path,
            data_object_name,
            file_format,
        )

        blob = self.bucket.blob(file_path)
        data = blob.download_as_text()
        match file_format:
            case FileFormat.CSV:
                return pd.read_csv(
                    StringIO(data),
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
        file_path = get_file_path_as_str(
            self.path,
            data_object_name,
            file_format,
        )
        # NOTE: Creation of directories is not required as GCS has a flat namespace.
        buffer = StringIO()
        match file_format:
            case FileFormat.CSV:
                df.to_csv(
                    buffer,
                    index=False,
                    **FORMAT_TO_OPTIONS[file_format],
                )
            case _:
                error_message = f"File format {file_format} not implemented yet"
                raise NotImplementedError(error_message)
        self.bucket.blob(file_path).upload_from_string(buffer.getvalue())

    def copy(
        self: Self,
        source_path: Path,
        target_path: Path,
    ) -> None:
        """Copy files or folders.

        :param source_path: Source path to copy from.
        :param target_path: Target path to copy to.
        """
        source_path = self.path / source_path
        self._validate_path(source_path)

        target_path = self.path / target_path
        blobs = self.bucket.list_blobs(prefix=source_path)
        for blob in blobs:
            new_blob_name = blob.name.replace(source_path, target_path, count=1)
            self.bucket.copy_blob(blob, self.bucket, new_blob_name)

    def move(
        self: Self,
        source_path: Path,
        target_path: Path,
    ) -> None:
        """Move files or folders.

        :param source_path: Source path to move from.
        :param target_path: Target path to move to.
        """
        source_path = self.path / source_path
        self._validate_path(source_path)

        target_path = self.path / target_path
        blobs = self.bucket.list_blobs(prefix=source_path)
        for blob in blobs:
            new_blob_name = blob.name.replace(source_path, target_path, count=1)
            self.bucket.copy_blob(blob, self.bucket, new_blob_name)
            blob.delete()

    def delete(
        self: Self,
        path: Path,
    ) -> None:
        """Delete files or folders.

        :param path: Path to delete.
        """
        path = self.path / path
        self._validate_path(path)

        blobs = self.bucket.list_blobs(prefix=path)
        for blob in blobs:
            blob.delete()
