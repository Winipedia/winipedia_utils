"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_concurrent.test_multiprocessing
"""

import logging
import multiprocessing
import time

import pytest

from winipedia_utils.concurrent.multiprocessing import (
    cancel_on_timeout,
    get_multiprocess_results_with_tqdm,
    get_order_and_func_result,
    multiprocess_loop,
    prepare_multiprocess_loop,
)
from winipedia_utils.testing.assertions import assert_with_msg

TIMEOUT_MESSAGE = "Test timeout"


# Define test functions at module level so they can be pickled
def _quick_function() -> str:
    """Test function that completes quickly."""
    return "completed"


quick_function = cancel_on_timeout(seconds=2, message=TIMEOUT_MESSAGE)(_quick_function)


def _slow_function() -> str:
    """Test function that runs slowly."""
    time.sleep(0.2)
    return "should not reach here"


slow_function = cancel_on_timeout(seconds=0.1, message=TIMEOUT_MESSAGE)(_slow_function)


def _function_with_args(a: int, b: int, c: int = 3) -> int:
    """Test function with arguments."""
    return a + b + c


function_with_args = cancel_on_timeout(seconds=2, message=TIMEOUT_MESSAGE)(
    _function_with_args
)


# Define test functions for multiprocess_loop at module level so they can be pickled
def square(x: int) -> int:
    """Test function that squares a number."""
    return x * x


def multiply(x: int, factor: int) -> int:
    """Test function that multiplies a number by a factor."""
    return x * factor


def add(a: int, b: int) -> int:
    """Test function that adds three numbers."""
    return a + b


def test_cancel_on_timeout(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test cancel_on_timeout decorator functionality."""
    # Test case 1: Function completes before timeout
    result = quick_function()
    assert_with_msg(
        result == "completed",
        "Function with sufficient timeout should complete successfully",
    )

    # Test case 2: Function exceeds timeout
    with pytest.raises(multiprocessing.TimeoutError):
        slow_function()

    # Test case 3: Test with arguments
    result_with_args = function_with_args(1, 2, c=4)
    expected = 1 + 2 + 4
    assert_with_msg(
        result_with_args == expected,
        "Function with arguments should work correctly with the decorator",
    )

    # Test case 4: Verify logging when timeout occurs
    # Clear previous logs
    caplog.clear()

    # Set the log level to capture warnings
    with caplog.at_level(logging.WARNING), pytest.raises(multiprocessing.TimeoutError):
        slow_function()

    # Verify the log message
    assert_with_msg(
        len(caplog.records) == 1,
        "Logger should be called exactly once when timeout occurs",
    )
    assert_with_msg(
        TIMEOUT_MESSAGE in caplog.text,
        "Log message should contain the custom timeout message",
    )
    assert_with_msg(
        f"{slow_function.__name__}" in caplog.text,
        "Log message should contain the function name",
    )
    assert_with_msg(
        "0.1" in caplog.text,
        "Log message should contain the timeout value",
    )


def test_multiprocess_loop() -> None:
    """Test multiprocess_loop functionality."""
    # Test Case 1: no args
    results = multiprocess_loop(square, [[]])
    assert_with_msg(
        results == [],
        f"{multiprocess_loop.__name__} should handle empty process_args correctly",
    )

    # Prepare test data
    process_args = [[1, 2, 3]]

    # Test basic functionality
    results = multiprocess_loop(square, process_args)

    # Verify results and order preservation
    assert_with_msg(
        results == [1, 4, 9],
        f"{multiprocess_loop.__name__} should preserve the order of input arguments",
    )

    # Test with static arguments
    process_args_static = (4,)
    results = multiprocess_loop(multiply, process_args, process_args_static)

    # Verify results and order preservation
    assert_with_msg(
        results == [4, 8, 12],
        f"{multiprocess_loop.__name__} should preserve order",
    )

    # test with several arguments
    process_args = [[1, 2, 3], [4, 5, 6]]
    results = multiprocess_loop(add, process_args)
    assert_with_msg(
        results == [5, 7, 9],
        f"{multiprocess_loop.__name__} should work correctly with several arguments",
    )


