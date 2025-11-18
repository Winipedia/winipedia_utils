"""Metaclass utilities for class behavior modification and enforcement.

This module provides metaclasses that can be used to
modify class behavior at creation time.
These metaclasses can be used individually or combined to create classes
with enhanced capabilities and stricter implementation requirements.

"""

import logging
import time
from abc import ABCMeta
from collections.abc import Callable
from functools import wraps
from typing import Any

from pyrig.src.modules.function import is_func

from winiutils.src.data.structures.text.string import value_to_truncated_string

logger = logging.getLogger(__name__)


class ABCLoggingMeta(ABCMeta):
    """Metaclass that automatically adds logging to class methods.

    Wraps non-magic methods with a logging decorator that tracks method calls,
    arguments, execution time, and return values. Includes rate limiting to
    prevent log flooding.
    """

    def __new__(
        mcs: type["ABCLoggingMeta"],
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
    ) -> "ABCLoggingMeta":
        """Create a new class with logging-wrapped methods.

        Args:
            mcs: The metaclass instance
            name: The name of the class being created
            bases: The base classes of the class being created
            dct: The attribute dictionary of the class being created

        Returns:
            A new class with logging functionality added to its methods

        """
        # Wrap all callables of the class with a logging wrapper

        for attr_name, attr_value in dct.items():
            if mcs.is_loggable_method(attr_value):
                if isinstance(attr_value, classmethod):
                    wrapped_method = mcs.wrap_with_logging(
                        func=attr_value.__func__, class_name=name, call_times={}
                    )
                    dct[attr_name] = classmethod(wrapped_method)
                elif isinstance(attr_value, staticmethod):
                    wrapped_method = mcs.wrap_with_logging(
                        func=attr_value.__func__, class_name=name, call_times={}
                    )
                    dct[attr_name] = staticmethod(wrapped_method)
                else:
                    dct[attr_name] = mcs.wrap_with_logging(
                        func=attr_value, class_name=name, call_times={}
                    )

        return super().__new__(mcs, name, bases, dct)

    @staticmethod
    def is_loggable_method(method: Callable[..., Any]) -> bool:
        """Determine if a method should have logging applied.

        Args:
            method: The method to check, properties are not logged
                as they are not callable and it turns out to be tricky with them

        Returns:
            True if the method should be wrapped with logging, False otherwise

        """
        return (
            is_func(method)  # must be a method-like attribute
            and hasattr(method, "__name__")  # must have a name
            and not method.__name__.startswith("__")  # must not be a magic method
        )

    @staticmethod
    def wrap_with_logging(
        func: Callable[..., Any],
        class_name: str,
        call_times: dict[str, float],
    ) -> Callable[..., Any]:
        """Wrap a function with logging functionality.

        Creates a wrapper that logs method calls, arguments, execution time,
        and return values. Includes rate limiting to prevent excessive logging.

        Args:
            func: The function to wrap with logging
            class_name: The name of the class containing the function
            call_times: Dictionary to track when methods were last called

        Returns:
            A wrapped function with logging capabilities

        """
        time_time = time.time  # Cache the time.time function for performance

        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            # call_times as a dictionary to store the call times of the function
            # we only log if the time since the last call is greater than the threshold
            # this is to avoid spamming the logs

            func_name = func.__name__

            threshold = 1

            last_call_time = call_times.get(func_name, 0)

            current_time = time_time()

            do_logging = (current_time - last_call_time) > threshold

            max_log_length = 20

            if do_logging:
                args_str = value_to_truncated_string(
                    value=args, max_length=max_log_length
                )

                kwargs_str = value_to_truncated_string(
                    value=kwargs, max_length=max_log_length
                )

                logger.info(
                    "%s - Calling %s with %s and %s",
                    class_name,
                    func_name,
                    args_str,
                    kwargs_str,
                )

            # Execute the function and return the result

            result = func(*args, **kwargs)

            if do_logging:
                duration = time_time() - current_time

                result_str = value_to_truncated_string(
                    value=result, max_length=max_log_length
                )

                logger.info(
                    "%s - %s finished with %s seconds -> returning %s",
                    class_name,
                    func_name,
                    duration,
                    result_str,
                )

            # save the call time for the next call

            call_times[func_name] = current_time

            return result

        return wrapper
