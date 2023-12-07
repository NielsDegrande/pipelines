"""Add product identifiers."""

from pandera.typing import DataFrame

from pipelines.sample.schemas.input import ProductSchema as ProductInputSchema
from pipelines.sample.schemas.output import ProductSchema as ProductOutputSchema


def add_product_identifiers(
    products: DataFrame[ProductInputSchema],
) -> DataFrame[ProductOutputSchema]:
    """Add product identifiers.

    :param products: DataFrame holding the product data.
    :return: Product data, complemented by identifiers.
    """
    products[ProductOutputSchema.product_id] = range(0, len(products), 1)
    return products
