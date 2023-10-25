"""Pipeline to orchestrate all logic."""

import logging

import mlflow
from box import Box

from pipelines.data.reader import read_dataframe
from pipelines.data.schemas.input import SampleSchema as SampleInputSchema
from pipelines.data.schemas.output import SampleSchema as SampleOutputSchema
from pipelines.data.writer import write_dataframe
from pipelines.sample.steps.price_processor import process_price
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
    mlflow.log_param("sample_key", config.sample_key)
    log_.info("Value for sample key is: %s.", config.sample_key)

    log_.info("Read data.")
    sample_data = read_dataframe(config, config.input.sample)
    SampleInputSchema.validate(sample_data)

    log_.info("Process data.")
    processed_data = process_price(sample_data)

    log_.info("Write data.")
    SampleOutputSchema.validate(processed_data)
    write_dataframe(config, config.output.sample, processed_data)

    log_.info("Pipeline run completed.")
