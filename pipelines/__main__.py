"""Package entry point."""

import argparse
import logging
from importlib import import_module

from configs import CONFIGS_DIRECTORY
from pipelines.utils import load_config
from pipelines.utils.constants import YAML_EXTENSION, PipelineEnum


def _parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pipeline",
        "-p",
        type=str,
        help="Pipeline to be run.",
        # Choices are fetched dynamically. Raises an ImportError on invalid choice.
        choices=list(PipelineEnum),
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    """Trigger entry point to Pipelines."""
    log_ = logging.getLogger(__name__)

    arguments = _parse_cli_args()
    pipeline_name = arguments.pipeline
    pipeline = import_module(".", package=f"pipelines.{pipeline_name}.pipeline")

    log_.info("Load configuration")
    config = load_config(
        [
            CONFIGS_DIRECTORY / f"config{YAML_EXTENSION}",
            CONFIGS_DIRECTORY / f"data_connectors{YAML_EXTENSION}",
            CONFIGS_DIRECTORY / pipeline_name / f"config{YAML_EXTENSION}",
        ],
    )
    pipeline.run(config)


if __name__ == "__main__":
    main()
