"""Utilities for working with DataFrames."""

from typing import TypeVar, cast

from pandas import DataFrame as PandasDataFrame
from pandera import DataFrameModel
from pandera.typing import DataFrame as PanderaDataFrame

T = TypeVar("T", bound=DataFrameModel)
DataFrame = PandasDataFrame | PanderaDataFrame


def validate_dataframe(
    schema: type[T],
    df: DataFrame,
) -> PanderaDataFrame[T]:
    """Validate given a specified schema.

    Casting is required as Pandera returns DataFrameBase[T].

    :param schema: Schema to use for validation and casting.
    :param df: DataFrame to validate.
    :return: The validated and casted DataFrame.
    """
    return cast(PanderaDataFrame[T], schema.validate(df))
