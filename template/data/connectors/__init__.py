"""Make it possible to dynamically create a data connector."""

from template.data.connectors.base import BaseConnector
from template.data.connectors.file import FileConnector


class IllegalDataConnectorError(Exception):
    """Raise this exception when an illegal data connector type is given."""


def get_data_connector(connector_type: str) -> BaseConnector:
    """Get a data connector.

    :param connector_type: Type of the data connector to get.
    :raises IllegalDataConnectorError: When connector type does not exist.
    :return: A data connector object.
    """
    match connector_type:
        case "file":
            return FileConnector()
        case _:
            raise IllegalDataConnectorError