def test_get_order_and_func_result() -> None:
    """Test get_order_and_func_result function."""

    # Test case 1: Basic functionality with a simple function
    def simple_func(x: int) -> int:
        return x * 2

    order_index = 5
    args = [10]
    func_order_args = (simple_func, order_index, *args)

    result = get_order_and_func_result(func_order_args)
    assert_with_msg(
        result == (order_index, 20),
        f"{get_order_and_func_result.__name__} should return a tuple of "
        f"(order_index, function_result)",
    )

    # Test case 2: Function with multiple arguments
    def multi_arg_func(a: int, b: int, c: int) -> int:
        return a + b + c

    order_index = 3
    args = [1, 2, 3]
    func_order_args = (multi_arg_func, order_index, *args)

    result = get_order_and_func_result(func_order_args)
    assert_with_msg(
        result == (order_index, 6),
        f"{get_order_and_func_result.__name__} should correctly handle functions "
        f"with multiple arguments",
    )

    # Test case 3: Function with keyword arguments (passed as positional)
    def kw_func(a: int, b: int = 5) -> int:
        return a * b

    order_index = 7
    args = [3, 4]  # b=4 overrides default
    func_order_args = (kw_func, order_index, *args)

    result = get_order_and_func_result(func_order_args)
    assert_with_msg(
        result == (order_index, 12),
        f"{get_order_and_func_result.__name__} should handle functions "
        f"with default arguments",
    )

    # Test case 4: Function returning complex types
    def list_func(x: int) -> list[int]:
        return [x, x * 2, x * 3]

    order_index = 9
    args = [2]
    func_order_args = (list_func, order_index, *args)

    result = get_order_and_func_result(func_order_args)
    assert_with_msg(
        result == (order_index, [2, 4, 6]),
        f"{get_order_and_func_result.__name__} should handle functions "
        f"returning complex types",
    )


def test_prepare_multiprocess_loop() -> None:
    """Test prepare_multiprocess_loop function."""
    # Test case 1: Basic functionality with multiprocessing
    process_args = [[1, 2, 3]]
    result_args, _max_processes = prepare_multiprocess_loop(
        threads=False,
        process_func=square,
        process_args=process_args,
    )
    # Verify structure of prepared arguments
    assert_with_msg(
        len(result_args) == len(process_args[0]),
        "prepare_multiprocess_loop should return one tuple per item in the first list",
    )
    # First element should be the function
    assert_with_msg(
        result_args[0] == (square, 0, 1),
        "First tuple should contain the function, order index, and argument",
    )

    # Test case 2: With static arguments
    process_args_static = (4,)
    result_args, _ = prepare_multiprocess_loop(
        threads=True,
        process_func=multiply,
        process_args=process_args,
        process_args_static=process_args_static,
    )

    # Verify static arguments are added correctly
    assert_with_msg(
        len(result_args) == len(process_args[0]),
        "prepare_multiprocess_loop should return one tuple per item in the first list",
    )

    # Check the structure of the first tuple
    assert_with_msg(
        result_args[0] == (multiply, 0, 1, 4),
        "First tuple should contain the function, order index, and arguments",
    )

    # Test case 3: Test with deepcopy_static_args parameter
    deepcopy_static_args = ({"key": "value"},)
    result_args, _ = prepare_multiprocess_loop(
        threads=False,
        process_func=square,
        process_args=process_args,
        process_args_static=process_args_static,
        deepcopy_static_args=deepcopy_static_args,
    )

    # Verify we have the right number of tuples
    assert_with_msg(
        len(result_args) == len(process_args[0]),
        "prepare_multiprocess_loop should return one tuple per item in the first list",
    )

    # Check that the static arguments have the expected value
    assert_with_msg(
        result_args[0] == (square, 0, 1, 4, {"key": "value"}),
        "Static arguments should have the expected value",
    )
    # Check that the static arguments are deep copied
    assert_with_msg(
        result_args[0][-1] is not result_args[1][-1]
        and result_args[0][-1] == result_args[1][-1],
        "Static arguments should be deep copied",
    )


