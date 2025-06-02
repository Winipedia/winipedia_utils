"""Tests for winipedia_utils.text.string module."""

import hashlib
from io import StringIO

from pytest_mock import MockFixture

from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.text.string import (
    ask_for_input_with_timeout,
    find_xml_namespaces,
    get_reusable_hash,
    split_on_uppercase,
    value_to_truncated_string,
)


def test_ask_for_input_with_timeout(mocker: MockFixture) -> None:
    """Test func for ask_for_input_with_timeout."""
    # Mock the cancel_on_timeout decorator to avoid multiprocessing issues in tests
    mock_cancel_on_timeout = mocker.patch(
        "winipedia_utils.text.string.cancel_on_timeout"
    )

    # Create a simple decorator that just calls the function
    def simple_decorator(_timeout_val: int, _msg: str) -> object:
        def decorator(func: object) -> object:
            return func

        return decorator

    mock_cancel_on_timeout.side_effect = simple_decorator

    # Test successful input within timeout
    mock_input = mocker.patch("builtins.input", return_value="test input")
    timeout_seconds = 5

    result = ask_for_input_with_timeout("Enter something: ", timeout_seconds)

    assert_with_msg(
        result == "test input",
        f"Expected 'test input', got '{result}'",
    )
    mock_input.assert_called_once_with("Enter something: ")

    # Test with different input
    mock_input.reset_mock()
    mock_input.return_value = "different input"
    short_timeout = 1

    result = ask_for_input_with_timeout("Enter something: ", short_timeout)
    assert_with_msg(
        result == "different input",
        f"Expected 'different input', got '{result}'",
    )


def test_find_xml_namespaces() -> None:
    """Test func for find_xml_namespaces."""
    # Test with string XML containing namespaces
    xml_string = """<?xml version="1.0"?>
    <root xmlns:ns1="http://example.com/ns1"
          xmlns:ns2="http://example.com/ns2"
          xmlns="http://example.com/default">
        <ns1:element>content</ns1:element>
        <ns2:element>content</ns2:element>
    </root>"""

    result = find_xml_namespaces(xml_string)

    expected = {
        "ns1": "http://example.com/ns1",
        "ns2": "http://example.com/ns2",
    }

    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )

    # Test with StringIO XML
    xml_stringio = StringIO(xml_string)
    result = find_xml_namespaces(xml_stringio)

    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )

    # Test with XML without namespaces
    simple_xml = """<?xml version="1.0"?>
    <root>
        <element>content</element>
    </root>"""

    result = find_xml_namespaces(simple_xml)

    assert_with_msg(
        result == {},
        f"Expected empty dict, got {result}",
    )

    # Test with XML containing only default namespace
    default_ns_xml = """<?xml version="1.0"?>
    <root xmlns="http://example.com/default">
        <element>content</element>
    </root>"""

    result = find_xml_namespaces(default_ns_xml)

    assert_with_msg(
        result == {},
        f"Expected empty dict (default namespace excluded), got {result}",
    )


def test_value_to_truncated_string() -> None:
    """Test func for value_to_truncated_string."""
    # Local constants for this test function
    truncate_length_small = 5
    truncate_length_medium = 15
    truncate_length_large = 20

    # Test with short string
    short_text = "Hello"
    result = value_to_truncated_string(short_text, 10)

    assert_with_msg(
        result == "Hello",
        f"Expected 'Hello', got '{result}'",
    )

    # Test with long string that needs truncation
    long_text = "This is a very long string that should be truncated"
    result = value_to_truncated_string(long_text, truncate_length_large)

    assert_with_msg(
        len(result) <= truncate_length_large,
        f"Expected result length <= {truncate_length_large}, got {len(result)}",
    )
    assert_with_msg(
        result.endswith("..."),
        f"Expected truncated string to end with '...', got '{result}'",
    )

    # Test with non-string object
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = value_to_truncated_string(test_list, truncate_length_medium)

    assert_with_msg(
        len(result) <= truncate_length_medium,
        f"Expected result length <= {truncate_length_medium}, got {len(result)}",
    )

    # Test with exact length
    exact_text = "Exactly20Characters!"
    result = value_to_truncated_string(exact_text, truncate_length_large)

    assert_with_msg(
        result == exact_text,
        f"Expected '{exact_text}', got '{result}'",
    )

    # Test with very small max_length
    result = value_to_truncated_string("Hello World", truncate_length_small)

    assert_with_msg(
        len(result) <= truncate_length_small,
        f"Expected result length <= {truncate_length_small}, got {len(result)}",
    )

    # Test with very small max_length (minimum is 4 for textwrap.shorten with "...")
    min_width = 4  # Must be larger than placeholder length
    result = value_to_truncated_string("Hello World", min_width)

    assert_with_msg(
        len(result) <= min_width,
        f"Expected result length <= {min_width}, got {len(result)}",
    )


