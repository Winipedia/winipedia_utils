"""Multiprocessing utilities for concurrent execution.

This module provides functions for parallel processing using both multiprocessing
and multithreading approaches. It includes utilities for handling timeouts,
managing process pools, and organizing parallel execution of functions.

Returns:
    Various utility functions for concurrent processing.
"""

import copy
import multiprocessing
import os
import threading
from collections.abc import Callable, Iterable
from functools import wraps
from multiprocessing.pool import Pool
from typing import Any

from tqdm import tqdm

from winipedia_utils.logging.logger import get_logger

logger = get_logger(__name__)


def cancel_on_timeout_with_multiprocessing(seconds: int, message: str) -> Callable[..., Any]:
    """Cancel a function execution if it exceeds a specified timeout.

    Creates a wrapper that executes the decorated function in a separate process
    and terminates it if execution time exceeds the specified timeout.

    Args:
        seconds: Maximum execution time in seconds before timeout
        message: Error message to include in the raised TimeoutError

    Returns:
        A decorator function that wraps the target function with timeout functionality

    Raises:
        multiprocessing.TimeoutError: When function execution exceeds the timeout
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            with Pool(processes=1) as pool:
                async_result = pool.apply_async(func, args, kwargs)
                try:
                    return async_result.get(timeout=seconds)
                except multiprocessing.TimeoutError:
                    logger.warning(
                        "%s -> Execution exceeded %s seconds: %s",
                        func.__name__,
                        seconds,
                        message,
                    )
                    pool.terminate()  # Ensure the worker process is killed
                    pool.join()  # Wait for cleanup
                    raise

        return wrapper

    return decorator


def multiprocess_loop(
    process_function: Callable[..., Any],
    process_args: Iterable[Iterable[Any]],
    process_args_static: Iterable[Any] | None = None,
    deepcopy_static_args: Iterable[Any] | None = None,
) -> list[Any]:
    """Process a loop using multiprocessing Pool for parallel execution.

    Executes the given process_function with the provided arguments in parallel using
    multiprocessing Pool, which is suitable for CPU-bound tasks.

    Args:
        process_function: Function that processes the given process_args
        process_args: List of argument lists to be processed by the process_function
        process_args_static: Optional constant arguments passed to each function call
        deepcopy_static_args: Optional arguments that should be deep-copied for each process

    Returns:
        List of results from the process_function executions

    Note:
        Pool is used for CPU-bound tasks as it bypasses Python's GIL by creating separate processes.
        Multiprocessing is not safe for mutable objects unlike ThreadPoolExecutor.
        When debugging, if ConnectionErrors occur, set max_processes to 1.
    """
    max_processes: int
    process_args, max_processes = prepare_multiprocess_loop(
        threads=False,
        process_func=process_function,
        process_args=process_args,
        process_args_static=process_args_static,
        deepcopy_static_args=deepcopy_static_args,
    )

    with Pool(processes=max_processes) as pool:
        if max_processes > 1:
            # using original function without progress bar,
            # bc pickling the wrapper function causes errors in multiprocessing
            results = (
                r
                for r in pool.imap_unordered(
                    process_function_for_imap_with_args_unpacking, process_args
                )
            )
        else:
            # if only one worker is allowed, then process the loop as a single loop
            results = (r for r in map(process_function_for_imap_with_args_unpacking, process_args))

        return get_multiprocess_results_with_tqdm(
            results=results,
            process_func=process_function,
            process_args=process_args,
            threads=False,
        )


def process_function_for_imap_with_args_unpacking(
    func_order_args: tuple[Any, ...],
) -> tuple[int, Any]:
    """Process function for imap with arguments unpacking.

    Helper function that unpacks arguments for use with imap and similar functions.
    Takes a tuple containing the function, order index, and arguments, then
    executes the function with the arguments.

    Args:
        func_order_args: Tuple containing (function, order_index, *args)

    Returns:
        tuple[int, Any]: Tuple of (order_index, function_result)
    """
    func: Callable[..., Any] = func_order_args[0]
    order: int = func_order_args[1]
    args = func_order_args[2:]
    result = func(*args)
    return order, result


def prepare_multiprocess_loop(
    *,
    threads: bool,
    process_func: Callable[..., Any],
    process_args: Iterable[Iterable[Any]],
    process_args_static: Iterable[Any] | None = None,
    deepcopy_static_args: Iterable[Any] | None = None,
) -> tuple[list[tuple[Any, ...]], int]:
    """Prepare arguments for multiprocessing or multithreading execution.

    Converts input arguments into a format suitable for parallel processing,
    organizing them for efficient unpacking during execution. The function:
    1. Converts all process_args to lists for consistency
    2. Prepends the process function and order indices to arguments
    3. Handles static arguments (with optional deep copying)
    4. Determines optimal number of worker processes/threads
    5. Restructures arguments into tuples for unpacking

    Args:
        threads: Whether to use threading (True) or multiprocessing (False)
        process_func: Function to be executed in parallel
        process_args: Iterable of argument lists for each parallel call
        process_args_static: Optional constant arguments to add to each call
        deepcopy_static_args: Optional arguments that should be deep-copied

    Returns:
        tuple: A tuple containing (process_args_tuples, max_pools) where:
            - process_args_tuples: List of argument tuples ready for execution
            - max_pools: Optimal number of worker processes/threads
    """
    # convert all process_args to list for consistency
    process_args_list = [list(process_arg) for process_arg in process_args]

    # for later unpacking and pickle safe processing,
    # the process_func needs to be added to the process_args
    process_args_len = len(process_args_list[0]) if process_args_list else 0
    process_args_list.insert(0, [process_func] * process_args_len)
    # also insert an order number for the process_args,
    # so we can reorder the results later to the original order
    process_args_list.insert(1, list(range(process_args_len)))

    if process_args_static is not None:
        # extend the process_args with the process_args_static
        extend_process_args_with_const_args(
            process_args=process_args_list,
            process_args_static=process_args_static,
            deepcopy_static_args=False,
        )

    if deepcopy_static_args is not None:
        extend_process_args_with_const_args(
            process_args=process_args_list,
            process_args_static=deepcopy_static_args,
            deepcopy_static_args=True,
        )

    max_pools = find_max_pools_for_multiprocessing(
        threads=threads, length_process_args=process_args_len
    )

    # we are ordering the process_args this way so each item is the args for one function call
    # the wrapper function process_function_for_imap_with_args_unpacking will unpack the args
    # so we can pass the same args to built in map, imap_unordered, or submit
    process_args_tuples = [
        tuple(process_arg) for process_arg in zip(*process_args_list, strict=True)
    ]

    return process_args_tuples, max_pools


def get_multiprocess_results_with_tqdm(
    results: Iterable[Any],
    process_func: Callable[..., Any],
    process_args: list[tuple[Any, ...]],
    *,
    threads: bool,
) -> list[Any]:
    """Get multiprocess results with tqdm progress tracking.

    Processes results from parallel execution with a progress bar and ensures
    they are returned in the original order.

    Args:
        results: Iterable of results from parallel execution
        process_func: Function that was executed in parallel
        process_args: List of argument tuples used for execution
        threads: Whether threading (True) or multiprocessing (False) was used

    Returns:
        list[Any]: Results from parallel execution in original order
    """
    results = tqdm(
        results,
        total=len(process_args),
        desc=f"Multi{'threading' if threads else 'processing'} {process_func.__name__}",
        unit=f" {'threads' if threads else 'processes'}",
    )
    results_list = list(results)
    # results list is a tuple of (order, result),
    # so we need to sort it by order to get the original order
    results_list = sorted(results_list, key=lambda x: x[0])
    # now extract the results from the tuple
    return [result[1] for result in results_list]


def find_max_pools_for_multiprocessing(*, threads: bool, length_process_args: int) -> int:
    """Find optimal number of worker processes or threads for parallel execution.

    Determines the maximum number of worker processes or threads based on system
    resources, active tasks, and the number of items to process.

    Args:
        threads: Whether to use threading (True) or multiprocessing (False)
        length_process_args: Number of items to process in parallel

    Returns:
        int: Maximum number of worker processes or threads to use
    """
    cpu_count = os.cpu_count() or 1
    if threads:
        logger.info("Using ThreadPoolExecutor for multithreading.")
        active_tasks = threading.active_count()
        max_tasks = cpu_count * 4
    else:
        logger.info("Using Pool for multiprocessing.")
        active_tasks = len(multiprocessing.active_children())
        max_tasks = cpu_count

    available_tasks = max_tasks - active_tasks
    max_pools = min(max_tasks, available_tasks)
    max_pools = min(max_pools, length_process_args)
    max_pools = max(max_pools, 1)

    logger.info("Multi%s with max_pools: %s", "threading" if threads else "processing", max_pools)

    return max_pools


def extend_process_args_with_const_args(
    process_args: list[list[Any]],
    process_args_static: Iterable[Any],
    *,
    deepcopy_static_args: bool = False,
) -> None:
    """Extend process arguments with constant arguments.

    Adds static arguments to the process arguments list, with optional deep copying
    to prevent shared references across parallel processes.

    Args:
        process_args: List of argument lists for parallel processing
        process_args_static: Iterable of constant arguments to add
        deepcopy_static_args: Whether to create deep copies of static arguments. Defaults to False.
    """
    length_process_args = len(process_args[0])
    for process_arg_static in process_args_static:
        if deepcopy_static_args:
            process_args_static_as_list = [
                copy.deepcopy(process_arg_static) for _ in range(length_process_args)
            ]
        else:
            process_args_static_as_list = [process_arg_static] * length_process_args
        process_args.append(process_args_static_as_list)
