# -*- coding: utf-8 -*-
"""Module to abstract all data writing."""

import pandas as pd
from box import Box

from template.data.connectors import get_data_connector


def write_dataframe(
    config: Box,
    data_object_name: str,
    df: pd.DataFrame,
) -> None:
    """Write dataframe.

    :param connector_type: Connector to use for data writing.
    :param data_object_name: Data object to write.
    :param df: DataFrame holding the data.
    """
    output_connector = config[config.data_connectors.output]
    connector = get_data_connector(output_connector.type)
    return connector.write_dataframe(data_object_name, df, **output_connector)
