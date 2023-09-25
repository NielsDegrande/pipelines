"""Tests for utils.config."""

from pipelines.utils.config import _update_config


def test_update_config__append() -> None:
    """Validate that _update_config correctly appends new full keys."""
    source = {
        "parent": {
            "child": {
                "c": "value_c",
            },
        },
    }
    target = {
        "parent": {
            "child": {
                "a": "value_a",
                "b": "value_b",
            },
        },
        "parent2": {"child": {"d": "value_d"}},
    }
    expected = {
        "parent": {
            "child": {
                "a": "value_a",
                "b": "value_b",
                "c": "value_c",
            },
        },
        "parent2": {"child": {"d": "value_d"}},
    }
    assert _update_config(source, target) == expected


def test_update_config__override() -> None:
    """Validate that _update_config correctly overrides existing full keys."""
    source = {
        "parent": {
            "child": {
                "a": "value_a_bis",
            },
        },
    }
    target = {
        "parent": {
            "child": {
                "a": "value_a",
                "b": "value_b",
            },
        },
        "parent2": {"child": {"d": "value_d"}},
    }
    expected = {
        "parent": {
            "child": {
                "a": "value_a_bis",
                "b": "value_b",
            },
        },
        "parent2": {"child": {"d": "value_d"}},
    }
    assert _update_config(source, target) == expected
