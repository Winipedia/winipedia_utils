"""Tests for the multiprocessing module."""

import multiprocessing
import time
from typing import Any

from winipedia_utils.utils.iterating.concurrent.multiprocessing import (
    cancel_on_timeout,
    get_spwan_pool,
    multiprocess_loop,
)
from winipedia_utils.utils.testing.assertions import assert_with_msg


# Module-level functions for multiprocessing tests (must be pickle-able)
def quick_function(x: int, y: int = 10) -> int:
    """Quick function for testing timeout functionality."""
    return x + y


def slow_function() -> str:
    """Slow function for testing timeout behavior."""
    time.sleep(2.0)  # Sleep longer than timeout
    return "completed"


def function_with_args(name: str, count: int, multiplier: float = 1.0) -> str:
    """Function with various argument types for testing."""
    return f"{name}_{count * multiplier}"


def instant_function() -> str:
    """Instant function for testing zero timeout."""
    return "instant"


def square_function(x: int) -> int:
    """Square function for testing basic parallel execution."""
    return x * x


def add_function(x: int, y: int) -> int:
    """Add function for testing static arguments."""
    return x + y


def multiply_function(x: int, y: int, z: int) -> int:
    """Multiply function for testing multiple arguments."""
    return x * y * z


def append_to_list(item: str, target_list: list[str]) -> list[str]:
    """Append function for testing deepcopy arguments."""
    target_list.append(item)
    return target_list.copy()


def simple_identity(x: str) -> str:
    """Identity function for testing process_args_len."""
    return x


def test_get_spwan_pool() -> None:
    """Test func for get_spwan_pool."""
    with get_spwan_pool(processes=1) as pool:
        ctx = getattr(pool, "_ctx", None)
        method = getattr(ctx, "get_start_method", lambda: None)()
        assert_with_msg(method == "spawn", "Expected spawn context")


def test_cancel_on_timeout() -> None:
    """Test func for cancel_on_timeout."""
    expected_sum = 20
    expected_result = "test_10.0"

    # Test successful execution within timeout
    wrapped_func = cancel_on_timeout(seconds=1.0, message="Test timeout")(
        quick_function
    )
    result = wrapped_func(5, y=15)
    assert_with_msg(result == expected_sum, f"Expected {expected_sum}, got {result}")

    # Test timeout behavior
    wrapped_slow_func = cancel_on_timeout(seconds=0.5, message="Slow function timeout")(
        slow_function
    )

    try:
        wrapped_slow_func()
        assert_with_msg(expr=False, msg="Expected TimeoutError to be raised")
    except multiprocessing.TimeoutError:
        pass  # Expected behavior

    # Test with different argument types
    wrapped_args_func = cancel_on_timeout(seconds=1.0, message="Args test timeout")(
        function_with_args
    )
    result = wrapped_args_func("test", 5, multiplier=2.0)
    assert_with_msg(
        result == expected_result, f"Expected '{expected_result}', got {result}"
    )

    # Test edge case with zero timeout (should timeout immediately)
    wrapped_instant = cancel_on_timeout(seconds=0.0, message="Zero timeout")(
        instant_function
    )

    try:
        wrapped_instant()
        assert_with_msg(expr=False, msg="Expected TimeoutError with zero timeout")
    except multiprocessing.TimeoutError:
        pass  # Expected behavior


def test_multiprocess_loop() -> None:
    """Test func for multiprocess_loop."""
    # Test basic parallel execution
    process_args = [[1], [2], [3], [4], [5]]
    results = multiprocess_loop(
        process_function=square_function, process_args=process_args
    )
    expected_results = [1, 4, 9, 16, 25]
    assert_with_msg(
        len(results) == len(expected_results),
        f"Expected {len(expected_results)} results, got {len(results)}",
    )

    # Results should be in original order
    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )

    # Test with static arguments
    process_args = [[1], [2], [3]]
    static_args = [10]  # Add 10 to each number
    results = multiprocess_loop(
        process_function=add_function,
        process_args=process_args,
        process_args_static=static_args,
    )
    expected_results = [11, 12, 13]
    assert_with_msg(
        len(results) == len(expected_results),
        f"Expected {len(expected_results)} results, got {len(results)}",
    )

    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )

    # Test with multiple arguments per function call
    process_args = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    results = multiprocess_loop(
        process_function=multiply_function, process_args=process_args
    )
    expected_results = [6, 24, 60]  # 1*2*3, 2*3*4, 3*4*5
    assert_with_msg(
        len(results) == len(expected_results),
        f"Expected {len(expected_results)} results, got {len(results)}",
    )

    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )

    # Test edge case with single item
    single_process_args = [[42]]
    results = multiprocess_loop(
        process_function=square_function, process_args=single_process_args
    )
    assert_with_msg(len(results) == 1, f"Expected 1 result, got {len(results)}")
    expected_square_of_42 = 1764
    assert_with_msg(
        results[0] == expected_square_of_42,
        f"Expected {expected_square_of_42} (42^2), got {results[0]}",
    )

    # Test edge case with empty args (should return empty list)
    empty_process_args: list[list[Any]] = []
    results = multiprocess_loop(
        process_function=square_function, process_args=empty_process_args
    )
    assert_with_msg(results == [], f"Expected empty list, got {results}")


def test_multiprocess_loop_with_deepcopy_args() -> None:
    """Test multiprocess_loop with deepcopy static arguments."""
    # Test with deepcopy static arguments
    process_args = [["a"], ["b"], ["c"]]
    deepcopy_args: list[list[str]] = [
        []
    ]  # Empty list that should be deep copied for each process
    results = multiprocess_loop(
        process_function=append_to_list,
        process_args=process_args,
        deepcopy_static_args=deepcopy_args,
    )
    expected_results: list[list[str]] = [["a"], ["b"], ["c"]]
    assert_with_msg(
        len(results) == len(expected_results),
        f"Expected {len(expected_results)} results, got {len(results)}",
    )

    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )


def test_multiprocess_loop_with_process_args_len() -> None:
    """Test multiprocess_loop with process_args_len parameter."""
    # Test with process_args_len parameter
    process_args = [["test1"], ["test2"]]
    results = multiprocess_loop(
        process_function=simple_identity, process_args=process_args, process_args_len=2
    )
    expected_results: list[str] = ["test1", "test2"]
    assert_with_msg(
        len(results) == len(expected_results),
        f"Expected {len(expected_results)} results, got {len(results)}",
    )

    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )
