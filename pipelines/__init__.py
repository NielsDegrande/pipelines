"""Package init file.

Logging is configured here to ensure global scope.
"""

from configs import CONFIGS_DIRECTORY
from pipelines.utils import configure_logging
from pipelines.utils.constants import YAML_EXTENSION

LOG_CONFIG_PATH = CONFIGS_DIRECTORY / f"log{YAML_EXTENSION}"
configure_logging(LOG_CONFIG_PATH)
