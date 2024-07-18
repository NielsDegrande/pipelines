"""Pipeline to orchestrate all logic."""

import logging
from pathlib import Path

import mlflow
from box import Box

from pipelines.data.manager import copy, delete, list_files, move
from pipelines.data.reader import read_dataframe
from pipelines.data.writer import write_dataframe
from pipelines.sample.schemas.product import (
    PRODUCTS_COLUMN_ORDER,
    ProductInputSchema,
)
from pipelines.sample.steps.price_processor import compute_price
from pipelines.sample.steps.product_identifier import add_product_identifiers
from pipelines.utils import timing
from pipelines.utils.constants import CSV_EXTENSION
from pipelines.utils.dataframe import select_columns, validate_dataframe

log_ = logging.getLogger(__name__)


@timing
def run(config: Box) -> None:
    """Run pipeline.

    :param config: Configuration to use for this run.
    """
    log_.info("Pipeline run started.")

    log_.info("Enable MLflow.")
    mlflow.autolog()
    mlflow.log_param("sample_key", config.sample.key)
    log_.info("Value for sample key is: %s.", config.sample.key)

    log_.info("Read data.")
    raw_data = read_dataframe(config, config.sample.input.product)
    input_data = validate_dataframe(ProductInputSchema, raw_data)

    log_.info("Process data.")
    id_data = add_product_identifiers(input_data)
    price_data = compute_price(id_data, config.sample.price.multiplier)

    log_.info("Write data.")
    output_data = select_columns(price_data, PRODUCTS_COLUMN_ORDER)
    write_dataframe(config, config.sample.output.product, output_data)

    log_.info("Copy data.")
    new_name = "copied_products" + CSV_EXTENSION
    copy(config, config.sample.output.product + CSV_EXTENSION, new_name)

    log_.info("Move data.")
    new_location = Path("moved")
    move(config, new_name, new_location / new_name)

    log_.info("List data.")
    log_.info("Files in output: %s", list_files(config, "", "output"))

    log_.info("Delete data.")
    delete(config, new_location)

    log_.info("Pipeline run completed.")
