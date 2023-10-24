"""Set up logging."""

import logging
import logging.config
from pathlib import Path

import yaml

LOG_FOLDER = "logs"


def configure_logging(config_path: Path) -> None:
    """Configure logging for application.

    :param config_path: Path to file holding logging configuration.
    :raises FileNotFoundError: When logging cannot be initialized.
    """
    # Ensure logs folder exists. This is the folder where you write the logs.
    Path(LOG_FOLDER).mkdir(exist_ok=True)

    # Configure logging.
    if config_path.exists():
        with config_path.open() as file_:
            logging.config.dictConfig(yaml.safe_load(file_.read()))
    else:
        error_message = "Log config not found, logging is not initialized."
        raise FileNotFoundError(error_message)
