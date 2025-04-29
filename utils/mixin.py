import time
from abc import ABCMeta
from functools import wraps
from inspect import isfunction
from typing import Dict, get_origin, List
from utils.string import value_to_truncated_string

from utils.logging.logger import get_logger


logger = get_logger(__name__)


class LoggingMeta(type):
    def __new__(mcs, name, bases, dct):
        # Wrap all callables of the class with a logging wrapper
        for attr_name, attr_value in dct.items():
            if mcs._is_loggable_method(attr_value):
                dct[attr_name] = mcs._wrap_with_logging(
                    func=attr_value, class_name=name, call_times={}
                )
        return super().__new__(mcs, name, bases, dct)

    @staticmethod
    def _is_loggable_method(method):
        return (
            callable(method)  # must be callable method
            and isfunction(method)  # must be a function
            and not method.__name__.startswith("__")  # must not be a magic method
        )

    @staticmethod
    def _wrap_with_logging(
        func: callable, class_name: str, call_times: Dict[str, float]
    ):
        """Wrap a function with logging functionality."""

        time_time = time.time  # Cache the time.time function for performance

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # we use the call times as a dictionary to store the call times of the function
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
                    f"{class_name=} - Calling {func_name=} with {args_str=} and {kwargs_str=}"
                )

            # Execute the function and return the result
            result = func(self, *args, **kwargs)

            if do_logging:
                duration = time_time() - current_time
                result_str = value_to_truncated_string(
                    value=result, max_length=max_log_length
                )
                logger.info(
                    f"{class_name=} - {func_name=} finished with {duration:.4f} seconds -> returning {result_str=}"
                )

            # save the call time for the next call
            call_times[func_name] = current_time

            return result

        return wrapper


class ImplementationMeta(type):
    __abstract__: bool = NotImplemented

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        if "__abstract__" not in dct:
            raise NotImplementedError(
                f"Class {cls.__name__} must define __abstract__ attribute to indicate if it is abstract or not."
            )

        if cls.__abstract__:
            return

        cls._check_attrs_implemented()

    def _check_attrs_implemented(cls):
        for attr in cls.attrs_to_implement():
            value = getattr(cls, attr, NotImplemented)
            if value is NotImplemented:
                raise ValueError(f"{attr=} must be implemented.")

        cls._check_implemented_attrs_types()

    def _get_implementation_type_hints(cls) -> Dict:
        type_hints = {
            k: eval(v) if isinstance(v, str) else v
            for base_class in cls.__mro__
            for k, v in getattr(base_class, "__annotations__", {}).items()
            if k in cls.attrs_to_implement()
        }
        return type_hints

    def _check_implemented_attrs_types(cls):
        implementation_type_hints = cls._get_implementation_type_hints()
        for attr, expected_type in implementation_type_hints.items():
            value = getattr(cls, attr, None)
            value_class = value if isinstance(value, type) else type(value)
            expected_type = get_origin(expected_type) or expected_type
            if not issubclass(value_class, expected_type):
                raise ValueError(
                    f"{attr=} must have type {expected_type}, got {value_class}"
                )

    # no underscore to make it public
    def attrs_to_implement(cls) -> List[str]:
        return cls._find_all_attrs_in_parent_classes_not_implemented()

    def _find_all_attrs_in_parent_classes_not_implemented(cls) -> List[str]:
        attrs = {
            attr
            for base_class in cls.__mro__
            for attr in dir(base_class)
            if getattr(base_class, attr, None) is NotImplemented
        }
        return list(attrs)


class ABCImplementationLoggingMeta(ImplementationMeta, LoggingMeta, ABCMeta):
    pass


class ABCImplementationLoggingMixin(metaclass=ABCImplementationLoggingMeta):
    __abstract__ = True
