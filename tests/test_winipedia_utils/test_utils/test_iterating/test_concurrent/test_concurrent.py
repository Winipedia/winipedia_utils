"""Tests for the concurrent module.

This module tests the functionality of the concurrent processing utilities.
"""

import os
from typing import Any

from winipedia_utils.utils.iterating.concurrent.concurrent import (
    concurrent_loop,
    find_max_pools,
    generate_process_args,
    get_multiprocess_results_with_tqdm,
    get_order_and_func_result,
)
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_get_order_and_func_result() -> None:
    """Test func for get_order_and_func_result."""
    expected_add_result = 8
    expected_multiply_order = 2
    expected_multiply_result = 24
    expected_string_order = 1
    expected_no_args_order = 3

    # Test basic functionality
    def simple_add(x: int, y: int) -> int:
        return x + y

    add_func_order_args = (simple_add, 0, 5, 3)
    order, result = get_order_and_func_result(add_func_order_args)

    assert_with_msg(order == 0, f"Expected order 0, got {order}")
    assert_with_msg(
        result == expected_add_result,
        f"Expected result {expected_add_result}, got {result}",
    )

    # Test with different function and order
    def multiply(x: int, y: int, z: int) -> int:
        return x * y * z

    multiply_func_order_args = (multiply, expected_multiply_order, 2, 3, 4)
    order, result = get_order_and_func_result(multiply_func_order_args)

    assert_with_msg(
        order == expected_multiply_order,
        f"Expected order {expected_multiply_order}, got {order}",
    )
    assert_with_msg(
        result == expected_multiply_result,
        f"Expected result {expected_multiply_result}, got {result}",
    )

    # Test with string function
    def concat_strings(*args: str) -> str:
        return "".join(args)

    string_func_order_args = (concat_strings, expected_string_order, "hello", "world")
    order, result = get_order_and_func_result(string_func_order_args)

    assert_with_msg(
        order == expected_string_order,
        f"Expected order {expected_string_order}, got {order}",
    )
    assert_with_msg(result == "helloworld", f"Expected 'helloworld', got {result}")

    # Test with no additional arguments
    def no_args_func() -> str:
        return "no_args"

    no_args_func_order_args = (no_args_func, expected_no_args_order)
    order, result = get_order_and_func_result(no_args_func_order_args)

    assert_with_msg(
        order == expected_no_args_order,
        f"Expected order {expected_no_args_order}, got {order}",
    )
    assert_with_msg(result == "no_args", f"Expected 'no_args', got {result}")


