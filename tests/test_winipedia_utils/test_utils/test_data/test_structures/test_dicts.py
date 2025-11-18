"""module."""

from pyrig.src.testing.assertions import assert_with_msg

from winipedia_utils.src.data.structures.dicts import reverse_dict


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
