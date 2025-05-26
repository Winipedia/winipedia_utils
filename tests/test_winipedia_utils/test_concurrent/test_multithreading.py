"""Tests for the multithreading module.

This module tests the functionality of the multithreading utilities.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest

from winipedia_utils.concurrent.multithreading import (
    get_future_results_as_completed,
    multithread_loop,
)
from winipedia_utils.testing.assertions import assert_with_msg


# Define test functions at module level
def square(x: int) -> int:
    """Square a number."""
    return x * x


def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def slow_function(delay: float = 0.1) -> str:
    """Take some time to complete and return a result."""
    time.sleep(delay)
    return "done"


# Define a function that can take any type of argument for testing
def generic_function(x: Any) -> Any:
    """Process any type of input and return it."""
    return x


def raise_exception(_x: Any) -> Any:
    """Raise an exception."""
    msg = "Exception raised in raise_exception"
    raise ValueError(msg)


def test_get_future_results_as_completed() -> None:
    """Test get_future_results_as_completed function."""
    # Constants for test values
    num_futures = 3

    # Create a list of futures with different completion times
    with ThreadPoolExecutor(max_workers=num_futures) as executor:
        # Create futures that will complete in reverse order
        futures = [
            executor.submit(slow_function, 0.03),  # Will complete last
            executor.submit(slow_function, 0.02),  # Will complete second
            executor.submit(slow_function, 0.01),  # Will complete first
        ]

        # Get results as they complete
        results = list(get_future_results_as_completed(futures))

        # Verify we got all results
        assert_with_msg(
            len(results) == num_futures,
            f"{get_future_results_as_completed.__name__} should return all results",
        )

        # Verify all results are "done"
        assert_with_msg(
            all(result == "done" for result in results),
            f"{get_future_results_as_completed.__name__} should return correct values",
        )

    # Test with empty futures list
    results = list(get_future_results_as_completed([]))
    assert_with_msg(
        results == [],
        f"{get_future_results_as_completed.__name__} should handle empty futures list",
    )


def test_multithread_loop() -> None:
    """Test multithread_loop functionality."""
    # Test Case 1: Empty process_args
    results = multithread_loop(square, [[]])
    assert_with_msg(
        results == [],
        f"{multithread_loop.__name__} should handle empty process_args correctly",
    )

    # Test Case 2: Basic functionality
    process_args = [[1, 2, 3]]
    results = multithread_loop(square, process_args)

    # Verify results and order preservation
    assert_with_msg(
        results == [1, 4, 9],
        f"{multithread_loop.__name__} should preserve the order of input arguments",
    )

    # Test Case 3: With static arguments
    process_args = [[1, 2, 3]]
    process_args_static = (4,)
    results = multithread_loop(multiply, process_args, process_args_static)

    # Verify results with static arguments
    assert_with_msg(
        results == [4, 8, 12],
        f"{multithread_loop.__name__} should work correctly with static arguments",
    )

    # Test Case 4: Multiple argument lists
    process_args = [[1, 2, 3], [4, 5, 6]]
    results = multithread_loop(add, process_args)
    assert_with_msg(
        results == [5, 7, 9],
        f"{multithread_loop.__name__} should work correctly with multiple arg lists",
    )

    # Test Case 5: Raises if one of the threads raises
    process_args = [[1, 2, 3]]
    with pytest.raises(ValueError, match="Exception raised in raise_exception"):
        multithread_loop(raise_exception, process_args)