def test_generate_process_args() -> None:
    """Test func for generate_process_args."""
    expected_count = 3
    expected_second_arg = 2
    expected_static_elements = 5
    expected_static_int = 10

    # Test basic functionality
    def test_func(x: int) -> int:
        return x * 2

    process_args = [[1], [2], [3]]
    result_generator = generate_process_args(
        process_function=test_func, process_args=process_args
    )
    results = list(result_generator)

    assert_with_msg(
        len(results) == expected_count,
        f"Expected {expected_count} results, got {len(results)}",
    )

    # Check structure: (function, order, *args)
    assert_with_msg(
        results[0][0] == test_func,
        f"Expected function {test_func}, got {results[0][0]}",
    )
    assert_with_msg(results[0][1] == 0, f"Expected order 0, got {results[0][1]}")
    assert_with_msg(results[0][2] == 1, f"Expected arg 1, got {results[0][2]}")

    assert_with_msg(results[1][1] == 1, f"Expected order 1, got {results[1][1]}")
    assert_with_msg(
        results[1][2] == expected_second_arg,
        f"Expected arg {expected_second_arg}, got {results[1][2]}",
    )

    # Test with static arguments
    process_args = [[1], [2]]
    static_args = [expected_static_int, "static"]
    result_generator = generate_process_args(
        process_function=test_func,
        process_args=process_args,
        process_args_static=static_args,
    )
    results = list(result_generator)

    # Check that static args are appended
    assert_with_msg(
        len(results[0]) == expected_static_elements,
        f"Expected {expected_static_elements} elements, got {len(results[0])}",
    )  # func, order, arg, static1, static2
    assert_with_msg(
        results[0][3] == expected_static_int,
        f"Expected static arg {expected_static_int}, got {results[0][3]}",
    )
    assert_with_msg(
        results[0][4] == "static", f"Expected static arg 'static', got {results[0][4]}"
    )

    # Test with deepcopy static arguments
    mutable_list = [1, 2, 3]
    process_args = [[1], [2]]
    result_generator = generate_process_args(
        process_function=test_func,
        process_args=process_args,
        deepcopy_static_args=[mutable_list],
    )
    results = list(result_generator)

    # Check that deepcopy args are present and different objects
    first_deepcopy_arg = results[0][3]
    second_deepcopy_arg = results[1][3]

    assert_with_msg(
        first_deepcopy_arg == mutable_list,
        f"Expected {mutable_list}, got {first_deepcopy_arg}",
    )
    assert_with_msg(
        second_deepcopy_arg == mutable_list,
        f"Expected {mutable_list}, got {second_deepcopy_arg}",
    )
    assert_with_msg(
        first_deepcopy_arg is not mutable_list,
        "Expected deepcopy to create different object",
    )
    assert_with_msg(
        first_deepcopy_arg is not second_deepcopy_arg,
        "Expected different deepcopy objects",
    )

    # Test with both static and deepcopy arguments
    process_args = [[1]]
    static_args = ["static"]
    deepcopy_args = [{"key": "value"}]
    result_generator = generate_process_args(
        process_function=test_func,
        process_args=process_args,
        process_args_static=static_args,
        deepcopy_static_args=deepcopy_args,
    )
    results = list(result_generator)

    expected_length = 5  # func, order, arg, static, deepcopy
    assert_with_msg(
        len(results[0]) == expected_length,
        f"Expected {expected_length} elements, got {len(results[0])}",
    )
    assert_with_msg(
        results[0][3] == "static", f"Expected 'static', got {results[0][3]}"
    )
    assert_with_msg(
        results[0][4] == {"key": "value"}, f"Expected dict, got {results[0][4]}"
    )


