"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_modules.test_class_
"""

from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar

from winipedia_utils.modules.class_ import (
    get_all_cls_from_module,
    get_all_methods_from_cls,
)
from winipedia_utils.testing.assertions import assert_with_msg


def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorate a function for testing purposes."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Execute the wrapped function."""
        return func(*args, **kwargs)

    return wrapper


# Test classes for get_all_methods_from_cls
class ParentClass:
    """Parent class for testing inheritance."""

    class_var: ClassVar[str] = "parent_class_var"

    def parent_method(self) -> str:
        """Parent method."""
        return "parent_method"

    @staticmethod
    def parent_static_method() -> str:
        """Parent static method."""
        return "parent_static_method"

    @classmethod
    def parent_class_method(cls) -> str:
        """Parent class method."""
        return "parent_class_method"

    @property
    def parent_property(self) -> str:
        """Parent property."""
        return "parent_property"


class TestClass(ParentClass):
    """Test class for method extraction."""

    class_var: ClassVar[str] = "test_class_var"

    def instance_method(self) -> str:
        """Instance method."""
        return "instance_method"

    @staticmethod
    def static_method() -> str:
        """Return a static method value."""
        return "static_method"

    @classmethod
    def class_method(cls) -> str:
        """Class method."""
        return "class_method"

    @property
    def prop(self) -> str:
        """Property method."""
        return "property"

    def _private_method(self) -> str:
        """Private method."""
        return "private_method"

    @decorator
    def decorated_method(self) -> str:
        """Decorate with @decorator."""
        return "decorated_method"


class DecoratedClass:
    """Class with decorated methods for testing."""

    @decorator
    def decorated_method(self) -> str:
        """Return a decorated method value."""
        return "decorated_method"


def test_get_all_methods_from_cls() -> None:
    """Test func for get_all_methods_from_cls."""
    # Test case 1: Get all methods excluding inherited methods
    methods = get_all_methods_from_cls(TestClass, exclude_parent_methods=True)

    # expected methods in order of definition
    expected_methods = [
        TestClass.instance_method,
        TestClass.static_method,
        TestClass.class_method,
        TestClass.prop,
        TestClass._private_method,  # noqa: SLF001
        TestClass.decorated_method,
    ]
    assert_with_msg(
        methods == expected_methods,
        f"Expected methods {expected_methods}, got {methods}",
    )

    # Test case 2: Get all methods including inherited methods
    methods = get_all_methods_from_cls(TestClass, exclude_parent_methods=False)

    # expected methods in order of definition
    expected_methods = [
        ParentClass.parent_method,
        ParentClass.parent_static_method,
        TestClass.parent_class_method,  # bound by accessed class
        ParentClass.parent_property,
        TestClass.instance_method,
        TestClass.static_method,
        TestClass.class_method,
        TestClass.prop,
        TestClass._private_method,  # noqa: SLF001
        TestClass.decorated_method,
    ]
    assert_with_msg(
        methods == expected_methods,
        f"Expected methods {expected_methods}, got {methods}",
    )


def test_get_all_cls_from_module() -> None:
    """Test func for get_all_cls_from_module."""
    # use this file as the module
    module = test_get_all_cls_from_module.__module__

    classes = get_all_cls_from_module(module)

    # expected classes in order of definition
    expected_classes = [ParentClass, TestClass, DecoratedClass]
    assert_with_msg(
        classes == expected_classes,
        f"Expected classes {expected_classes}, got {classes}",
    )
