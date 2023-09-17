# -*- coding: utf-8 -*-
"""Pipeline to orchestrate all logic."""

import logging

import mlflow
from box import Box

from template.data.reader import read_dataframe
from template.data.schemas.input import SampleSchema as SampleInputSchema
from template.data.schemas.output import SampleSchema as SampleOutputSchema
from template.data.writer import write_dataframe
from template.steps.price_processor import process_price
from template.utils import timing

log_ = logging.getLogger(__name__)


@timing
def run(config: Box) -> None:
    """Run pipeline.

    :param config: Configuration to use for this run.
    :param chosen_scenario: name of the chosen scenario
    """
    log_.info("Pipeline run started.")

    # Example: Use MLflow to log params, metrics and artifacts.
    mlflow.autolog()
    mlflow.log_param("sample_key", config.sample_key)

    # Example: Read data.
    df = read_dataframe(config, "sample")
    SampleInputSchema.validate(df)

    # Example: Process data with one sample step.
    df = process_price(df)

    # Example: Write data.
    SampleOutputSchema.validate(df)
    write_dataframe(config, "sample", df)

    log_.info("Pipeline run completed.")
