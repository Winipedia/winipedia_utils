"""Tests for winipedia_utils.modules.function module."""

import functools

from winipedia_utils.modules.function import (
    get_all_functions_from_module,
    is_func,
    is_func_or_method,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_is_func_or_method() -> None:
    """Test func for is_func_or_method."""

    # Test with regular function
    def regular_function() -> None:
        """Regular function."""

    assert_with_msg(
        is_func_or_method(regular_function),
        "Expected regular function to be identified as func or method",
    )

    # Test with method (bound method)
    class TestClass:
        def instance_method(self) -> None:
            """Instance method."""

        @classmethod
        def class_method(cls) -> None:
            """Class method."""

        @staticmethod
        def static_method() -> None:
            """Return nothing from static method."""

    test_instance = TestClass()

    # Bound method
    assert_with_msg(
        is_func_or_method(test_instance.instance_method),
        "Expected bound instance method to be identified as func or method",
    )

    # Unbound method (function in class namespace)
    assert_with_msg(
        is_func_or_method(TestClass.instance_method),
        "Expected unbound instance method to be identified as func or method",
    )

    # Test with non-function objects
    assert_with_msg(
        not is_func_or_method("string"),
        "Expected string to not be identified as func or method",
    )

    assert_with_msg(
        not is_func_or_method(42),
        "Expected integer to not be identified as func or method",
    )

    assert_with_msg(
        not is_func_or_method([1, 2, 3]),
        "Expected list to not be identified as func or method",
    )

    assert_with_msg(
        not is_func_or_method(TestClass),
        "Expected class to not be identified as func or method",
    )


def test_is_func() -> None:
    """Test func for is_func."""

    # Test with regular function
    def regular_function() -> None:
        """Regular function."""

    assert_with_msg(
        is_func(regular_function),
        "Expected regular function to be identified as func",
    )

    # Test with class containing various method types
    class TestClass:
        def instance_method(self) -> None:
            """Instance method."""

        @classmethod
        def class_method(cls) -> None:
            """Class method."""

        @staticmethod
        def static_method() -> None:
            """Return nothing from static method."""

        @property
        def test_property(self) -> str:
            """Test property."""
            return "test"

    # Test staticmethod descriptor
    assert_with_msg(
        is_func(TestClass.__dict__["static_method"]),
        "Expected staticmethod descriptor to be identified as func",
    )

    # Test classmethod descriptor
    assert_with_msg(
        is_func(TestClass.__dict__["class_method"]),
        "Expected classmethod descriptor to be identified as func",
    )

    # Test property descriptor
    assert_with_msg(
        is_func(TestClass.__dict__["test_property"]),
        "Expected property descriptor to be identified as func",
    )

    # Test instance method (unbound function)
    assert_with_msg(
        is_func(TestClass.__dict__["instance_method"]),
        "Expected instance method to be identified as func",
    )

    # Test decorated function with __wrapped__
    @functools.wraps(regular_function)
    def decorated_function() -> None:
        """Return result from decorated function."""
        return regular_function()

    assert_with_msg(
        is_func(decorated_function),
        "Expected decorated function to be identified as func",
    )

    # Test with non-function objects
    assert_with_msg(
        not is_func("string"),
        "Expected string to not be identified as func",
    )

    assert_with_msg(
        not is_func(42),
        "Expected integer to not be identified as func",
    )

    assert_with_msg(
        not is_func([1, 2, 3]),
        "Expected list to not be identified as func",
    )

    # Test bound method (should still return True)
    test_instance = TestClass()
    assert_with_msg(
        is_func(test_instance.instance_method),
        "Expected bound method to be identified as func",
    )


def test_get_all_functions_from_module() -> None:
    """Test func for get_all_functions_from_module."""
    # Test with winipedia_utils.modules.function module
    from winipedia_utils.modules import function as func_module

    functions = get_all_functions_from_module(func_module)

    # Verify we got some functions
    assert_with_msg(
        len(functions) > 0,
        f"Expected at least 1 function, got {len(functions)}",
    )

    # Verify all returned objects are callable
    for func in functions:
        assert_with_msg(
            callable(func),
            f"Expected function {func.__name__} to be callable",
        )

    # Verify functions have __name__ attribute
    function_names = [func.__name__ for func in functions]
    expected_functions = [
        "is_func_or_method",
        "is_func",
        "get_all_functions_from_module",
    ]

    expected_count = len(expected_functions)
    assert_with_msg(
        len(functions) == expected_count,
        f"Expected {expected_count} functions, got {len(functions)}",
    )

    for expected_name in expected_functions:
        assert_with_msg(
            expected_name in function_names,
            f"Expected function '{expected_name}' to be found",
        )

    # Test with string module name
    functions_from_string = get_all_functions_from_module(
        "winipedia_utils.modules.function"
    )

    assert_with_msg(
        len(functions_from_string) == len(functions),
        "Expected same number of functions when using string module name",
    )

    # Verify all functions are callable
    for func in functions:
        assert_with_msg(
            callable(func),
            f"Expected function {func.__name__} to be callable",
        )
