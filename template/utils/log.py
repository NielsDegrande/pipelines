# -*- coding: utf-8 -*-
"""Set up logging."""

import logging
import logging.config
from pathlib import Path

import yaml

LOG_FOLDER = "logs"


def configure_logging(config_path: str) -> None:
    """Configure logging for application.

    :param config_path: Path to file holding logging configuration.
    :raises FileNotFoundError: When logging cannot be initialized.
    """
    # Ensure logs folder exists.
    Path(LOG_FOLDER).mkdir(exist_ok=True)

    # Configure logging.
    path_ = Path(config_path)
    if path_.exists():
        with open(path_, "r") as file_:
            logging.config.dictConfig(yaml.safe_load(file_.read()))
    else:
        raise FileNotFoundError(
            "Log config not found, logging is not initialized.",
        )
