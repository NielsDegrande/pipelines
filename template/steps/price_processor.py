"""Process the price data."""

import pandas as pd

from template.data.schemas.input import SampleSchema


def process_price(df: pd.DataFrame) -> pd.DataFrame:
    """Process price data.

    :param df: DataFrame holding the price data.
    :return: Processed price data.
    """
    df[SampleSchema.price] = df[SampleSchema.price] * 2
    return df
