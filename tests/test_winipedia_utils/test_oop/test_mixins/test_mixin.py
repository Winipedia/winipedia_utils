"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_oop.test_mixins.test_mixin
"""

from abc import abstractmethod
from typing import Any, final

import pytest
from pytest_mock import MockFixture

from winipedia_utils.oop.mixins.meta import StrictABCLoggingMeta
from winipedia_utils.oop.mixins.mixin import StrictABCLoggingMixin
from winipedia_utils.testing.assertions import assert_with_msg


class TestStrictABCLoggingMixin:
    """Test class for ABCImplementationLoggingMixin."""

    def test_mixin_metaclass(self) -> None:
        """Test that the mixin uses the correct metaclass."""
        # Verify that ABCImplementationLoggingMixin uses ABCImplementationLoggingMeta

        expected_msg = (
            "Expected ABCImplementationLoggingMixin to use ABCImplementationLoggingMeta"
        )
        assert_with_msg(
            type(StrictABCLoggingMixin) is StrictABCLoggingMeta,
            expected_msg,
        )

    def test_abstract_mixin_usage(self) -> None:
        """Test using the mixin as an abstract base class."""

        # Create an abstract class that inherits from the mixin
        class AbstractTestMixin(StrictABCLoggingMixin):
            @abstractmethod
            def abstract_method(self) -> str:
                """Abstract method that must be implemented."""

            @final
            def concrete_method(self) -> str:
                """Concrete method provided by the mixin."""
                return "concrete_result"

        # Verify the class has the expected methods
        assert_with_msg(
            hasattr(AbstractTestMixin, "abstract_method"),
            "Expected AbstractTestMixin to have abstract_method",
        )
        assert_with_msg(
            hasattr(AbstractTestMixin, "concrete_method"),
            "Expected AbstractTestMixin to have concrete_method",
        )

    def test_concrete_mixin_implementation(self) -> None:
        """Test creating a concrete implementation using the mixin."""
        # Constants for test values
        test_input_value = 5
        expected_doubled_value = 10

        # Create a concrete class that implements all abstract methods
        class ConcreteTestMixin(StrictABCLoggingMixin):
            @final
            def test_method(self) -> str:
                """Test method implementation."""
                return "test_result"

            @final
            def another_method(self, value: int) -> int:
                """Another test method with parameters."""
                return value * 2

        # Create instance and test method calls
        instance = ConcreteTestMixin()

        result = instance.test_method()
        assert_with_msg(
            result == "test_result",
            f"Expected 'test_result', got {result}",
        )

        result2 = instance.another_method(test_input_value)
        assert_with_msg(
            result2 == expected_doubled_value,
            f"Expected {expected_doubled_value}, got {result2}",
        )

    def test_mixin_with_abstract_and_concrete_methods(self) -> None:
        """Test mixin with both abstract and concrete methods."""

        # Create an abstract mixin with both types of methods
        class MixedTestMixin(StrictABCLoggingMixin):
            @abstractmethod
            def required_method(self) -> str:
                """Return required method result."""

            @final
            def utility_method(self) -> str:
                """Return utility result."""
                return "utility_result"

        # Create a concrete implementation
        class ConcreteMixed(MixedTestMixin):
            @final
            def required_method(self) -> str:
                """Implement the required method."""
                return "implemented"

        # Test the concrete implementation
        instance = ConcreteMixed()

        # Test the implemented abstract method
        result = instance.required_method()
        assert_with_msg(
            result == "implemented",
            f"Expected 'implemented', got {result}",
        )

        # Test the inherited concrete method
        result2 = instance.utility_method()
        assert_with_msg(
            result2 == "utility_result",
            f"Expected 'utility_result', got {result2}",
        )

    def test_mixin_with_attributes(self) -> None:
        """Test mixin with NotImplemented attributes."""

        # Create a base class with required attributes (not using the mixin directly)
        class AttributeBase:
            required_attr: Any = NotImplemented
            optional_attr: str = "default_value"

        # Create a mixin that inherits from the base and provides methods
        class AttributeTestMixin(AttributeBase, StrictABCLoggingMixin):
            @abstractmethod
            def abstract_placeholder(self) -> None:
                """Make this class abstract to avoid attribute checking."""

            @final
            def get_required_attr(self) -> Any:
                """Get the required attribute value."""
                return self.required_attr

            @final
            def get_optional_attr(self) -> str:
                """Get the optional attribute value."""
                return self.optional_attr

        # Create a concrete implementation that provides the required attribute
        class ConcreteAttribute(AttributeTestMixin):
            required_attr: str = "implemented_value"

            @final
            def abstract_placeholder(self) -> None:
                """Implement the abstract placeholder."""

        # Test the concrete implementation
        instance = ConcreteAttribute()

        result = instance.get_required_attr()
        assert_with_msg(
            result == "implemented_value",
            f"Expected 'implemented_value', got {result}",
        )

        result2 = instance.get_optional_attr()
        assert_with_msg(
            result2 == "default_value",
            f"Expected 'default_value', got {result2}",
        )

    def test_mixin_attribute_implementation_failure(self) -> None:
        """Test that missing required attributes cause errors."""

        # Create a base class with required attributes
        class FailureBase:
            required_attr: Any = NotImplemented

        # Create a mixin that inherits from the base
        class FailureTestMixin(FailureBase, StrictABCLoggingMixin):
            @abstractmethod
            def abstract_placeholder(self) -> None:
                """Make this class abstract to avoid attribute checking."""

            @final
            def dummy_method(self) -> None:
                """Satisfy method decorator requirements."""

        # Attempt to create a concrete class without implementing required attributes
        with pytest.raises(ValueError, match=r"required_attr.*must be implemented"):
            # Missing required_attr implementation
            class FailingConcrete(FailureTestMixin):
                @final
                def abstract_placeholder(self) -> None:
                    """Implement the abstract placeholder."""

    def test_mixin_method_decorator_enforcement(self) -> None:
        """Test that method decorator enforcement works with the mixin."""
        # This should fail because methods must be decorated
        # with @final or @abstractmethod
        with pytest.raises(TypeError, match="must be decorated with"):

            class BadMixin(StrictABCLoggingMixin):
                def undecorated_method(self) -> None:
                    """Lack proper decoration."""

    def test_mixin_logging_functionality(self, mocker: MockFixture) -> None:
        """Test that the mixin provides logging functionality."""
        # Constants
        expected_log_calls = 2

        # Mock the logger to capture logging calls
        mock_logger = mocker.patch("winipedia_utils.oop.mixins.meta.logger")
        mock_time = mocker.patch("time.time")
        mock_value_to_truncated_string = mocker.patch(
            "winipedia_utils.oop.mixins.meta.value_to_truncated_string"
        )

        # Set up mocks
        mock_time.side_effect = [1000.0, 1000.5, 1001.0]
        mock_value_to_truncated_string.return_value = "truncated"

        # Create a test mixin with logging
        class LoggingTestMixin(StrictABCLoggingMixin):
            @final
            def logged_method(self, arg: str) -> str:
                """Return result with logging."""
                return f"result_{arg}"

        # Create instance and call method
        instance = LoggingTestMixin()
        result = instance.logged_method("test")

        # Verify the result
        assert_with_msg(
            result == "result_test",
            f"Expected 'result_test', got {result}",
        )

        # Verify logging was called
        assert_with_msg(
            mock_logger.info.call_count >= expected_log_calls,
            "Expected logging to be called for method entry and exit",
        )

    def test_mixin_inheritance_chain(self) -> None:
        """Test complex inheritance chains with the mixin."""

        # Create a base mixin
        class BaseMixin(StrictABCLoggingMixin):
            @abstractmethod
            def base_method(self) -> str:
                """Return base method result."""

            @final
            def base_utility(self) -> str:
                """Return base utility result."""
                return "base_utility"

        # Create an intermediate mixin
        class IntermediateMixin(BaseMixin):
            @abstractmethod
            def intermediate_method(self) -> str:
                """Intermediate abstract method."""

            @final
            def intermediate_utility(self) -> str:
                """Intermediate utility method."""
                return "intermediate_utility"

        # Create a concrete implementation
        class ConcreteImplementation(IntermediateMixin):
            @final
            def base_method(self) -> str:
                """Implement base method."""
                return "base_implemented"

            @final
            def intermediate_method(self) -> str:
                """Implement intermediate method."""
                return "intermediate_implemented"

        # Test the concrete implementation
        instance = ConcreteImplementation()

        # Test all methods work
        assert_with_msg(
            instance.base_method() == "base_implemented",
            "Expected base_method to work",
        )
        assert_with_msg(
            instance.intermediate_method() == "intermediate_implemented",
            "Expected intermediate_method to work",
        )
        assert_with_msg(
            instance.base_utility() == "base_utility",
            "Expected base_utility to work",
        )
        assert_with_msg(
            instance.intermediate_utility() == "intermediate_utility",
            "Expected intermediate_utility to work",
        )

    def test_mixin_multiple_inheritance(self) -> None:
        """Test multiple inheritance with the mixin."""

        # Create a mixin
        class TestMixin(StrictABCLoggingMixin):
            @final
            def mixin_method(self) -> str:
                """Return mixin result."""
                return "mixin"

        # Create a class that inherits from the mixin and adds its own methods
        class MultipleInheritance(TestMixin):
            @final
            def regular_method(self) -> str:
                """Return regular result."""
                return "regular"

            @final
            def combined_method(self) -> str:
                """Combine both method results."""
                return f"{self.regular_method()}_{self.mixin_method()}"

        # Test the multiple inheritance
        instance = MultipleInheritance()

        assert_with_msg(
            instance.regular_method() == "regular",
            "Expected regular_method to work",
        )
        assert_with_msg(
            instance.mixin_method() == "mixin",
            "Expected mixin_method to work",
        )
        assert_with_msg(
            instance.combined_method() == "regular_mixin",
            "Expected combined_method to work",
        )


class TestABCLoggingMixin:
    """Test class for ABCLoggingMixin."""
