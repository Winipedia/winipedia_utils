"""Tests for winipedia_utils.testing.create_tests module."""

import os
import sys
from importlib import import_module
from pathlib import Path
from types import ModuleType

from pytest_mock import MockFixture

from winipedia_utils.dev.testing import create_tests as create_tests_module
from winipedia_utils.dev.testing.create_tests import (
    create_test_module,
    create_test_package,
    create_tests,
    create_tests_base,
    create_tests_for_package,
    get_test_classes_content,
    get_test_functions_content,
    get_test_module_content,
)
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_create_tests(mocker: MockFixture) -> None:
    """Test func for create_tests."""
    # Mock the two main functions that create_tests calls to verify orchestration
    mock_create_tests_base = mocker.patch(
        make_obj_importpath(create_tests_module) + ".create_tests_base"
    )
    mock_create_tests_for_src_package = mocker.patch(
        make_obj_importpath(create_tests_module) + ".create_tests_for_package"
    )

    # Call the function
    create_tests()

    # Verify both functions were called exactly once
    base_count = mock_create_tests_base.call_count
    src_count = mock_create_tests_for_src_package.call_count

    assert_with_msg(
        base_count == 1,
        f"Expected create_tests_base called once, got {base_count}",
    )

    assert_with_msg(
        src_count == 1,
        f"Expected create_tests_for_src_package called once, got {src_count}",
    )


def test_create_tests_base(tmp_path: Path, mocker: MockFixture) -> None:
    """Test func for create_tests_base."""
    # Change to tmp directory for testing
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)

        # Mock only the external dependencies we can't easily test
        mock_copy_package = mocker.patch(
            make_obj_importpath(create_tests_module) + ".copy_package"
        )

        # Create tests directory first (since copy_package is mocked)
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Call the function
        create_tests_base()

        # Verify copy_package was called
        assert_with_msg(
            mock_copy_package.called,
            "Expected copy_package to be called",
        )

    finally:
        os.chdir(original_cwd)


def test_create_tests_for_package(mocker: MockFixture) -> None:
    """Test func for create_tests_for_src_package."""
    # Mock the dependencies
    mock_walk_package = mocker.patch(
        make_obj_importpath(create_tests_module) + ".walk_package"
    )
    mock_create_test_package = mocker.patch(
        make_obj_importpath(create_tests_module) + ".create_test_package"
    )
    mock_create_test_module = mocker.patch(
        make_obj_importpath(create_tests_module) + ".create_test_module"
    )

    # Create mock package and modules
    mock_package = mocker.MagicMock(spec=ModuleType)
    mock_module1 = mocker.MagicMock(spec=ModuleType)
    mock_module2 = mocker.MagicMock(spec=ModuleType)

    # Set up mock return values
    mock_walk_package.return_value = [(mock_package, [mock_module1, mock_module2])]

    # Call the function
    create_tests_for_package(package=mock_package)

    # Verify walk_package was called with the source package
    mock_walk_package.assert_called_once_with(mock_package)

    # Verify create_test_package was called for the package
    mock_create_test_package.assert_called_once_with(mock_package)

    # Verify create_test_module was called for each module
    expected_module_calls = 2
    actual_module_calls = mock_create_test_module.call_count
    assert_with_msg(
        actual_module_calls == expected_module_calls,
        f"Expected create_test_module called {expected_module_calls} times, "
        f"got {actual_module_calls}",
    )


def test_create_test_package(mocker: MockFixture) -> None:
    """Test func for create_test_package."""
    # Mock the dependencies
    mock_make_test_obj_importpath_from_obj = mocker.patch(
        make_obj_importpath(create_tests_module) + ".make_test_obj_importpath_from_obj"
    )
    mock_create_module = mocker.patch(
        make_obj_importpath(create_tests_module) + ".create_module"
    )

    # Create mock package
    mock_package = mocker.MagicMock(spec=ModuleType)

    # Set up mock return values
    test_package_name = "tests.test_package"
    mock_make_test_obj_importpath_from_obj.return_value = test_package_name

    # Call the function
    create_test_package(mock_package)

    # Verify make_test_obj_importpath_from_obj was called with the package
    mock_make_test_obj_importpath_from_obj.assert_called_once_with(mock_package)

    # Verify create_module was called with the test package name and is_package=True
    mock_create_module.assert_called_once_with(test_package_name, is_package=True)


