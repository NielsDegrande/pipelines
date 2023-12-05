"""Module to define output data schemas, to be validated before write."""

import pandera as pa
from pandera.typing import Series


class ProductSchema(pa.DataFrameModel):
    """Schema for sample data."""

    class Config:
        """Configuration for output schema."""

        strict = True  # Disallow additional columns.

    product_id: Series[int] = pa.Field(unique=True, nullable=False, coerce=True)
    product_name: Series[str] = pa.Field(unique=True, nullable=False, coerce=True)
    color: Series[str] = pa.Field(nullable=False, coerce=True)
    price: Series[float] = pa.Field(ge=0, nullable=False, coerce=True)
