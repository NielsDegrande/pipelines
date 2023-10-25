"""Utility functions for files."""

from pathlib import Path

from pipelines.utils.constants import FORMAT_TO_EXTENSION, FileFormats


def get_file_format(file_format: str | None) -> FileFormats:
    """Get file format.

    :param file_format: Format of the file.
    :raises: ValueError if file format is not supported.
    :return: File format.
    """
    match file_format:
        case FileFormats.CSV:
            return FileFormats.CSV
        case None:
            # Default to CSV if no format specified in connector config,
            # or given by pipeline.
            return FileFormats.CSV
        case _:
            error_message = f"Unsupported file format: {file_format}"
            raise ValueError(error_message)


def get_file_path(path: str | Path | None, name: str, file_format: FileFormats) -> Path:
    """Get file path.

    :param path: Path to the folder.
    :param name: Name of the file.
    :param file_format: Format of the file.
    :return: Path to the file.
    """
    file_name = f"{name}{FORMAT_TO_EXTENSION[file_format]}"
    path = "" if path is None else path
    return Path(path) / file_name


def get_file_path_as_str(
    path: str | Path | None,
    name: str,
    file_format: FileFormats,
) -> str:
    """Get file path.

    :param path: Path to the folder.
    :param name: Name of the file.
    :param file_format: Format of the file.
    :return: Path to the file.
    """
    return str(get_file_path(path, name, file_format))
