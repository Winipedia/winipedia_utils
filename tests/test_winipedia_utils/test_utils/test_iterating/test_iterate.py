"""module."""

import pytest
from pyrig.src.testing.assertions import assert_with_msg

from winipedia_utils.src.iterating.iterate import (
    get_len_with_default,
)


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
