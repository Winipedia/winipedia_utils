"""Tests for winipedia_utils.testing.tests.base.utils.utils module."""

from pathlib import Path

from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.tests.base.utils.utils import (
    _assert_no_untested_objs,
    _conftest_content_is_correct,
    _get_conftest_content,
    _get_test_0_content,
    _test_0_content_is_correct,
)


def test__assert_no_untested_objs() -> None:
    """Test func for _assert_no_untested_objs."""
    # Test with a test function - should not raise (functions have no sub-objects)
    _assert_no_untested_objs(test__assert_no_untested_objs)

    # Test with another test function from this module
    _assert_no_untested_objs(test__get_conftest_content)

    # Test with a real test module that we know has complete coverage
    # Use the test_assertions module which should have complete coverage
    from tests.test_winipedia_utils.test_testing import test_assertions

    # This should not raise since test_assertions should have complete coverage
    _assert_no_untested_objs(test_assertions)

    # Test that the function works correctly - it should validate that all
    # source objects have corresponding test objects. Since we're testing
    # with modules that should have complete coverage, no AssertionError
    # should be raised. The function's behavior with incomplete coverage
    # is tested implicitly by the project's test validation system.

    from tests.test_winipedia_utils.test_oop.test_mixins import test_meta

    # This should not raise since test_meta should have complete coverage
    _assert_no_untested_objs(test_meta)


def test__get_conftest_content() -> None:
    """Test func for _get_conftest_content."""
    content = _get_conftest_content()

    # Verify the content is a string (type check for robustness)
    assert_with_msg(
        type(content) is str,
        f"Expected string content, got {type(content)}",
    )

    # Verify the content is not empty
    assert_with_msg(
        len(content) > 0,
        "Expected non-empty content",
    )

    # Verify the content contains expected elements
    assert_with_msg(
        "pytest_plugins" in content,
        "Expected 'pytest_plugins' in conftest content",
    )

    assert_with_msg(
        "winipedia_utils.testing.tests.conftest" in content,
        "Expected winipedia_utils plugin reference in content",
    )

    # Verify the content has proper docstring
    assert_with_msg(
        '"""Pytest configuration for tests.' in content,
        "Expected proper docstring in conftest content",
    )

    # Verify the content mentions test scopes
    assert_with_msg(
        "function, class, module, package, session" in content,
        "Expected test scopes mentioned in content",
    )

    # Verify the content has the warning about manual modification
    assert_with_msg(
        "should not be modified manually" in content,
        "Expected warning about manual modification",
    )


def test__conftest_content_is_correct(tmp_path: Path) -> None:
    """Test func for _conftest_content_is_correct."""
    # Test with non-existent file
    non_existent_path = tmp_path / "non_existent_conftest.py"
    result = _conftest_content_is_correct(non_existent_path)
    assert_with_msg(
        result is False,
        f"Expected False for non-existent file, got {result}",
    )

    # Test with correct content
    correct_conftest_path = tmp_path / "correct_conftest.py"
    correct_content = _get_conftest_content()
    correct_conftest_path.write_text(correct_content)

    result = _conftest_content_is_correct(correct_conftest_path)
    assert_with_msg(
        result is True,
        f"Expected True for correct content, got {result}",
    )

    # Test with correct content plus extra content (should still be True)
    extended_conftest_path = tmp_path / "extended_conftest.py"
    extended_content = correct_content + "\n\n# Additional custom content\n"
    extended_conftest_path.write_text(extended_content)

    result = _conftest_content_is_correct(extended_conftest_path)
    assert_with_msg(
        result is True,
        f"Expected True for extended content, got {result}",
    )

    # Test with incorrect content
    incorrect_conftest_path = tmp_path / "incorrect_conftest.py"
    incorrect_content = '''"""Wrong conftest content."""

# This is not the correct content
pytest_plugins = ["wrong.plugin"]
'''
    incorrect_conftest_path.write_text(incorrect_content)

    result = _conftest_content_is_correct(incorrect_conftest_path)
    assert_with_msg(
        result is False,
        f"Expected False for incorrect content, got {result}",
    )

    # Test with empty file
    empty_conftest_path = tmp_path / "empty_conftest.py"
    empty_conftest_path.write_text("")

    result = _conftest_content_is_correct(empty_conftest_path)
    assert_with_msg(
        result is False,
        f"Expected False for empty file, got {result}",
    )

    # Test with partial correct content (should be False)
    partial_conftest_path = tmp_path / "partial_conftest.py"
    partial_content = (
        '"""Pytest configuration for tests.'  # Only part of the expected content
    )
    partial_conftest_path.write_text(partial_content)

    result = _conftest_content_is_correct(partial_conftest_path)
    assert_with_msg(
        result is False,
        f"Expected False for partial content, got {result}",
    )


def test__get_test_0_content() -> None:
    """Test func for _get_test_0_content."""
    content = _get_test_0_content()
    assert_with_msg(
        type(content) is str,
        f"Expected string content, got {type(content)}",
    )
    assert_with_msg(
        len(content) > 0,
        "Expected non-empty content",
    )


def test__test_0_content_is_correct() -> None:
    """Test func for _test_0_content_is_correct."""
    non_existent_path = Path("non_existent_test_0.py")
    result = _test_0_content_is_correct(non_existent_path)
    assert_with_msg(
        result is False,
        f"Expected False for non-existent file, got {result}",
    )
    correct_content = _get_test_0_content()
    correct_path = Path("correct_test_0.py")
    correct_path.write_text(correct_content)
    result = _test_0_content_is_correct(correct_path)
    assert_with_msg(
        result is True,
        f"Expected True for correct content, got {result}",
    )
