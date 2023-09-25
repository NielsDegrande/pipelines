"""Module to abstract all data reading."""


import pandas as pd
from box import Box

from pipelines.data.connectors import get_data_connector


def read_dataframe(config: Box, data_object_name: str) -> pd.DataFrame:
    """Read dataframe.

    :param config: Config to use for data reading.
    :param data_object_name: Data object to read.
    :return: DataFrame holding the data.
    """
    input_connector = config[config.data_connectors.input]
    connector = get_data_connector(input_connector.type)
    return connector.read_dataframe(data_object_name, **input_connector)
