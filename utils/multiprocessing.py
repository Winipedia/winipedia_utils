import copy
import multiprocessing
import os
import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from functools import wraps
from multiprocessing.pool import Pool
from multiprocessing.pool import ThreadPool as PoolThreadPool
from typing import Any, Callable, Generator, Iterable, List, Tuple

from tqdm import tqdm

from utils.logging.logger import get_logger

logger = get_logger(__name__)


def cancel_on_timeout_with_multiprocessing(
    seconds: int, message: str
) -> Callable[[Callable[[Any, Any], Any]], Callable[[Any, Any], Any]]:
    """Timeout decorator, parameter in seconds."""

    def decorator(func: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
        """Wrap the original function."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Closure for function."""
            with PoolThreadPool(processes=1) as pool:
                async_result = pool.apply_async(func, args, kwargs)
                try:
                    return async_result.get(timeout=seconds)
                except multiprocessing.context.TimeoutError:
                    # with block will terminate the pool after __exit__
                    logger.warning(
                        f"{func.__name__} -> Execution exceeded {seconds} seconds: {message}"
                    )
                    raise multiprocessing.context.TimeoutError(message)

        return wrapper

    return decorator


def _get_future_results_as_completed(
    futures: List[Future[Any]],
) -> Generator[Any, None, None]:
    """
    This function gets the results from the futures with as_completed.
    :param futures: list, the list of futures
    :return: list, the list of results from the futures
    """
    for future in as_completed(futures):
        yield future.result()


def multithread_loop(
    process_function: Callable[[Any, Any], Any],
    process_args: Iterable[Iterable[Any]],
    process_args_static: Iterable[Any] | None = None,
) -> List[Any]:
    """
    This function processes a loop of a given process_function with the given process_args in a ThreadPoolExecutor.
    :param process_function: function, the function that processes the given process_args
    :param process_args: list, the list of arguments that are processed by the process_function
    :param process_args_static: list, the list of constant arguments that are processed by the process_function
    :return: list, the list of results from the process_function

    NOTE: ThreadPoolExecutor is used for Input/Output bound tasks, not for CPU bound tasks.
    """

    process_args, max_workers = _prepare_multiprocess_loop(
        threads=True,
        process_func=process_function,
        process_args=process_args,
        process_args_static=process_args_static,
        deepcopy_static_args=None,
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        if max_workers > 1:
            results = [
                executor.submit(
                    _process_function_for_imap_with_args_unpacking, process_args_single
                )
                for process_args_single in process_args
            ]
            results = _get_future_results_as_completed(results)
        else:
            results = map(_process_function_for_imap_with_args_unpacking, process_args)

        results_list = _get_multiprocess_results_with_tqdm(
            results=results,
            process_func=process_function,
            process_args=process_args,
            threads=True,
        )

    # convert to list to make sure that the results are processed
    return results_list


def multiprocess_loop(
    process_function: Callable[[Any, Any], Any],
    process_args: Iterable[Iterable[Any]],
    process_args_static: Iterable[Any] | None = None,
    deepcopy_static_args: Iterable[Any] | None = None,
) -> List[Any]:
    """
    This function processes a loop of a given process_function with the given process_args in a ThreadPoolExecutor.
    :param process_function: function, the function that processes the given process_args
    :param process_args: list of lists as expected by a thread pool executor, will be converted for starmap
    :param process_args_static: list, the list of constant arguments that are processed by the process_function
    :param deepcopy_static_args: list, the list of static args that should be deep-copied for each process
    :return: list, the list of results from the process_function

    NOTE: Pool is used for CPU bound tasks, not for Input/Output bound tasks.
        It goes around Pythons GIL Lock by creating separate processes.
    NOTE: Multiprocessing is not safe for mutables like ThreadPoolExecutors are.
    NOTE: In the debugger the multiprocessing module sometimes causes ConnectionErrors or similar
        bc of the way the debugger works. In that case just reduce the max_processes to 1,
        and it will run like a single loop and the debugger shouldn't cause any problems.
    """
    process_args: List[List[Any]]
    max_processes: int
    process_args, max_processes = _prepare_multiprocess_loop(
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
            results = pool.imap_unordered(
                _process_function_for_imap_with_args_unpacking, process_args
            )
        else:
            # if only one worker is allowed, then process the loop as a single loop
            results = map(_process_function_for_imap_with_args_unpacking, process_args)

        results_list = _get_multiprocess_results_with_tqdm(
            results=results,
            process_func=process_function,
            process_args=process_args,
            threads=False,
        )

    return results_list


def _process_function_for_imap_with_args_unpacking(
    func_order_args: Tuple[Callable[[Any, Any], Any], int, List[Any]],
) -> Tuple[int, Any]:
    """
    This function processes the given function with the given arguments.
    :param func_order_args: tuple, the tuple of the function, the order, and the arguments
    The order is a number that is the index of the process_args, so we can reorder the results later to the original order
    """
    func, order, args = func_order_args[0], func_order_args[1], func_order_args[2:]
    result: Any = func(*args)
    return order, result


def _prepare_multiprocess_loop(
    threads: bool,
    process_func: Callable[[Any, Any], Any],
    process_args: Iterable[Iterable[Any]],
    process_args_static: Iterable[Any] | None = None,
    deepcopy_static_args: Iterable[Any] | None = None,
) -> Tuple[List[List[Any]], int]:
    """
    This function prepares the process_args for the multiprocess loop.
    :param threads: bool, if the loop is for threads else for processes
    :param process_func: function, the function that processes the given process_args
    :param process_args: list, the list of arguments that are processed by the process_function,
        should be given as expected by the ThreadPoolExecutor as a list of lists.
    :param process_args_static: list, the list of constant arguments that are processed by the process_function
    :param deepcopy_static_args: list, the list of static args that should be deep-copied for each process
    """

    # convert all process_args to list in case a generator is passed as iterable
    process_args = [list(process_arg) for process_arg in process_args]

    # for later unpacking and pickle safe processing, the process_func needs to be added to the process_args
    process_args_len = len(process_args[0]) if process_args else 0
    process_args.insert(0, [process_func] * process_args_len)
    # also insert an order number for the process_args, so we can reorder the results later to the original order
    process_args.insert(1, list(range(process_args_len)))

    if process_args_static is not None:
        # extend the process_args with the process_args_static
        _extend_process_args_with_const_args(
            process_args=process_args,
            process_args_static=process_args_static,
            deepcopy_static_args=False,
        )

    if deepcopy_static_args is not None:
        _extend_process_args_with_const_args(
            process_args=process_args,
            process_args_static=deepcopy_static_args,
            deepcopy_static_args=True,
        )

    max_pools = _find_max_pools_for_multiprocessing(
        threads=threads, length_process_args=len(process_args[0])
    )

    # we are ordering the process_args this way so each item is the args for one function call
    # the wrapper function process_function_for_imap_with_args_unpacking will unpack the args
    # so we can pass the same args to built in map, imap_unordered, or submit
    process_args = list(zip(*process_args))

    return process_args, max_pools


def _get_multiprocess_results_with_tqdm(
    results: Iterable[Any],
    process_func: Callable[[Any, Any], Any],
    process_args: List[List[Any]],
    threads: bool,
) -> List[Any]:
    """
    This function creates a progress bar for the multiprocessing loop.
    :param results: iterable, the iterable of results from the process_function
    :param process_func: function, the function that processes the given process_args
    :param process_args: list, the list of arguments that are processed by the process_function
    :param threads: bool, if the loop is for threads else for processes
    :return: ProgressBar, the progress bar for the multiprocessing loop
    """
    results = tqdm(
        results,
        total=len(process_args),
        desc=f"Multi{'threading' if threads else 'processing'} {process_func.__name__}",
        unit=f" {'threads' if threads else 'processes'}",
    )
    results_list = list(results)
    # results list is a tuple of (order, result) so we need to sort it by order to get the original order
    results_list = sorted(results_list, key=lambda x: x[0])
    # now extract the results from the tuple
    results_list = [result[1] for result in results_list]

    return results_list


def _find_max_pools_for_multiprocessing(threads: bool, length_process_args: int) -> int:
    """
    This function finds the max_pools for multiprocessing.
    :param threads: bool, if the max_pools are for threads else for processes
    :param length_process_args: int, the length of the process_args
    :return: int, the max_pools for multiprocessing
    """
    if threads:
        logger.info("Using ThreadPoolExecutor for multithreading.")
        active_tasks = threading.active_count()
        max_tasks = int(os.cpu_count()) * 4
    else:
        logger.info("Using Pool for multiprocessing.")
        active_tasks = len(multiprocessing.active_children())
        max_tasks = int(os.cpu_count())

    available_tasks = max_tasks - active_tasks
    max_pools = min(max_tasks, available_tasks)
    max_pools = min(max_pools, length_process_args)
    max_pools = max(max_pools, 1)

    logger.info(
        f"Multi{'threading' if threads else 'processing'} with max_pools: {max_pools}"
    )

    return max_pools


def _extend_process_args_with_const_args(
    process_args: List[List[Any]],
    process_args_static: List[Any],
    deepcopy_static_args: bool = False,
) -> None:
    """
    This function extends the process_args with the process_const_args.
    :param process_args: list, the list of arguments that are processed by the process_function
    :param process_args_static: list, the list of constant arguments that are processed by the process_function
    :param deepcopy_static_args: bool, if the process_args_static should be deep-copied for each process
    :return: list, the extended list of arguments that are processed by the process_function
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
