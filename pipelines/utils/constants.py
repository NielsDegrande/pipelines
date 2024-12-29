"""Keep constant values separate from other code."""

from enum import StrEnum, auto


class Pipeline(StrEnum):
    """All available pipelines."""

    sample = auto()


class DataConnector(StrEnum):
    """All available data connectors."""

    database = auto()
    file = auto()
    gcs = auto()


class FileFormat(StrEnum):
    """All supported file formats."""

    CSV = auto()


# Extensions.
CSV_EXTENSION = ".csv"
YAML_EXTENSION = ".yaml"

# Format to extension mapping.
FORMAT_TO_EXTENSION = {
    FileFormat.CSV: CSV_EXTENSION,
}

# Format to options mapping.
FORMAT_TO_OPTIONS: dict = {
    # Enforce same CSV separator across all files to avoid issues.
    FileFormat.CSV: {
        "sep": ",",
    },
}
