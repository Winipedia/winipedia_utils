"""module."""

from typing import Any

import pytest

from winipedia_utils.iterating.iterate import (
    get_len_with_default,
    nested_structure_is_subset,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_len_with_default() -> None:
    """Test func for get_len_with_default."""
    # Test with list
    test_list = [1, 2, 3]
    assert_with_msg(
        get_len_with_default(test_list) == len(test_list),
        f"Expected 3, got {get_len_with_default(test_list)}",
    )

    # Test with set
    test_set = {1, 2, 3}
    assert_with_msg(
        get_len_with_default(test_set) == len(test_set),
        f"Expected 3, got {get_len_with_default(test_set)}",
    )

    # Test with generator
    expected_len = 3
    test_gen = (x for x in range(expected_len))
    result = get_len_with_default(test_gen, default=expected_len)
    assert_with_msg(
        result == expected_len,
        f"Expected 3, got {result}",
    )

    # Test with no default raises TypeError
    with pytest.raises(TypeError):
        get_len_with_default(test_gen)


def test_nested_structure_is_subset() -> None:
    """Test func for nested_structure_is_subset."""
    subset: dict[str, Any] = {
        "a": 1,
        "b": [2, 3, {"c": 4}],
    }
    superset: dict[str, Any] = {
        "a": 1,
        "b": [2, 3, {"c": 4}, 5],
        "d": 6,
    }
    assert_with_msg(
        nested_structure_is_subset(subset, superset),
        "Expected subset to be subset of superset",
    )

    subset = {
        "a": 1,
        "b": [2, 3, {"c": 4}],
    }
    superset = {
        "a": 1,
        "b": [2, 3, {"c": 5}],
    }
    assert_with_msg(
        not nested_structure_is_subset(subset, superset),
        "Expected subset not to be subset of superset",
    )

    false_values: list[Any] = []

    def on_false_dict_action(
        subset_obj: dict[str, Any], _superset_obj: dict[str, Any], key: str
    ) -> None:
        fv = subset_obj[key]
        false_values.append(fv)

    def on_false_list_action(
        subset_obj: list[Any], _superset_obj: list[Any], index: int
    ) -> None:
        fv = subset_obj[index]
        false_values.append(fv)

    subset = {
        "a": 1,
        "b": [2, 0, {"c": 4}],
    }
    superset = {
        "a": 1,
        "b": [2, 3, {"c": 5}],
    }
    nested_structure_is_subset(
        subset, superset, on_false_dict_action, on_false_list_action
    )
    expected_false_values: list[Any] = [0, 4, {"c": 4}, [2, 0, {"c": 4}]]
    assert_with_msg(
        false_values == expected_false_values,
        f"Expected false values to be {expected_false_values}, got {false_values}",
    )

    subset = {
        "a": 1,
        "b": [2, 3, {"d": 5}, {"c": 4}],
    }
    superset = {
        "a": 1,
        "b": [3, 2, {"c": 4}, {"d": 5}],
    }
    is_nested_subset = nested_structure_is_subset(
        subset, superset, on_false_dict_action, on_false_list_action
    )
    assert_with_msg(
        is_nested_subset,
        "Expected subset to be subset of superset",
    )
