"""Package entry point."""

import argparse
import logging
from importlib import import_module

from dotenv import load_dotenv

from configs import CONFIGS_DIRECTORY
from pipelines.utils import load_config
from pipelines.utils.constants import YAML_EXTENSION, Pipeline


def _parse_cli_args() -> argparse.Namespace:
    """Parse command line arguments.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pipeline",
        "-p",
        type=str,
        help="Pipeline to be run.",
        # Choices are fetched dynamically. Raises an ImportError on invalid choice.
        choices=list(Pipeline),
        required=True,
    )
    parser.add_argument(
        "--root_config",
        type=str,
        help="""
        Global config to be loaded.
        Multiple values can be provided, separated by spaces.
        """,
        nargs="+",
        required=False,
        default=[],
    )
    parser.add_argument(
        "--pipeline_config",
        type=str,
        help="""
        Pipeline config to be loaded.
        Multiple values can be provided, separated by spaces.
        """,
        nargs="+",
        required=False,
        default=[],
    )
    parser.add_argument(
        "--cli_config",
        type=str,
        nargs="+",
        required=False,
        help=(
            "Additional configuration to be loaded from the command line. "
            "Should be in the format key=value. "
            "Separate multiple values with spaces. "
            "Use dot notation to specify nested keys."
        ),
    )
    return parser.parse_args()


def main() -> None:
    """Run a pipeline."""
    log_ = logging.getLogger(__name__)

    arguments = _parse_cli_args()
    pipeline_name = arguments.pipeline
    pipeline = import_module(".", package=f"pipelines.{pipeline_name}.pipeline")

    log_.info("Load configuration.")
    load_dotenv()
    root_configs = [
        CONFIGS_DIRECTORY / (config + YAML_EXTENSION)
        for config in ["config", "data_connectors", *arguments.root_config]
    ]
    pipeline_configs = [
        CONFIGS_DIRECTORY / pipeline_name / (config + YAML_EXTENSION)
        for config in ["config", *arguments.pipeline_config]
    ]
    config = load_config(
        root_configs + pipeline_configs,
        cli_config=arguments.cli_config,
    )
    pipeline.run(config)


if __name__ == "__main__":
    main()
