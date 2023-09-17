# -*- coding: utf-8 -*-
"""Package entry point."""

import logging

import template.pipeline as pipeline
from template.utils import load_config


def main():
    """Trigger entry point to Template."""
    log_ = logging.getLogger(__name__)
    log_.info("Load configuration")
    config = load_config(
        ["configs/config.yaml", "configs/data_connectors.yaml"],
    )
    pipeline.run(config)


if __name__ == "__main__":
    main()
