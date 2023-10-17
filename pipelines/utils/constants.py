"""Keep constants value separate from other code."""

from enum import StrEnum, auto


class PipelineEnum(StrEnum):
    """All available pipelines."""

    SAMPLE = auto()


# Extensions.
YAML_EXTENSION = ".yaml"
