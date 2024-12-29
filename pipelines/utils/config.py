"""Config related utility functions."""

import logging
from collections import defaultdict
from os import environ
from pathlib import Path
from string import Template
from typing import Any

import yaml
from box import Box

from pipelines.utils.constants import DataConnector, Pipeline

log_ = logging.getLogger(__name__)

type ConfigDict = dict[str, Any]


def load_config(config_paths: list[Path]) -> Box:
    """Load config from file.

    :param config_paths: Path to config files.
    :raises FileNotFoundError: When config cannot be loaded.
    :return: Boxed config.
    """
    config: ConfigDict = {}
    for config_path in config_paths:
        if config_path.exists():
            with config_path.open() as file_:
                config = _update_config(yaml.safe_load(file_.read()), config)
        else:
            error_message = f"'{config_path}' not found, configuration is not loaded."
            raise FileNotFoundError(error_message)
    config = Box(config)
    config = _set_connectors_to_pipeline(config)
    environment_variables = defaultdict(str, environ)
    return _resolve_environment_variables(config, environment_variables)


def _update_config(source: ConfigDict, target: ConfigDict) -> ConfigDict:
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


def _set_connectors_to_pipeline(config: Box) -> Box:
    """Replace the placeholders in data_connector configuration with specific pipeline.

    :param config: Config for the pipeline with placeholders.
    :return: Config for the pipeline without placeholders.
    """
    pipeline = Pipeline(config.name)
    for connector_name in config.data_connectors.values():
        connector_config = config.data_connector_options[connector_name]
        if connector_config.type in [
            DataConnector.file,
            DataConnector.gcs,
        ]:
            connector_config.path = connector_config.path.format(pipeline=pipeline)
    return config


def _resolve_environment_variables(config: Box, environment_variables: dict) -> Box:
    """Update config with values read from the environment.

    Compliant config values correspond to the format: ${NAME_OF_ENVIRONMENT_VARIABLE}.
    Default to empty string if the environment variable does not exist on the system.

    :param config: Config for the pipeline with environment variable placeholders.
    :param environment_variables: Dictionary holding the environment variables.
    :return: Config for the pipeline without environment variable placeholders.
    """
    for key, value in config.items():
        if isinstance(value, Box):
            _resolve_environment_variables(value, environment_variables)
        elif isinstance(value, list):
            config[key] = [
                (
                    Template(item).substitute(environment_variables)
                    if "${" in str(item)
                    else item
                )
                for item in value
            ]
        elif isinstance(value, str) and "${" in value:
            config[key] = Template(value).substitute(environment_variables)
    return config
