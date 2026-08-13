"""Compute the product prices."""

from typing import TYPE_CHECKING

from pipelines.sample.schemas.product import ProductOutputSchema, ProductWithIdSchema
from pipelines.utils.dataframe import validate_dataframe

if TYPE_CHECKING:
    from pandera.typing import DataFrame


def compute_price(
    products: DataFrame[ProductWithIdSchema],
    price_multiplier: int,
) -> DataFrame[ProductOutputSchema]:
    """Compute product prices.

    :param products: DataFrame holding the product data.
    :param price_multiplier: Price will be computed as this multiplier times ID.
    :return: Product data, complemented by price.
    """
    products[ProductOutputSchema.price] = (
        products[ProductOutputSchema.product_id] + 1
    ) * price_multiplier
    return validate_dataframe(ProductOutputSchema, products)
