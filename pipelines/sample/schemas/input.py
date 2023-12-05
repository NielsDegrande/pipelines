"""Module to define input data schemas, to be validated after read."""

import pandera as pa
from pandera.typing import Series


class ProductSchema(pa.DataFrameModel):
    """Schema for product data."""

    product_name: Series[str] = pa.Field(unique=True, nullable=False, coerce=True)
    color: Series[str] = pa.Field(nullable=False, coerce=True)
