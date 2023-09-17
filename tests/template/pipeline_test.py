# -*- coding: utf-8 -*-
"""Run pipeline E2E and validate success/failure."""

import template.pipeline as pipeline
from template.utils import load_config


def test_pipeline__expect_no_error():
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
