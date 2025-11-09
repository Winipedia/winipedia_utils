"""Tests module."""

from tests.test_winipedia_utils.test_utils.test_oop.test_mixins import test_meta
from tests.test_winipedia_utils.test_utils.test_testing import test_assertions
from winipedia_utils.dev.testing.utils import (
    assert_no_untested_objs,
)


def test_assert_no_untested_objs() -> None:
    """Test func for _assert_no_untested_objs."""
    # Test with a test function - should not raise (functions have no sub-objects)
    assert_no_untested_objs(test_assert_no_untested_objs)

    # Test with a real test module that we know has complete coverage
    # Use the test_assertions module which should have complete coverage
    # This should not raise since test_assertions should have complete coverage
    assert_no_untested_objs(test_assertions)

    # Test that the function works correctly - it should validate that all
    # source objects have corresponding test objects. Since we're testing
    # with modules that should have complete coverage, no AssertionError
    # should be raised. The function's behavior with incomplete coverage
    # is tested implicitly by the project's test validation system.
    # This should not raise since test_meta should have complete coverage
    assert_no_untested_objs(test_meta)
