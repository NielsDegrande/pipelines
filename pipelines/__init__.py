"""Package init file.

Logging is configured here to ensure global scope.
"""

from pipelines.utils import configure_logging

LOG_CONFIG_PATH = "configs/log.yaml"
configure_logging(LOG_CONFIG_PATH)
