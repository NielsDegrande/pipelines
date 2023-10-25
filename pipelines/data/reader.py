"""Module to abstract all data reading."""


import pandas as pd
from box import Box

from pipelines.data.connectors import get_data_connector, get_data_connector_config


def read_dataframe(
    config: Box,
    data_object_name: str,
    connector_key: str = "input",
    **kwargs: dict,
) -> pd.DataFrame:
    """Read dataframe.

    :param config: Config to use for data reading.
    :param data_object_name: Data object to read from.
    :param connector_key: Key of the connector to use.
    :return: DataFrame holding the data.
    """
    connector_config = get_data_connector_config(config, connector_key)
    connector = get_data_connector(connector_config)
    return connector.read_dataframe(data_object_name, **connector_config, **kwargs)