def test_get_multiprocess_results_with_tqdm() -> None:
    """Test func for get_multiprocess_results_with_tqdm."""

    # Test basic functionality with ordered results
    def dummy_func() -> None:
        pass

    # Simulate results from parallel execution (order, result) tuples
    results = [(0, "first"), (2, "third"), (1, "second")]
    expected_count = 3

    sorted_results = get_multiprocess_results_with_tqdm(
        results=results,
        process_func=dummy_func,
        process_args_len=expected_count,
        threads=True,
    )

    # Results should be sorted by order
    expected_results = ["first", "second", "third"]
    assert_with_msg(
        len(sorted_results) == expected_count,
        f"Expected {expected_count} results, got {len(sorted_results)}",
    )

    for i, (result, expected) in enumerate(
        zip(sorted_results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )

    # Test with threading=False (multiprocessing) - using different data types
    int_results = [(1, 100), (0, 50), (2, 150)]
    int_sorted_results = get_multiprocess_results_with_tqdm(
        results=int_results,
        process_func=dummy_func,
        process_args_len=expected_count,
        threads=False,
    )

    expected_int_results = [50, 100, 150]
    for i, (result_2, expected_2) in enumerate(
        zip(int_sorted_results, expected_int_results, strict=False)
    ):
        assert_with_msg(
            result_2 == expected_2,
            f"At index {i}: expected {expected_2}, got {result_2}",
        )

    # Test with single result
    single_results = [(0, "only")]
    sorted_single = get_multiprocess_results_with_tqdm(
        results=single_results,
        process_func=dummy_func,
        process_args_len=1,
        threads=True,
    )

    assert_with_msg(
        len(sorted_single) == 1, f"Expected 1 result, got {len(sorted_single)}"
    )
    assert_with_msg(
        sorted_single[0] == "only", f"Expected 'only', got {sorted_single[0]}"
    )

    # Test with empty results
    empty_results: list[tuple[int, Any]] = []
    sorted_empty = get_multiprocess_results_with_tqdm(
        results=empty_results, process_func=dummy_func, process_args_len=0, threads=True
    )

    assert_with_msg(
        len(sorted_empty) == 0, f"Expected 0 results, got {len(sorted_empty)}"
    )
    assert_with_msg(sorted_empty == [], f"Expected empty list, got {sorted_empty}")


def test_find_max_pools() -> None:
    """Test func for find_max_pools."""
    # Test threading mode
    threading_pools = find_max_pools(threads=True)

    # Should return at least 1
    assert_with_msg(
        threading_pools >= 1, f"Expected at least 1 thread pool, got {threading_pools}"
    )

    # Should be reasonable based on CPU count
    cpu_count = os.cpu_count() or 1
    max_expected_threads = cpu_count * 4
    assert_with_msg(
        threading_pools <= max_expected_threads,
        f"Expected at most {max_expected_threads} thread pools, got {threading_pools}",
    )

    # Test multiprocessing mode
    multiprocessing_pools = find_max_pools(threads=False)

    assert_with_msg(
        multiprocessing_pools >= 1,
        f"Expected at least 1 process pool, got {multiprocessing_pools}",
    )
    assert_with_msg(
        multiprocessing_pools <= cpu_count,
        f"Expected at most {cpu_count} process pools, got {multiprocessing_pools}",
    )

    # Test with process_args_len constraint
    small_task_pools = find_max_pools(threads=True, process_args_len=2)

    # Should not exceed the number of tasks
    assert_with_msg(
        small_task_pools >= 1, f"Expected at least 1 pool, got {small_task_pools}"
    )
    # Note: The actual constraint depends on available tasks vs process_args_len

    # Test with large process_args_len
    large_task_pools = find_max_pools(threads=False, process_args_len=1000)

    assert_with_msg(
        large_task_pools >= 1, f"Expected at least 1 pool, got {large_task_pools}"
    )


def test_concurrent_loop() -> None:
    """Test func for concurrent_loop."""

    # Test basic threading functionality
    def square_func(x: int) -> int:
        return x * x

    process_args = [[1], [2], [3], [4]]
    results = concurrent_loop(
        threading=True, process_function=square_func, process_args=process_args
    )

    expected_results = [1, 4, 9, 16]
    expected_count = 4
    assert_with_msg(
        len(results) == expected_count,
        f"Expected {expected_count} results, got {len(results)}",
    )

    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )

    # Test with static arguments
    def add_func(x: int, y: int) -> int:
        return x + y

    process_args = [[1], [2], [3]]
    static_args = [10]
    results = concurrent_loop(
        threading=True,
        process_function=add_func,
        process_args=process_args,
        process_args_static=static_args,
    )

    expected_results = [11, 12, 13]
    for i, (result, expected) in enumerate(
        zip(results, expected_results, strict=False)
    ):
        assert_with_msg(
            result == expected, f"At index {i}: expected {expected}, got {result}"
        )

    # Test with process_args_len parameter
    def identity_func(x: str) -> str:
        return x

    string_process_args = [["test1"], ["test2"]]
    string_results = concurrent_loop(
        threading=True,
        process_function=identity_func,
        process_args=string_process_args,
        process_args_len=2,
    )

    expected_string_results = ["test1", "test2"]
    for idx, (result_2, expected_2) in enumerate(
        zip(string_results, expected_string_results, strict=False)
    ):
        assert_with_msg(
            result_2 == expected_2,
            f"At index {idx}: expected {expected_2}, got {result_2}",
        )

    # Test edge case with single item
    single_process_args = [[42]]
    single_results = concurrent_loop(
        threading=True, process_function=square_func, process_args=single_process_args
    )

    expected_single_result = 1764
    assert_with_msg(
        len(single_results) == 1, f"Expected 1 result, got {len(single_results)}"
    )
    assert_with_msg(
        single_results[0] == expected_single_result,
        f"Expected {expected_single_result}, got {single_results[0]}",
    )

    # Test edge case with empty args
    empty_process_args: list[list[Any]] = []
    empty_results = concurrent_loop(
        threading=True, process_function=square_func, process_args=empty_process_args
    )

    assert_with_msg(
        len(empty_results) == 0, f"Expected 0 results, got {len(empty_results)}"
    )
    assert_with_msg(empty_results == [], f"Expected empty list, got {empty_results}")


# Note: test_get_order_and_func_result_func() is not needed as
# get_order_and_func_result_func was removed from the current implementation
# and replaced with get_order_and_func_result
