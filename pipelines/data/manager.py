"""Module to abstract all data writing."""

from pathlib import Path

from box import Box

from pipelines.data.connectors import get_data_connector, get_data_connector_config
from pipelines.data.connectors.base_file import BaseFileConnector
from pipelines.utils.constants import FileFormat
from pipelines.utils.exceptions import InvalidConnectorError


def list_files(
    config: Box,
    directory_path: Path | str,
    connector_key: str = "input",
    file_format: FileFormat | None = None,
) -> list[Path]:
    """List all files in directory that match extension.

    :param config: Config to use for data listing.
    :param directory_path: Directory to search.
    :param connector_key: Key of the connector to use.
    :param file_format: Extension to match.
    :return: All files within directory that match extension.
    """
    connector_config = get_data_connector_config(config, connector_key)
    connector = get_data_connector(connector_config)

    if not isinstance(connector, BaseFileConnector):
        message = "This method is only supported for file connectors."
        raise InvalidConnectorError(message)

    connector_path = Path(connector_config.path)
    return connector.list_files(
        connector_path / directory_path,
        file_format,
    )


def copy(
    config: Box,
    source_path: Path | str,
    target_path: Path | str,
    connector_key: str = "output",
) -> None:
    """Copy files or folders.

    :param config: Config to use for data copying.
    :param source_path: Source path to copy from.
    :param target_path: Target path to copy to.
    :param connector_key: Key of the connector to use.
    """
    connector_config = get_data_connector_config(config, connector_key)
    connector = get_data_connector(connector_config)

    if not isinstance(connector, BaseFileConnector):
        message = "This method is only supported for file connectors."
        raise InvalidConnectorError(message)

    connector_path = Path(connector_config.path)
    connector.copy(
        connector_path / source_path,
        connector_path / target_path,
    )


def move(
    config: Box,
    source_path: Path | str,
    target_path: Path | str,
    connector_key: str = "output",
) -> None:
    """Move files or folders.

    :param config: Config to use for data moving.
    :param source_path: Source path to move from.
    :param target_path: Target path to move to.
    :param connector_key: Key of the connector to use.
    """
    connector_config = get_data_connector_config(config, connector_key)
    connector = get_data_connector(connector_config)

    if not isinstance(connector, BaseFileConnector):
        message = "This method is only supported for file connectors."
        raise InvalidConnectorError(message)

    connector_path = Path(connector_config.path)
    connector.move(
        connector_path / source_path,
        connector_path / target_path,
    )


def delete(
    config: Box,
    path: Path | str,
    connector_key: str = "output",
) -> None:
    """Delete files or folders.

    :param config: Config to use for data deletion.
    :param path: Path to delete.
    :param connector_key: Key of the connector to use.
    """
    connector_config = get_data_connector_config(config, connector_key)
    connector = get_data_connector(connector_config)

    if not isinstance(connector, BaseFileConnector):
        message = "This method is only supported for file connectors."
        raise InvalidConnectorError(message)

    connector_path = Path(connector_config.path)
    connector.delete(connector_path / path)
