"""Tests for the multithreading module.

This module tests the functionality of the multithreading utilities.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pyrig.src.testing.assertions import assert_with_msg

from winiutils.src.iterating.concurrent.multithreading import (
    get_future_results_as_completed,
    imap_unordered,
    multithread_loop,
)


def test_get_future_results_as_completed() -> None:
    """Test func for get_future_results_as_completed."""
    expected_futures_count = 3
    expected_single_result = 10

    # Test with simple functions that return values
    def simple_task(value: int) -> int:
        return value * 2

    def slow_task(value: int) -> int:
        time.sleep(0.1)  # Small delay to test completion order
        return value * 3

    # Create futures manually
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(simple_task, 1),
            executor.submit(slow_task, 2),
            executor.submit(simple_task, 3),
        ]

        # Get results as they complete
        results = list(get_future_results_as_completed(futures))

        # Should have all results
        assert_with_msg(
            len(results) == expected_futures_count,
            f"Expected {expected_futures_count} results, got {len(results)}",
        )

        # Results should contain expected values
        # (order may vary due to completion timing)
        # 1*2=2, 2*3=6, 3*2=6, so set should be {2, 6}
        expected_values = {2, 6}
        result_set = set(results)
        assert_with_msg(
            result_set == expected_values,
            f"Expected {expected_values}, got {result_set}",
        )

    # Test with empty futures list
    empty_results = list(get_future_results_as_completed([]))
    assert_with_msg(
        len(empty_results) == 0, f"Expected 0 results, got {len(empty_results)}"
    )

    # Test with single future
    with ThreadPoolExecutor(max_workers=1) as executor:
        single_future = [executor.submit(simple_task, 5)]
        single_results = list(get_future_results_as_completed(single_future))
        assert_with_msg(
            len(single_results) == 1, f"Expected 1 result, got {len(single_results)}"
        )
        assert_with_msg(
            single_results[0] == expected_single_result,
            f"Expected {expected_single_result}, got {single_results[0]}",
        )


def test_multithread_loop() -> None:
    """Test func for multithread_loop."""

    # Test basic parallel execution
    def square_function(x: int) -> int:
        return x * x

    process_args = [[1], [2], [3], [4], [5]]
    results = multithread_loop(
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
    def add_function(x: int, y: int) -> int:
        return x + y

    process_args = [[1], [2], [3]]
    static_args = [10]  # Add 10 to each number
    results = multithread_loop(
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
    def multiply_function(x: int, y: int, z: int) -> int:
        return x * y * z

    process_args = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    results = multithread_loop(
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

    # Test with process_args_len parameter
    def simple_identity(x: str) -> str:
        return x

    string_process_args = [["test1"], ["test2"]]
    string_results = multithread_loop(
        process_function=simple_identity,
        process_args=string_process_args,
        process_args_len=2,
    )
    expected_string_results = ["test1", "test2"]
    assert_with_msg(
        len(string_results) == len(expected_string_results),
        f"Expected {len(expected_string_results)} results, got {len(string_results)}",
    )

    for i, (result_2, expected_2) in enumerate(
        zip(string_results, expected_string_results, strict=False)
    ):
        assert_with_msg(
            result_2 == expected_2,
            f"At index {i}: expected {expected_2}, got {result_2}",
        )

    # Test edge case with single item
    expected_square_of_42 = 1764
    single_process_args = [[42]]
    results = multithread_loop(
        process_function=square_function, process_args=single_process_args
    )
    assert_with_msg(len(results) == 1, f"Expected 1 result, got {len(results)}")
    assert_with_msg(
        results[0] == expected_square_of_42,
        f"Expected {expected_square_of_42} (42^2), got {results[0]}",
    )

    # Test edge case with empty args (should return empty list)
    empty_process_args: list[list[Any]] = []
    results = multithread_loop(
        process_function=square_function, process_args=empty_process_args
    )
    assert_with_msg(
        len(results) == 0, f"Expected 0 results for empty args, got {len(results)}"
    )
    assert_with_msg(results == [], f"Expected empty list, got {results}")


def test_imap_unordered() -> None:
    """Test func for imap_unordered."""
    expected_int_count = 5
    expected_string_count = 3
    expected_single_double = 14
    max_parallel_time = 0.5
    expected_parallel_count = 3

    # Test basic functionality
    def double_function(x: int) -> int:
        return x * 2

    with ThreadPoolExecutor(max_workers=3) as executor:
        iterable = [1, 2, 3, 4, 5]
        results = list(imap_unordered(executor, double_function, iterable))

        # Should have all results
        assert_with_msg(
            len(results) == expected_int_count,
            f"Expected {expected_int_count} results, got {len(results)}",
        )

        # Results should contain expected values (order may vary)
        expected_values = {2, 4, 6, 8, 10}  # 1*2, 2*2, 3*2, 4*2, 5*2
        result_set = set(results)
        assert_with_msg(
            result_set == expected_values,
            f"Expected {expected_values}, got {result_set}",
        )

    # Test with string processing
    def uppercase_function(s: str) -> str:
        return s.upper()

    with ThreadPoolExecutor(max_workers=2) as executor:
        string_iterable = ["hello", "world", "test"]
        string_results = list(
            imap_unordered(executor, uppercase_function, string_iterable)
        )

        assert_with_msg(
            len(string_results) == expected_string_count,
            f"Expected {expected_string_count} results, got {len(string_results)}",
        )
        expected_string_values = {"HELLO", "WORLD", "TEST"}
        string_result_set = set(string_results)
        assert_with_msg(
            string_result_set == expected_string_values,
            f"Expected {expected_string_values}, got {string_result_set}",
        )

    # Test with empty iterable
    with ThreadPoolExecutor(max_workers=1) as executor:
        empty_results = list(imap_unordered(executor, double_function, []))
        assert_with_msg(
            len(empty_results) == 0, f"Expected 0 results, got {len(empty_results)}"
        )

    # Test with single item
    with ThreadPoolExecutor(max_workers=1) as executor:
        single_results = list(imap_unordered(executor, double_function, [7]))
        assert_with_msg(
            len(single_results) == 1, f"Expected 1 result, got {len(single_results)}"
        )
        assert_with_msg(
            single_results[0] == expected_single_double,
            f"Expected {expected_single_double}, got {single_results[0]}",
        )

    # Test with function that takes time (to verify parallel execution)
    def slow_function(x: int) -> int:
        time.sleep(0.05)  # Small delay
        return x * 3

    with ThreadPoolExecutor(max_workers=3) as executor:
        start_time = time.time()
        parallel_results = list(imap_unordered(executor, slow_function, [1, 2, 3]))
        end_time = time.time()

        # Should complete faster than sequential execution
        # Sequential would take ~0.15s, parallel should be much faster
        execution_time = end_time - start_time
        assert_with_msg(
            execution_time < max_parallel_time,  # Allow some margin for overhead
            f"Parallel execution took too long: {execution_time:.3f}s",
        )

        assert_with_msg(
            len(parallel_results) == expected_parallel_count,
            f"Expected {expected_parallel_count} results, got {len(parallel_results)}",
        )
        expected_parallel_values = {3, 6, 9}  # 1*3, 2*3, 3*3
        parallel_result_set = set(parallel_results)
        assert_with_msg(
            parallel_result_set == expected_parallel_values,
            f"Expected {expected_parallel_values}, got {parallel_result_set}",
        )
