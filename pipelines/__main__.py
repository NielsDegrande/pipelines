"""Package entry point."""

import argparse
import logging
from importlib import import_module

from pipelines.utils import load_config
from pipelines.utils.constants import PipelineEnum


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

    log_.info("Load configuration")
    config = load_config(
        ["configs/config.yaml", "configs/data_connectors.yaml"],
    )

    pipeline_name = arguments.__dict__.get("pipeline")
    pipeline = import_module(".", package=f"pipelines.{pipeline_name}.pipeline")
    pipeline.run(config)


if __name__ == "__main__":
    main()