def test_create_test_module(mocker: MockFixture) -> None:
    """Test func for create_test_module."""
    # Mock the dependencies
    mock_make_test_obj_importpath_from_obj = mocker.patch(
        make_obj_importpath(create_tests_module) + ".make_test_obj_importpath_from_obj"
    )
    mock_create_module = mocker.patch(
        make_obj_importpath(create_tests_module) + ".create_module"
    )
    mock_to_path = mocker.patch(make_obj_importpath(create_tests_module) + ".to_path")
    mock_get_test_module_content = mocker.patch(
        make_obj_importpath(create_tests_module) + ".get_test_module_content"
    )

    # Create mock module and path
    mock_module = mocker.MagicMock(spec=ModuleType)
    mock_test_module = mocker.MagicMock(spec=ModuleType)
    mock_path = mocker.MagicMock()

    # Set up mock return values
    test_module_name = "tests.test_module"
    test_content = "test module content"
    mock_make_test_obj_importpath_from_obj.return_value = test_module_name
    mock_create_module.return_value = mock_test_module
    mock_to_path.return_value = mock_path
    mock_get_test_module_content.return_value = test_content

    # Call the function
    create_test_module(mock_module)

    # Verify make_test_obj_importpath_from_obj was called
    mock_make_test_obj_importpath_from_obj.assert_called_once_with(mock_module)

    # Verify create_module was called with correct parameters
    mock_create_module.assert_called_once_with(test_module_name, is_package=False)

    # Verify to_path was called with the test module
    mock_to_path.assert_called_once_with(mock_test_module, is_package=False)

    # Verify get_test_module_content was called
    mock_get_test_module_content.assert_called_once_with(mock_module)

    # Verify the content was written to the path
    mock_path.write_text.assert_called_once_with(test_content)


def test_get_test_module_content(mocker: MockFixture) -> None:
    """Test func for get_test_module_content."""
    # Mock the dependencies
    mock_get_test_obj_from_obj = mocker.patch(
        make_obj_importpath(create_tests_module) + ".get_test_obj_from_obj"
    )
    mock_get_module_content_as_str = mocker.patch(
        make_obj_importpath(create_tests_module) + ".get_module_content_as_str"
    )
    mock_get_test_functions_content = mocker.patch(
        make_obj_importpath(create_tests_module) + ".get_test_functions_content"
    )
    mock_get_test_classes_content = mocker.patch(
        make_obj_importpath(create_tests_module) + ".get_test_classes_content"
    )

    # Create mock modules
    mock_module = mocker.MagicMock(spec=ModuleType)
    mock_test_module = mocker.MagicMock(spec=ModuleType)

    # Set up mock return values
    initial_content = "initial test module content"
    functions_content = "content with functions"
    final_content = "final content with classes"

    mock_get_test_obj_from_obj.return_value = mock_test_module
    mock_get_module_content_as_str.return_value = initial_content
    mock_get_test_functions_content.return_value = functions_content
    mock_get_test_classes_content.return_value = final_content

    # Call the function
    result = get_test_module_content(mock_module)

    # Verify the result
    assert_with_msg(
        result == final_content,
        f"Expected final content, got {result}",
    )

    # Verify all functions were called in the correct order
    mock_get_test_obj_from_obj.assert_called_once_with(mock_module)
    mock_get_module_content_as_str.assert_called_once_with(mock_test_module)
    mock_get_test_functions_content.assert_called_once_with(
        mock_module, mock_test_module, initial_content
    )
    mock_get_test_classes_content.assert_called_once_with(
        mock_module, mock_test_module, functions_content
    )


