"""Make it possible to dynamically create a data connector."""

from box import Box

from pipelines.data.connectors.base import BaseConnector
from pipelines.data.connectors.database import DatabaseConnector
from pipelines.data.connectors.file import FileConnector
from pipelines.data.connectors.gcs import GcsConnector
from pipelines.utils.constants import DataConnector


def get_data_connector_config(config: Box, connector_key: str) -> Box:
    """Get the config for a data connector.

    :param config: Config to use for data operations.
    :param connector_key: Key of the connector to use.
    :return: Config for the data connector.
    """
    connector_name = config.data_connectors[connector_key]
    return config.data_connector_options[connector_name]


class IllegalDataConnectorError(Exception):
    """Raise this exception when an illegal data connector type is given."""


def get_data_connector(connector_config: Box) -> BaseConnector:
    """Get a data connector.

    :param connector_config: Config for connector.
    :raises IllegalDataConnectorError: When connector type does not exist.
    :return: A data connector object.
    """
    match connector_config.type:
        case DataConnector.file:
            return FileConnector()
        case DataConnector.gcs:
            return GcsConnector(connector_config.bucket_name)
        case DataConnector.database:
            return DatabaseConnector(
                connector_config.dialect,
                connector_config.host,
                connector_config.db_name,
                connector_config.username,
                connector_config.password,
            )
        case _:
            raise IllegalDataConnectorError