def test_get_multiprocess_results_with_tqdm() -> None:
    """Test get_multiprocess_results_with_tqdm function."""
    # Test case 1: Basic functionality with threading
    # Create a simple iterable of results (order, value)
    results = [(1, "b"), (0, "a"), (2, "c")]
    process_args = [(square, 0, 1), (square, 1, 2), (square, 2, 3)]

    sorted_results = get_multiprocess_results_with_tqdm(
        results=iter(results),  # Convert to iterator
        process_func=square,
        process_args=process_args,
        threads=True,
    )

    # Verify results are sorted by order and only values are returned
    assert_with_msg(
        sorted_results == ["a", "b", "c"],
        f"{get_multiprocess_results_with_tqdm.__name__} should sort results by order",
    )

    # Test case 2: Empty results
    empty_results = get_multiprocess_results_with_tqdm(
        results=iter([]),
        process_func=square,
        process_args=[],
        threads=False,
    )

    assert_with_msg(
        empty_results == [],
        f"{get_multiprocess_results_with_tqdm.__name__} should handle empty results",
    )


def test_find_max_pools_for_multiprocessing() -> None:
    """Test find_max_pools_for_multiprocessing function."""
    from winipedia_utils.concurrent.multiprocessing import (
        find_max_pools_for_multiprocessing,
    )

    # Constants for test values
    test_length = 10
    min_expected = 1

    # Test case 1: Basic functionality with threading
    max_pools = find_max_pools_for_multiprocessing(
        threads=True, length_process_args=test_length
    )
    assert_with_msg(
        max_pools >= min_expected and max_pools <= test_length,
        f"{find_max_pools_for_multiprocessing.__name__} should return valid pool count",
    )

    # Test case 2: Basic functionality with multiprocessing
    max_pools = find_max_pools_for_multiprocessing(
        threads=False, length_process_args=test_length
    )
    assert_with_msg(
        max_pools >= min_expected and max_pools <= test_length,
        f"{find_max_pools_for_multiprocessing.__name__} should return valid pool count",
    )

    # Test case 3: Small process_args (should limit max_pools)
    small_length = 1
    max_pools = find_max_pools_for_multiprocessing(
        threads=True, length_process_args=small_length
    )
    assert_with_msg(
        max_pools == small_length,
        f"{find_max_pools_for_multiprocessing.__name__} should limit pools correctly",
    )

    # Test case 4: Zero process_args (should return at least 1)
    zero_length = 0
    max_pools = find_max_pools_for_multiprocessing(
        threads=False, length_process_args=zero_length
    )
    assert_with_msg(
        max_pools == min_expected,
        f"{find_max_pools_for_multiprocessing.__name__} should return at least 1",
    )


def test_extend_process_args_with_const_args() -> None:
    """Test extend_process_args_with_const_args function."""
    from winipedia_utils.concurrent.multiprocessing import (
        extend_process_args_with_const_args,
    )

    # Test case 1: Basic functionality without deep copying
    process_args = [[1, 2, 3], [4, 5, 6]]
    static_args = ("static",)

    extend_process_args_with_const_args(
        process_args=process_args,
        process_args_static=static_args,
        deepcopy_static_args=False,
    )

    # Verify static arguments are added correctly
    assert_with_msg(
        process_args == [[1, 2, 3], [4, 5, 6], ["static", "static", "static"]],
        f"{extend_process_args_with_const_args.__name__} should add new lists",
    )

    # Test case 2: With deep copying of mutable objects
    process_args = [[1, 2, 3], [4, 5, 6]]
    mutable_obj = {"key": "value"}

    extend_process_args_with_const_args(
        process_args=process_args,
        process_args_static=(mutable_obj,),
        deepcopy_static_args=True,
    )

    # Check that the mutable object was added
    assert_with_msg(
        process_args == [[1, 2, 3], [4, 5, 6], [mutable_obj, mutable_obj, mutable_obj]],
        f"{extend_process_args_with_const_args.__name__} should add mutable objects",
    )
