"""Pipeline to orchestrate all logic."""

import logging

import mlflow
from box import Box

from pipelines.data.reader import read_dataframe
from pipelines.data.writer import write_dataframe
from pipelines.sample.schemas.input import ProductSchema as ProductInputSchema
from pipelines.sample.schemas.output import ProductSchema as ProductOutputSchema
from pipelines.sample.steps.price_processor import compute_price
from pipelines.utils import timing

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
    sample_data = read_dataframe(config, config.sample.input.product)
    ProductInputSchema.validate(sample_data)

    log_.info("Compute data.")
    processed_data = compute_price(sample_data, config.sample.price.multiplier)

    log_.info("Write data.")
    ProductOutputSchema.validate(processed_data)
    write_dataframe(config, config.sample.output.product, processed_data)

    log_.info("Pipeline run completed.")
