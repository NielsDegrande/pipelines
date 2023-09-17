# -*- coding: utf-8 -*-
"""Config related utility functions."""

import logging
from pathlib import Path
from typing import List

import yaml
from box import Box

log_ = logging.getLogger(__name__)


def load_config(config_paths: List[str]) -> Box:
    """Load config from file.

    :param config_path: Path to config.
    :raises FileNotFoundError: When config cannot be loaded.
    :return: Boxed config.
    """
    config: dict = {}
    for config_path in config_paths:
        path_ = Path(config_path)
        if path_.exists():
            with open(path_, "r") as file_:
                config = _update_config(yaml.safe_load(file_.read()), config)
        else:
            raise FileNotFoundError(
                "Config not found, configuration is not loaded.",
            )
    return Box(config)


def _update_config(source: dict, target: dict) -> dict:
    """Update nested dictionaries recursively.

    This happens in an append-overwrite manner:
    - Append if full key is unseen (e.g. parent.child).
    - Override if full key already exists in target.

    :param source: Source of new keys and values.
    :param target: Existing mapping to update with source.
    :return: Combination of both source and target.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # Recurse if the value in source is a nested dictionary.
            # Required to prevent overriding a key in full.
            # Instead go down the nesting, add the new keys,
            # and override the overlapping ones.
            target[key] = _update_config(value, target.get(key, {}))
        else:
            # Reached lowest level in recursion, set key to value.
            target[key] = value
    return target
