"""Tests for winipedia_utils.testing.tests.base.utils.utils module."""

from abc import ABC, abstractmethod

from tests.test_winipedia_utils.test_oop.test_mixins import test_meta
from tests.test_winipedia_utils.test_testing import test_assertions
from winipedia_utils.modules.function import is_abstractmethod
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.tests.base.utils.utils import (
    assert_no_untested_objs,
    get_github_token,
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


def test_assert_isabstrct_method() -> None:
    """Test func for assert_isabstrct_method."""

    class AbstractClass(ABC):
        """Abstract class for testing."""

        @abstractmethod
        def abstract_method(self) -> None:
            pass

        def concrete_method(self) -> None:
            """Concrete method."""
            return

    is_abstract = is_abstractmethod(AbstractClass.abstract_method)
    assert_with_msg(
        is_abstract, "Expected abstract method to be identified as abstract"
    )

    is_abstract = is_abstractmethod(AbstractClass.concrete_method)
    assert_with_msg(
        not is_abstract, "Expected concrete method to not be identified as abstract"
    )


def test_get_github_token() -> None:
    """Test func for get_github_token."""
    token = get_github_token()
    assert_with_msg(
        isinstance(token, str), f"Expected token to be str, got {type(token)}"
    )
