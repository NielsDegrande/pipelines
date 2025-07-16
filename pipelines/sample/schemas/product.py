"""Module to define input data schemas, to be validated after read."""

import pandera.pandas as pa
from pandera.typing import Series


class ProductInputSchema(pa.DataFrameModel):
    """Input schema for product data."""

    product_name: Series[str] = pa.Field(unique=True, nullable=False, coerce=True)
    color: Series[str] = pa.Field(nullable=False, coerce=True)


class ProductWithIdSchema(ProductInputSchema):
    """Intermediate schema for product data."""

    product_id: Series[int] = pa.Field(unique=True, nullable=False, coerce=True)


class ProductOutputSchema(ProductWithIdSchema):
    """Output schema for sample data."""

    price: Series[float] = pa.Field(ge=0, nullable=False, coerce=True)


PRODUCTS_COLUMN_ORDER = [
    ProductWithIdSchema.product_id,
    *ProductInputSchema.to_schema().columns.keys(),
    ProductOutputSchema.price,
]
