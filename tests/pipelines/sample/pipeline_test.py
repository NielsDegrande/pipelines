"""Run pipeline E2E and validate success or failure."""

from pipelines.sample import pipeline
from pipelines.utils import load_config


def test_pipeline__expect_no_error() -> None:
    """Validate that the pipeline runs E2E with no error."""
    # Load config.
    config = load_config(
        [
            "configs/config.yaml",
            "configs/e2e_test.yaml",
            "configs/data_connectors.yaml",
        ],
    )
    pipeline.run(config)
