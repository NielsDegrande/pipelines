"""Tests for utils.config."""

from pipelines.utils.config import _update_config, parse_cli_config


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


def test_parse_cli_config() -> None:
    """Validate that parse_cli_config correctly appends or overrides new keys."""
    cli_config = [
        "test1.test2.test3=value1",
        "test1.test2.test3=value2",
        "test1.test2.test3bis=value3",
        "test1.test2bis.test3=value4",
    ]
    expected = {
        "test1": {
            "test2": {
                "test3": "value2",
                "test3bis": "value3",
            },
            "test2bis": {
                "test3": "value4",
            },
        },
    }
    assert parse_cli_config(cli_config) == expected
