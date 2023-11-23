"""Process the price data."""

from pandera.typing import DataFrame

from pipelines.data.schemas.input import SampleSchema


def process_price(df: DataFrame[SampleSchema]) -> DataFrame[SampleSchema]:
    """Process price data.

    :param df: DataFrame holding the price data.
    :return: Processed price data.
    """
    df[SampleSchema.price] = df[SampleSchema.price] * 2
    return df