def test_get_test_functions_content(tmp_path: Path) -> None:
    """Test func for get_test_functions_content."""
    # Create a real source module with functions
    source_module_content = '''"""Test source module."""

def function_a() -> str:
    """First function."""
    return "a"

def function_b() -> int:
    """Second function."""
    return 42
'''

    # Create a test module with one existing test
    test_module_content = '''"""Test module."""

def test_function_a() -> None:
    """Test func for function_a."""
    pass
'''

    # Create the modules
    source_file = tmp_path / "source_module.py"
    test_file = tmp_path / "test_module.py"

    source_file.write_text(source_module_content)
    test_file.write_text(test_module_content)

    # Change to tmp_path directory and import the modules
    original_cwd = Path.cwd()
    original_path = sys.path[:]
    os.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))

    try:
        source_module = import_module("source_module")
        test_module = import_module("test_module")

        # Call the function
        initial_content = "# Initial content\n"
        result = get_test_functions_content(source_module, test_module, initial_content)

        # Verify the result contains the initial content
        assert_with_msg(
            initial_content in result,
            "Expected result to contain initial content",
        )

        # Verify the result contains new test function for function_b
        assert_with_msg(
            "def test_function_b() -> None:" in result,
            "Expected result to contain test_function_b",
        )

        # Verify the result contains the docstring
        assert_with_msg(
            "Test func for function_b" in result,
            "Expected result to contain docstring for function_b",
        )

        # Verify NotImplementedError is in the result
        assert_with_msg(
            "NotImplementedError" in result,
            "Expected result to contain NotImplementedError",
        )

        # Verify it doesn't duplicate existing test
        function_a_count = result.count("def test_function_a() -> None:")
        assert_with_msg(
            function_a_count == 0,
            f"Expected no new test_function_a, found {function_a_count} occurrences",
        )

    finally:
        # Clean up
        os.chdir(original_cwd)
        sys.path[:] = original_path
        if "source_module" in sys.modules:
            del sys.modules["source_module"]
        if "test_module" in sys.modules:
            del sys.modules["test_module"]


def test_get_test_classes_content(tmp_path: Path) -> None:
    """Test func for get_test_classes_content."""
    # Create a real source module with classes
    source_module_content = '''"""Test source module."""

class Calculator:
    """Calculator class."""

    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

class StringHelper:
    """String helper class."""

    def reverse(self, text: str) -> str:
        """Reverse a string."""
        return text[::-1]
'''

    # Create a test module with one existing test class
    test_module_content = '''"""Test module."""

class TestCalculator:
    """Test class for Calculator."""

    def test_add(self) -> None:
        """Test method for add."""
        pass
'''

    # Create the modules
    source_file = tmp_path / "source_module.py"
    test_file = tmp_path / "test_module.py"

    source_file.write_text(source_module_content)
    test_file.write_text(test_module_content)

    # Change to tmp_path directory and import the modules
    original_cwd = Path.cwd()
    original_path = sys.path[:]
    os.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))

    try:
        source_module = import_module("source_module")
        test_module = import_module("test_module")

        # Call the function
        initial_content = "# Initial content\n"
        result = get_test_classes_content(source_module, test_module, initial_content)

        # Verify the result contains the initial content
        assert_with_msg(
            initial_content in result,
            "Expected result to contain initial content",
        )

        # Verify the result contains new test class for StringHelper
        assert_with_msg(
            "class TestStringHelper:" in result,
            "Expected result to contain TestStringHelper",
        )

        # Verify the result contains test method for reverse
        assert_with_msg(
            "def test_reverse(self) -> None:" in result,
            "Expected result to contain test_reverse method",
        )

        # Verify the result contains missing test method for multiply
        assert_with_msg(
            "def test_multiply(self) -> None:" in result,
            "Expected result to contain test_multiply method",
        )

        # Verify docstrings are present
        assert_with_msg(
            "Test class for StringHelper" in result,
            "Expected result to contain StringHelper class docstring",
        )

        assert_with_msg(
            "Test method for reverse" in result,
            "Expected result to contain reverse method docstring",
        )

        # Verify NotImplementedError is in the result
        assert_with_msg(
            "NotImplementedError" in result,
            "Expected result to contain NotImplementedError",
        )

    finally:
        # Clean up
        os.chdir(original_cwd)
        sys.path[:] = original_path
        if "source_module" in sys.modules:
            del sys.modules["source_module"]
        if "test_module" in sys.modules:
            del sys.modules["test_module"]
