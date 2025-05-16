"""Class utilities for introspection and manipulation.

This module provides utility functions for working with Python classes,
including extracting methods from classes and finding classes within modules.
These utilities are particularly useful for reflection, testing, and dynamic code generation.
"""

import inspect
from collections.abc import Callable
from types import ModuleType
from typing import Any


def is_func_or_method(obj: Callable[..., Any]) -> bool:
    """Return True if *obj* is a function or method.

    This function checks if the given object is a function or method,
    including those defined in a class body.

    Args:
        obj: The object to check

    Returns:
        bool: True if the object is a function or method, False otherwise
    """
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def is_func(obj: Callable[..., Any]) -> bool:
    """Return True if *obj* is a 'method-like' attribute as it appears in a class body.

    Accepts:


        • plain functions (instance methods)
        • staticmethod / classmethod descriptors
        • property descriptors (getter counts as method)
        • decorated functions that keep a __wrapped__ chain

    Returns:
        bool: True if the object is a method-like attribute, False otherwise
    """
    # plain function

    if is_func_or_method(obj):
        return True

    # common descriptors

    if isinstance(obj, (staticmethod, classmethod, property)):
        return True

    # unwrap any wrappers (@functools.wraps) and retest

    unwrapped = inspect.unwrap(obj)

    return is_func_or_method(unwrapped)


def get_all_methods_from_cls(
    class_: type, *, exclude_parent_methods: bool = False
) -> list[Callable[..., Any]]:
    """Get all methods from a class.

    Retrieves all methods (functions or methods) from a class. Can optionally
    exclude methods inherited from parent classes.

    Args:
        class_: The class to extract methods from
        exclude_parent_methods: If True, only include methods defined in this class,
        excluding those inherited from parent classes
    Returns:
        A list of callable methods from the class
    """
    methods = [(method, name) for name, method in inspect.getmembers(class_) if is_func(method)]

    if exclude_parent_methods:
        methods = [
            (method, name)
            for method, name in methods
            if method.__module__ == class_.__module__ and name in class_.__dict__
        ]

    return [method for method, _name in methods]


def get_all_cls_from_module(module: ModuleType) -> list[type]:
    """Get all classes defined in a module.

    Retrieves all class objects that are defined directly in the specified module,
    excluding imported classes.

    Args:
        module: The module to extract classes from

    Returns:
        A list of class types defined in the module
    """
    return [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if obj.__module__ == module.__name__
    ]
