"""Add product identifiers."""

from typing import TYPE_CHECKING

from pipelines.sample.schemas.product import ProductInputSchema, ProductWithIdSchema
from pipelines.utils.dataframe import validate_dataframe

if TYPE_CHECKING:
    from pandera.typing import DataFrame


def add_product_identifiers(
    products: DataFrame[ProductInputSchema],
) -> DataFrame[ProductWithIdSchema]:
    """Add product identifiers.

    :param products: DataFrame holding the product data.
    :return: Product data, complemented by identifiers.
    """
    products[ProductWithIdSchema.product_id] = range(0, len(products), 1)
    return validate_dataframe(ProductWithIdSchema, products)
