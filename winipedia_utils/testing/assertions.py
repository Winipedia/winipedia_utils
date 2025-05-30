"""Testing assertion utilities for enhanced test validation.

This module provides custom assertion functions that extend Python's built-in
assert statement with additional features like improved error messages and
specialized validation logic for common testing scenarios.
"""


def assert_with_msg(expr: bool, msg: str) -> None:  # noqa: FBT001
    """Assert that an expression is true with a custom error message.

    A thin wrapper around Python's built-in assert statement that makes it
    easier to provide meaningful error messages when assertions fail.

    Args:
        expr: The expression to evaluate for truthiness
        msg: The error message to display if the assertion fails

    Raises:
        AssertionError: If the expression evaluates to False

    """
    assert expr, msg  # noqa: S101  # nosec: B101
