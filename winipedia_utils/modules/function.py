"""Function utilities for introspection and manipulation.

This module provides utility functions for working with Python functions,
including extracting functions from modules and manipulating function objects.
These utilities are particularly useful for reflection, testing, and
dynamic code generation.
"""

import inspect
from collections.abc import Callable
from types import ModuleType
from typing import Any


def get_all_functions_from_module(module: ModuleType) -> list[Callable[..., Any]]:
    """Get all functions defined in a module.

    Retrieves all function objects that are defined directly in the specified module,
    excluding imported functions.

    Args:
        module: The module to extract functions from

    Returns:
        A list of callable functions defined in the module
    """
    return [
        func
        for _name, func in inspect.getmembers(module, inspect.isfunction)
        if func.__module__ == module.__name__
    ]
