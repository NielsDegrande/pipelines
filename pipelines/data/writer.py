"""Module to abstract all data writing."""

import pandas as pd
from box import Box

from pipelines.data.connectors import get_data_connector, get_data_connector_config


def write_dataframe(
    config: Box,
    data_object_name: str,
    df: pd.DataFrame,
    connector_key: str = "output",
    **kwargs: dict,
) -> None:
    """Write dataframe.

    :param config: Config to use for data writing.
    :param data_object_name: Data object to write.
    :param df: DataFrame holding the data.
    :param connector_key: Key of the connector to use.
    :param **kwargs: Additional kwargs to pass to the connector.
    """
    connector_config = get_data_connector_config(config, connector_key)
    connector = get_data_connector(connector_config)
    connector.write_dataframe(data_object_name, df, **connector_config, **kwargs)
