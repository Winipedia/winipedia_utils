"""Multithreading utilities for concurrent execution.

This module provides functions for parallel processing using thread pools.
It includes utilities for handling thread pools, managing futures, and organizing
parallel execution of I/O-bound tasks.
Base helper functions that serve threading and processing are located in the
multiprocessing module.

Returns:
    Various utility functions for multithreaded processing.

"""

from collections.abc import Callable, Generator, Iterable
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Any

from winipedia_utils.concurrent.multiprocessing import (
    get_multiprocess_results_with_tqdm,
    get_order_and_func_result,
    prepare_multiprocess_loop,
)


def get_future_results_as_completed(
    futures: Iterable[Future[Any]],
) -> Generator[Any, None, None]:
    """Get future results as they complete.

    Yields results from futures in the order they complete,
    not in the order they were submitted.

    Args:
        futures: List of Future objects to get results from

    Yields:
        The result of each completed future

    """
    for future in as_completed(futures):
        yield future.result()


def multithread_loop(
    process_function: Callable[..., Any],
    process_args: Iterable[Iterable[Any]],
    process_args_static: Iterable[Any] | None = None,
) -> list[Any]:
    """Process a loop using ThreadPoolExecutor for parallel execution.

    Executes the given process_function with the provided arguments in parallel using
    ThreadPoolExecutor, which is suitable for I/O-bound tasks.

    Args:
        process_function: Function that processes the given process_args
        process_args: List of argument lists to be processed by the process_function
        process_args_static: Optional constant arguments passed to each function call

    Returns:
        List of results from the process_function executions

    Note:
        ThreadPoolExecutor is used for I/O-bound tasks, not for CPU-bound tasks.

    """
    process_args, max_workers = prepare_multiprocess_loop(
        threads=True,
        process_func=process_function,
        process_args=process_args,
        process_args_static=process_args_static,
        deepcopy_static_args=None,
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        if max_workers > 1:
            results = [
                executor.submit(get_order_and_func_result, process_args_single)
                for process_args_single in process_args
            ]
            finished_results = get_future_results_as_completed(results)
        else:
            finished_results = (r for r in map(get_order_and_func_result, process_args))

        return get_multiprocess_results_with_tqdm(
            results=finished_results,
            process_func=process_function,
            process_args=process_args,
            threads=True,
        )
