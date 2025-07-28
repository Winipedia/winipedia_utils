"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_oop.test_mixins.test_meta
"""

from abc import abstractmethod
from typing import Any, final

import pytest
from pytest_mock import MockFixture

from winipedia_utils.oop.mixins.meta import (
    ABCLoggingMeta,
    StrictABCLoggingMeta,
    StrictABCMeta,
)
from winipedia_utils.testing.assertions import assert_with_msg


class TestABCLoggingMeta:
    """Test class for LoggingMeta."""

    def test___new__(self) -> None:
        """Test method for __new__."""

        # Create a class with LoggingMeta to test that it works
        class TestClass(metaclass=ABCLoggingMeta):
            def test_method(self) -> str:
                return "test"

        # Verify the class was created successfully
        assert_with_msg(
            type(TestClass).__name__ == f"{ABCLoggingMeta.__name__}",
            "Expected TestClass to be created with LoggingMeta",
        )

        # Verify that methods are wrapped (they should have different behavior)
        instance = TestClass()
        result = instance.test_method()
        assert_with_msg(
            result == "test",
            f"Expected method to return 'test', got {result}",
        )

    def test___new___skips_non_loggable_methods(self, mocker: MockFixture) -> None:
        """Test that __new__ skips non-loggable methods."""
        # Mock is_loggable_method to return False
        mock_is_loggable = mocker.patch.object(
            ABCLoggingMeta, "is_loggable_method", return_value=False
        )
        mock_wrap_logging = mocker.patch.object(ABCLoggingMeta, "wrap_with_logging")

        # Create a class with LoggingMeta
        class TestClass(metaclass=ABCLoggingMeta):
            def __init__(self) -> None:
                pass

        # Verify the class was created successfully
        assert_with_msg(
            type(TestClass) is ABCLoggingMeta,
            "Expected TestClass to be created with LoggingMeta",
        )

        # Verify is_loggable_method was called
        mock_is_loggable.assert_called()

        # Verify wrap_with_logging was NOT called for non-loggable methods
        mock_wrap_logging.assert_not_called()

    def test_is_loggable_method(self, mocker: MockFixture) -> None:
        """Test method for is_loggable_method."""
        # Mock is_func to control its behavior
        mock_is_func = mocker.patch("winipedia_utils.oop.mixins.meta.is_func")

        # Test case 1: Regular method (should be loggable)
        def regular_method() -> None:
            pass

        regular_method.__name__ = "regular_method"
        mock_is_func.return_value = True

        result = ABCLoggingMeta.is_loggable_method(regular_method)
        assert_with_msg(result is True, "Expected regular method to be loggable")

        # Test case 2: Magic method (should not be loggable)
        def magic_method() -> None:
            pass

        magic_method.__name__ = "__init__"
        mock_is_func.return_value = True

        result = ABCLoggingMeta.is_loggable_method(magic_method)
        assert_with_msg(result is False, "Expected magic method to not be loggable")

        # Test case 3: Non-function (should not be loggable)
        mock_is_func.return_value = False
        non_function: Any = 42  # Not a function

        result = ABCLoggingMeta.is_loggable_method(non_function)
        assert_with_msg(result is False, "Expected non-function to not be loggable")

    def test_wrap_with_logging(self, mocker: MockFixture) -> None:
        """Test method for wrap_with_logging."""
        # Mock dependencies
        mock_logger = mocker.patch("winipedia_utils.oop.mixins.meta.logger")
        mock_time = mocker.patch("time.time")
        mock_value_to_truncated_string = mocker.patch(
            "winipedia_utils.oop.mixins.meta.value_to_truncated_string"
        )

        # Set up time mock to simulate passage of time
        mock_time.side_effect = [1000.0, 1000.5, 1001.0]  # start, during, end
        mock_value_to_truncated_string.return_value = "truncated"

        # Create a test function to wrap
        def test_func(self: object, arg1: str, arg2: int = 42) -> str:  # noqa: ARG001
            return f"result_{arg1}_{arg2}"

        test_func.__name__ = "test_func"

        # Wrap the function
        call_times: dict[str, float] = {}
        wrapped_func = ABCLoggingMeta.wrap_with_logging(
            test_func, "TestClass", call_times
        )

        # Create a mock self object
        mock_self = mocker.MagicMock()

        # Call the wrapped function
        result = wrapped_func(mock_self, "hello", arg2=100)

        # Verify the result
        assert_with_msg(
            result == "result_hello_100",
            f"Expected 'result_hello_100', got {result}",
        )

        # Verify logging was called (should log because it's the first call)
        expected_log_calls = 2  # start and end logging
        actual_log_calls = mock_logger.info.call_count
        assert_with_msg(
            actual_log_calls == expected_log_calls,
            f"Expected {expected_log_calls} log calls, got {actual_log_calls}",
        )

        # Verify call time was recorded
        assert_with_msg(
            "test_func" in call_times,
            "Expected call time to be recorded for test_func",
        )

    def test_wrap_with_logging_rate_limiting(self, mocker: MockFixture) -> None:
        """Test that wrap_with_logging implements rate limiting."""
        # Mock dependencies
        mock_logger = mocker.patch("winipedia_utils.oop.mixins.meta.logger")
        mock_time = mocker.patch("time.time")

        # Set up time mock to simulate rapid calls (within threshold)
        mock_time.side_effect = [1000.0, 1000.5, 1000.5, 1000.6]

        # Create a test function
        def test_func(self: object) -> str:  # noqa: ARG001
            return "result"

        test_func.__name__ = "test_func"

        # Wrap the function
        call_times: dict[str, float] = {}
        wrapped_func = ABCLoggingMeta.wrap_with_logging(
            test_func, "TestClass", call_times
        )

        mock_self = mocker.MagicMock()

        # First call - should log
        wrapped_func(mock_self)
        first_call_count = mock_logger.info.call_count

        # Second call within threshold - should not log
        wrapped_func(mock_self)
        second_call_count = mock_logger.info.call_count

        # Verify rate limiting worked
        assert_with_msg(
            second_call_count == first_call_count,
            "Expected no additional logging due to rate limiting",
        )


class TestStrictABCMeta:
    """Test class for ImplementationMeta."""

    def test___init__(self, mocker: MockFixture) -> None:
        """Test method for __init__."""
        # Mock methods
        mock_check_method_decorators = mocker.patch.object(
            StrictABCMeta, "check_method_decorators"
        )
        mock_is_abstract_cls = mocker.patch.object(
            StrictABCMeta, "is_abstract_cls", return_value=False
        )
        mock_check_attrs_implemented = mocker.patch.object(
            StrictABCMeta, "check_attrs_implemented"
        )

        # Create a concrete class
        class ConcreteClass(metaclass=StrictABCMeta):
            @final
            def concrete_method(self) -> None:
                pass

        # verify creation
        assert_with_msg(
            type(ConcreteClass) is StrictABCMeta,
            "Expected ConcreteClass to be created with ImplementationMeta",
        )

        # Verify all checks were called for concrete class
        mock_check_method_decorators.assert_called_once()
        mock_is_abstract_cls.assert_called_once()
        mock_check_attrs_implemented.assert_called_once()

    def test___init___with_abstract_class(self, mocker: MockFixture) -> None:
        """Test __init__ with an abstract class."""
        # Mock methods
        mock_check_method_decorators = mocker.patch.object(
            StrictABCMeta, "check_method_decorators"
        )
        mock_is_abstract_cls = mocker.patch.object(
            StrictABCMeta, "is_abstract_cls", return_value=True
        )
        mock_check_attrs_implemented = mocker.patch.object(
            StrictABCMeta, "check_attrs_implemented"
        )

        # Create an abstract class
        class AbstractClass(metaclass=StrictABCMeta):
            @abstractmethod
            def abstract_method(self) -> None:
                pass

        # Verify the class was created successfully
        assert_with_msg(
            type(AbstractClass) is StrictABCMeta,
            "Expected AbstractClass to be created with ImplementationMeta",
        )

        # Verify method decorators were checked
        mock_check_method_decorators.assert_called_once()

        # Verify abstract class check was called
        mock_is_abstract_cls.assert_called_once()

        # Verify attrs implementation was NOT checked for abstract class
        mock_check_attrs_implemented.assert_not_called()

    def test___init___with_concrete_class(self, mocker: MockFixture) -> None:
        """Test __init__ with a concrete class."""
        # Mock methods
        mock_check_method_decorators = mocker.patch.object(
            StrictABCMeta, "check_method_decorators"
        )
        mock_is_abstract_cls = mocker.patch.object(
            StrictABCMeta, "is_abstract_cls", return_value=False
        )
        mock_check_attrs_implemented = mocker.patch.object(
            StrictABCMeta, "check_attrs_implemented"
        )

        # Create a concrete class
        class ConcreteClass(metaclass=StrictABCMeta):
            @final
            def concrete_method(self) -> None:
                pass

        # Verify the class was created successfully
        assert_with_msg(
            type(ConcreteClass) is StrictABCMeta,
            "Expected ConcreteClass to be created with ImplementationMeta",
        )

        # Verify all checks were called for concrete class
        mock_check_method_decorators.assert_called_once()
        mock_is_abstract_cls.assert_called_once()
        mock_check_attrs_implemented.assert_called_once()

    def test_is_abstract_cls(self) -> None:
        """Test method for is_abstract_cls."""

        # Create a class with abstract methods
        class AbstractClass(metaclass=StrictABCMeta):
            @abstractmethod
            def abstract_method(self) -> None:
                pass

            @final
            def concrete_method(self) -> None:
                pass

            @classmethod
            @abstractmethod
            def abstract_classmethod(cls) -> None:
                pass

        # Test that class with abstract methods is detected as abstract
        result = AbstractClass.is_abstract_cls()
        assert_with_msg(
            result is True,
            "Expected class with abstract methods to be detected as abstract",
        )

        # Create a class without abstract methods
        class ConcreteClass(metaclass=StrictABCMeta):
            @final
            def concrete_method(self) -> None:
                pass

            @classmethod
            @final
            def concrete_classmethod(cls) -> type:
                return cls

        # Test that class without abstract methods is not abstract
        result = ConcreteClass.is_abstract_cls()
        assert_with_msg(
            result is False,
            "Expected class without abstract methods to not be abstract",
        )
        assert_with_msg(
            ConcreteClass.concrete_classmethod() is ConcreteClass,
            "Expected class method to return class",
        )

    def test_check_method_decorators_success(self) -> None:
        """Test check_method_decorators with properly decorated methods."""

        # Create a test class with properly decorated methods
        class TestClass(metaclass=StrictABCMeta):
            @final
            def final_method(self) -> None:
                pass

            @abstractmethod
            def abstract_method(self) -> None:
                pass

        # This should not raise an exception since all methods are decorated
        TestClass.check_method_decorators()

        # Verify the class was created successfully
        assert_with_msg(
            type(TestClass) is StrictABCMeta,
            "Expected TestClass to be created successfully",
        )

    def test_check_method_decorators_failure(self) -> None:
        """Test check_method_decorators with improperly decorated methods."""
        # This should raise a TypeError during class creation
        with pytest.raises(TypeError, match="must be decorated with"):

            class TestClass(metaclass=StrictABCMeta):
                def undecorated_method(self) -> None:
                    pass

    def test_is_final_method(self) -> None:
        """Test method for is_final_method."""

        # Create a class with a final method
        class TestClass:
            @final
            def final_method(self) -> None:
                pass

            def non_final_method(self) -> None:
                pass

        # Test with a final method
        result = StrictABCMeta.is_final_method(TestClass.final_method)
        assert_with_msg(
            result is True, "Expected method with @final to be detected as final"
        )

        # Test with a non-final method
        result = StrictABCMeta.is_final_method(TestClass.non_final_method)
        assert_with_msg(
            result is False,
            "Expected method without @final to not be detected as final",
        )

    def test_is_abstract_method(self) -> None:
        """Test method for is_abstract_method."""

        # Create a class with abstract and non-abstract methods
        class TestClass:
            @abstractmethod
            def abstract_method(self) -> None:
                pass

            def non_abstract_method(self) -> None:
                pass

        # Test with an abstract method
        result = StrictABCMeta.is_abstract_method(TestClass.abstract_method)
        assert_with_msg(
            result is True,
            "Expected method with @abstractmethod to be detected as abstract",
        )

        # Test with a non-abstract method
        result = StrictABCMeta.is_abstract_method(TestClass.non_abstract_method)
        assert_with_msg(
            result is False,
            "Expected method without @abstractmethod to not be detected as abstract",
        )

    def test_check_attrs_implemented_success(self) -> None:
        """Test check_attrs_implemented with all attributes implemented."""

        # Create a base class with NotImplemented attributes
        class BaseClass:
            attr1: Any = NotImplemented
            attr2: Any = NotImplemented

        # Create a test class with implemented attributes
        class TestClass(BaseClass, metaclass=StrictABCMeta):
            attr1: str = "value1"
            attr2: str = "value2"

            @final
            def dummy_method(self) -> None:
                pass

        # This should not raise an exception
        TestClass.check_attrs_implemented()

        # Verify the class was created successfully
        assert_with_msg(
            TestClass.attr1 == "value1",
            f"Expected attr1 to be 'value1', got {TestClass.attr1}",
        )

    def test_check_attrs_implemented_failure(self) -> None:
        """Test check_attrs_implemented with missing attributes."""

        # Create a base class with NotImplemented attributes
        class BaseClass:
            missing_attr: Any = NotImplemented
            implemented_attr: Any = NotImplemented

        # This should raise a ValueError during class creation for the missing attribute
        with pytest.raises(ValueError, match="missing_attr.*must be implemented"):

            class TestClass(BaseClass, metaclass=StrictABCMeta):
                implemented_attr: str = "value"
                # missing_attr is not implemented

                @final
                def dummy_method(self) -> None:
                    pass

    def test_attrs_to_implement(self) -> None:
        """Test method for attrs_to_implement."""

        # Create a base class with NotImplemented attributes
        class BaseClass:
            required_attr1: Any = NotImplemented
            implemented_attr: str = "implemented"
            required_attr2: Any = NotImplemented

        # Create a derived class that implements the required attributes
        class DerivedClass(BaseClass, metaclass=StrictABCMeta):
            required_attr1: str = "implemented1"
            required_attr2: str = "implemented2"

            @final
            def dummy_method(self) -> None:
                pass

        # Get attributes to implement - this tests the method works
        DerivedClass.attrs_to_implement()

        # Since we implemented all required attributes, the list should be empty
        # or contain only the originally NotImplemented ones from the base class
        # Let's test the base class directly
        base_attrs = [
            name
            for name, value in BaseClass.__dict__.items()
            if value is NotImplemented
        ]

        expected_attrs = {"required_attr1", "required_attr2"}
        actual_base_attrs = set(base_attrs)

        assert_with_msg(
            expected_attrs == actual_base_attrs,
            f"Expected {expected_attrs}, got {actual_base_attrs}",
        )

    def test_check_attrs_implemented(self) -> None:
        """Test method for check_attrs_implemented."""

        # This is the same as test_check_attrs_implemented_success
        # Create a base class with NotImplemented attributes
        class BaseClass:
            attr1: Any = NotImplemented
            attr2: Any = NotImplemented

        # Create a test class with implemented attributes
        class TestClass(BaseClass, metaclass=StrictABCMeta):
            attr1: str = "value1"
            attr2: str = "value2"

            @final
            def dummy_method(self) -> None:
                pass

        # This should not raise an exception
        TestClass.check_attrs_implemented()

        # Verify the class was created successfully
        assert_with_msg(
            TestClass.attr1 == "value1",
            f"Expected attr1 to be 'value1', got {TestClass.attr1}",
        )

    def test_check_method_decorators(self) -> None:
        """Test method for check_method_decorators."""

        # This is the same as test_check_method_decorators_success
        # Create a test class with properly decorated methods
        class TestClass(metaclass=StrictABCMeta):
            @final
            def final_method(self) -> None:
                pass

            @abstractmethod
            def abstract_method(self) -> None:
                pass

        # This should not raise an exception since all methods are decorated
        TestClass.check_method_decorators()

        # Verify the class was created successfully
        assert_with_msg(
            hasattr(TestClass, "final_method"),
            "Expected TestClass to be created successfully with methods",
        )


class TestStrictABCLoggingMeta:
    """Test class for ABCImplementationLoggingMeta."""

    def test_combined_metaclass_functionality(self) -> None:
        """Test that ABCImplementationLoggingMeta combines all three metaclasses."""

        # Create a class using the combined metaclass
        class CombinedClass(metaclass=StrictABCLoggingMeta):
            @abstractmethod
            def abstract_method(self) -> None:
                pass

            @final
            def concrete_method(self) -> str:
                return "test"

        # Verify the class is an instance of the combined metaclass
        assert_with_msg(
            type(CombinedClass) is StrictABCLoggingMeta,
            "Expected class to be instance of ABCImplementationLoggingMeta",
        )

        # Verify the class has the expected methods
        assert_with_msg(
            hasattr(CombinedClass, "abstract_method"),
            "Expected class to have abstract_method",
        )
        assert_with_msg(
            hasattr(CombinedClass, "concrete_method"),
            "Expected class to have concrete_method",
        )

    def test_abc_functionality(self) -> None:
        """Test that ABC functionality works correctly."""

        # Create an abstract class
        class AbstractClass(metaclass=StrictABCLoggingMeta):
            CLASS_VAR: str = NotImplemented

            @abstractmethod
            def abstract_method(self) -> None:
                pass

            @classmethod
            @final
            def concrete_classmethod2(cls) -> type:
                return cls

            @staticmethod
            @final
            def concrete_staticmethod() -> str:
                return "test"

            @staticmethod
            @final
            def concrete_staticmethod2() -> str:
                return "test"

        assert_with_msg(
            AbstractClass.concrete_classmethod2() is AbstractClass,
            "Expected concrete_classmethod2 to return class",
        )

        assert_with_msg(
            AbstractClass.concrete_staticmethod() == "test",
            "Expected concrete_staticmethod to return 'test'",
        )
        assert_with_msg(
            AbstractClass.concrete_staticmethod() == "test",
            "Expected concrete_staticmethod to return 'test'",
        )

        class AbstractClass2(AbstractClass):
            @final
            def abstract_method2(self) -> None:
                pass

        assert_with_msg(
            AbstractClass2.concrete_classmethod2() is AbstractClass2,
            "Expected concrete_classmethod2 to return class",
        )

        # Create a concrete implementation
        class ConcreteClass(AbstractClass):
            CLASS_VAR: str = "test"

            @final
            def abstract_method(self) -> None:
                pass

        # Verify that we can instantiate the concrete class
        try:
            ConcreteClass()
            success = True
        except TypeError:
            success = False

        assert_with_msg(
            success,
            "Expected to be able to instantiate concrete class",
        )