def test_get_reusable_hash() -> None:
    """Test func for get_reusable_hash."""
    # Local constant for this test function
    sha256_hex_length = 64

    # Test with string
    test_string = "Hello, World!"
    result = get_reusable_hash(test_string)

    # Verify it's a valid hex string
    assert_with_msg(
        len(result) == sha256_hex_length,
        f"Expected {sha256_hex_length}-character hash, got {len(result)} characters",
    )

    # Verify it's actually hex
    try:
        int(result, 16)
        is_valid_hex = True
    except ValueError:
        is_valid_hex = False

    assert_with_msg(
        is_valid_hex,
        f"Expected valid hex string, got '{result}'",
    )

    # Test consistency - same input should produce same hash
    result2 = get_reusable_hash(test_string)
    assert_with_msg(
        result == result2,
        f"Expected consistent hash, got {result} and {result2}",
    )

    # Test with different input produces different hash
    different_result = get_reusable_hash("Different string")
    assert_with_msg(
        result != different_result,
        "Expected different inputs to produce different hashes",
    )

    # Test with non-string objects
    test_list = [1, 2, 3]
    list_hash = get_reusable_hash(test_list)

    assert_with_msg(
        len(list_hash) == sha256_hex_length,
        f"Expected {sha256_hex_length}-character hash for list, got {len(list_hash)}",
    )

    # Test with number
    number_hash = get_reusable_hash(42)

    assert_with_msg(
        len(number_hash) == sha256_hex_length,
        f"Expected {sha256_hex_length}-char hash for number, got {len(number_hash)}",
    )

    # Verify the hash matches manual calculation
    expected_hash = hashlib.sha256(test_string.encode("utf-8")).hexdigest()
    assert_with_msg(
        result == expected_hash,
        f"Expected {expected_hash}, got {result}",
    )

    # Test with None
    none_hash = get_reusable_hash(None)
    expected_none_hash = hashlib.sha256(b"None").hexdigest()

    assert_with_msg(
        none_hash == expected_none_hash,
        f"Expected {expected_none_hash}, got {none_hash}",
    )


def test_split_on_uppercase() -> None:
    """Test func for split_on_uppercase."""
    # Test with simple string
    result = split_on_uppercase("HelloWorld")
    assert_with_msg(
        result == ["Hello", "World"],
        f"Expected ['Hello', 'World'], got {result}",
    )

    # Test with multiple uppercase letters
    result = split_on_uppercase("SplitCamelCase")
    assert_with_msg(
        result == ["Split", "Camel", "Case"],
        f"Expected ['Split', 'Camel', 'Case'], got {result}",
    )

    # Test with all uppercase
    result = split_on_uppercase("ALLUPPERCASE")
    assert_with_msg(
        result == list("ALLUPPERCASE"),
        f"Expected {list('ALLUPPERCASE')}, got {result}",
    )

    # Test with all lowercase
    result = split_on_uppercase("alllowercase")
    assert_with_msg(
        result == ["alllowercase"],
        f"Expected ['alllowercase'], got {result}",
    )

    # test with numbers
    result = split_on_uppercase("split1Camel2Case")
    assert_with_msg(
        result == ["split1", "Camel2", "Case"],
        f"Expected ['split1', 'Camel2', 'Case'], got {result}",
    )
