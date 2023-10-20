"""Run pipeline E2E and validate success or failure."""

from configs import CONFIGS_DIR
from pipelines.sample import pipeline
from pipelines.utils import load_config
from pipelines.utils.constants import YAML_EXTENSION


def test_pipeline__expect_no_error() -> None:
    """Validate that the pipeline runs E2E with no error."""
    pipeline_name = "sample"

    # Load config.
    config = load_config(
        [
            CONFIGS_DIR / f"config{YAML_EXTENSION}",
            CONFIGS_DIR / f"data_connectors{YAML_EXTENSION}",
            CONFIGS_DIR / f"e2e_test{YAML_EXTENSION}",
            CONFIGS_DIR / pipeline_name / f"config{YAML_EXTENSION}",
            CONFIGS_DIR / pipeline_name / f"e2e_test{YAML_EXTENSION}",
        ],
    )
    pipeline.run(config)
