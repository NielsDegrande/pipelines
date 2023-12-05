"""Compute the product prices."""

from pandera.typing import DataFrame

from pipelines.sample.schemas.input import ProductSchema as ProductInputSchema
from pipelines.sample.schemas.output import ProductSchema as ProductOutputSchema


def compute_price(
    products: DataFrame[ProductInputSchema],
    price_multiplier: int,
) -> DataFrame[ProductOutputSchema]:
    """Compute product prices.

    :param products: DataFrame holding the product data.
    :param price_multiplier: Price will be computed as this multiplier times ID.
    :return: Product data, complemented by price.
    """
    products[ProductOutputSchema.product_id] = range(1, len(products) + 1, 1)
    products[ProductOutputSchema.price] = (
        products[ProductOutputSchema.product_id] + 1
    ) * price_multiplier
    return products
