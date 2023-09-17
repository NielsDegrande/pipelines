# -*- coding: utf-8 -*-
"""Package init file.

Logging is configured here to ensure global scope.
"""

from template.utils import configure_logging

LOG_CONFIG_PATH = "configs/log.yaml"
configure_logging(LOG_CONFIG_PATH)
