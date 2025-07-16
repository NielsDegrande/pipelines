"""Utilities for working with DataFrames."""

from typing import TypeVar, cast

from pandas import DataFrame as PandasDataFrame
from pandera.pandas import DataFrameModel
from pandera.typing import DataFrame as PanderaDataFrame

T = TypeVar("T", bound=DataFrameModel)
DataFrame = PandasDataFrame | PanderaDataFrame


def select_columns(
    df: DataFrame,
    columns: list[str],
) -> PandasDataFrame:
    """Select columns from a DataFrame.

    This function additionally:
    - Re-orders columns, as part of the selection.
    - Ensures the type is pd.DataFrame, as opposed to pd.Series.

    :param df: Any DataFrame to select columns from.
    :param columns: Columns to select.
    :return: DataFrame with selected columns.
    """
    if not len(columns):
        message = "No columns selected."
        raise ValueError(message)
    return PandasDataFrame(df[columns])


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
