"""Keep constants value separate from other code."""

from enum import StrEnum, auto


class Pipelines(StrEnum):
    """All available pipelines."""

    sample = auto()


class DataConnectors(StrEnum):
    """All available data connectors."""

    file = auto()
    gcs = auto()


class FileFormats(StrEnum):
    """All supported file formats."""

    CSV = auto()


# Extensions.
CSV_EXTENSION = ".csv"
YAML_EXTENSION = ".yaml"

# Format to extension mapping.
FORMAT_TO_EXTENSION = {
    FileFormats.CSV: CSV_EXTENSION,
}

# Format to options mapping.
FORMAT_TO_OPTIONS: dict = {
    # Enforce same CSV separator across all files to avoid issues.
    FileFormats.CSV: {
        "sep": ",",
    },
}
