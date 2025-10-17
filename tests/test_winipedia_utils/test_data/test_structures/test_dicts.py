"""module."""

from winipedia_utils.data.structures.dicts import reverse_dict
from winipedia_utils.testing.assertions import assert_with_msg


def test_reverse_dict() -> None:
    """Test func for reverse_dict."""
    # Test with simple dictionary
    test_dict = {"a": 1, "b": 2, "c": 3}
    expected = {1: "a", 2: "b", 3: "c"}
    result = reverse_dict(test_dict)
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )
