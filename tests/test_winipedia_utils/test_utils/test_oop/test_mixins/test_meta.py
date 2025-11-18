"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_oop.test_mixins.test_meta
"""

from typing import Any

from pyrig.src.modules.function import is_func
from pyrig.src.modules.module import make_obj_importpath
from pyrig.src.testing.assertions import assert_with_msg
from pytest_mock import MockFixture

from winipedia_utils.src.data.structures.text.string import value_to_truncated_string
from winipedia_utils.src.oop.mixins import meta
from winipedia_utils.src.oop.mixins.meta import (
    ABCLoggingMeta,
)


class TestABCLoggingMeta:
    """Test class for LoggingMeta."""

    def test___new__(self) -> None:
        """Test method for __new__."""

        # Create a class with LoggingMeta to test that it works
        class TestClass(metaclass=ABCLoggingMeta):
            def test_method(self) -> str:
                return "test"

        # Verify the class was created successfully
        assert_with_msg(
            type(TestClass).__name__ == f"{ABCLoggingMeta.__name__}",
            "Expected TestClass to be created with LoggingMeta",
        )

        # Verify that methods are wrapped (they should have different behavior)
        instance = TestClass()
        result = instance.test_method()
        assert_with_msg(
            result == "test",
            f"Expected method to return 'test', got {result}",
        )

    def test___new___skips_non_loggable_methods(self, mocker: MockFixture) -> None:
        """Test that __new__ skips non-loggable methods."""
        # Mock is_loggable_method to return False
        mock_is_loggable = mocker.patch.object(
            ABCLoggingMeta, "is_loggable_method", return_value=False
        )
        mock_wrap_logging = mocker.patch.object(ABCLoggingMeta, "wrap_with_logging")

        # Create a class with LoggingMeta
        class TestClass(metaclass=ABCLoggingMeta):
            def __init__(self) -> None:
                pass

        # Verify the class was created successfully
        assert_with_msg(
            type(TestClass) is ABCLoggingMeta,
            "Expected TestClass to be created with LoggingMeta",
        )

        # Verify is_loggable_method was called
        mock_is_loggable.assert_called()

        # Verify wrap_with_logging was NOT called for non-loggable methods
        mock_wrap_logging.assert_not_called()

    def test_is_loggable_method(self, mocker: MockFixture) -> None:
        """Test method for is_loggable_method."""
        # Mock is_func to control its behavior
        mock_is_func = mocker.patch(make_obj_importpath(is_func))

        # Test case 1: Regular method (should be loggable)
        def regular_method() -> None:
            pass

        regular_method.__name__ = "regular_method"
        mock_is_func.return_value = True

        result = ABCLoggingMeta.is_loggable_method(regular_method)
        assert_with_msg(result is True, "Expected regular method to be loggable")

        # Test case 2: Magic method (should not be loggable)
        def magic_method() -> None:
            pass

        magic_method.__name__ = "__init__"
        mock_is_func.return_value = True

        result = ABCLoggingMeta.is_loggable_method(magic_method)
        assert_with_msg(result is False, "Expected magic method to not be loggable")

        # Test case 3: Non-function (should not be loggable)
        mock_is_func.return_value = False
        non_function: Any = 42  # Not a function

        result = ABCLoggingMeta.is_loggable_method(non_function)
        assert_with_msg(result is False, "Expected non-function to not be loggable")

    def test_wrap_with_logging(self, mocker: MockFixture) -> None:
        """Test method for wrap_with_logging."""
        # Mock dependencies
        mock_logger = mocker.patch(make_obj_importpath(meta) + ".logger")
        mock_time = mocker.patch("time.time")
        mock_value_to_truncated_string = mocker.patch(
            make_obj_importpath(value_to_truncated_string)
        )

        # Set up time mock to simulate passage of time
        mock_time.side_effect = [1000.0, 1000.5, 1001.0]  # start, during, end
        mock_value_to_truncated_string.return_value = "truncated"

        # Create a test function to wrap
        def test_func(self: object, arg1: str, arg2: int = 42) -> str:  # noqa: ARG001
            return f"result_{arg1}_{arg2}"

        test_func.__name__ = "test_func"

        # Wrap the function
        call_times: dict[str, float] = {}
        wrapped_func = ABCLoggingMeta.wrap_with_logging(
            test_func, "TestClass", call_times
        )

        # Create a mock self object
        mock_self = mocker.MagicMock()

        # Call the wrapped function
        result = wrapped_func(mock_self, "hello", arg2=100)

        # Verify the result
        assert_with_msg(
            result == "result_hello_100",
            f"Expected 'result_hello_100', got {result}",
        )

        # Verify logging was called (should log because it's the first call)
        expected_log_calls = 2  # start and end logging
        actual_log_calls = mock_logger.info.call_count
        assert_with_msg(
            actual_log_calls == expected_log_calls,
            f"Expected {expected_log_calls} log calls, got {actual_log_calls}",
        )

        # Verify call time was recorded
        assert_with_msg(
            "test_func" in call_times,
            "Expected call time to be recorded for test_func",
        )

    def test_wrap_with_logging_rate_limiting(self, mocker: MockFixture) -> None:
        """Test that wrap_with_logging implements rate limiting."""
        # Mock dependencies
        mock_logger = mocker.patch(make_obj_importpath(meta) + ".logger")
        mock_time = mocker.patch("time.time")

        # Set up time mock to simulate rapid calls (within threshold)
        mock_time.side_effect = [1000.0, 1000.5, 1000.5, 1000.6]

        # Create a test function
        def test_func(self: object) -> str:  # noqa: ARG001
            return "result"

        test_func.__name__ = "test_func"

        # Wrap the function
        call_times: dict[str, float] = {}
        wrapped_func = ABCLoggingMeta.wrap_with_logging(
            test_func, "TestClass", call_times
        )

        mock_self = mocker.MagicMock()

        # First call - should log
        wrapped_func(mock_self)
        first_call_count = mock_logger.info.call_count

        # Second call within threshold - should not log
        wrapped_func(mock_self)
        second_call_count = mock_logger.info.call_count

        # Verify rate limiting worked
        assert_with_msg(
            second_call_count == first_call_count,
            "Expected no additional logging due to rate limiting",
        )
