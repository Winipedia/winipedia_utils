"""Tests for winipedia_utils.projects.poetry.poetry module."""

from types import ModuleType

from pytest_mock import MockFixture

from winipedia_utils.projects.poetry.poetry import (
    get_poetry_run_module_script,
    get_python_module_script,
    get_run_python_module_args,
    get_script_from_args,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_script_from_args() -> None:
    """Test func for get_script_from_args."""
    # Test with simple args
    result = get_script_from_args(["poetry", "run", "pytest"])
    assert_with_msg(
        result == "poetry run pytest",
        f"Expected 'poetry run pytest', got '{result}'",
    )

    # Test with single arg
    result = get_script_from_args(["python"])
    assert_with_msg(
        result == "python",
        f"Expected 'python', got '{result}'",
    )

    # Test with empty args
    result = get_script_from_args([])
    assert_with_msg(
        result == "",
        f"Expected empty string, got '{result}'",
    )


def test_get_run_python_module_args(mocker: MockFixture) -> None:
    """Test func for get_run_python_module_args."""
    # Create a mock module
    mock_module = mocker.MagicMock(spec=ModuleType)
    mock_module.__name__ = "test_module"

    result = get_run_python_module_args(mock_module)
    assert_with_msg(
        result == ["python", "-m", "test_module"],
        f"Expected ['python', '-m', 'test_module'], got {result}",
    )


def test_get_python_module_script(mocker: MockFixture) -> None:
    """Test func for get_run_python_module_script."""
    # Create a mock module
    mock_module = mocker.MagicMock(spec=ModuleType)
    mock_module.__name__ = "my_module"

    result = get_python_module_script(mock_module)
    assert_with_msg(
        result == "python -m my_module",
        f"Expected 'python -m my_module', got '{result}'",
    )


def test_get_poetry_run_module_script(mocker: MockFixture) -> None:
    """Test func for get_poetry_run_module_script."""
    # Create a mock module
    mock_module = mocker.MagicMock(spec=ModuleType)
    mock_module.__name__ = "app_module"

    result = get_poetry_run_module_script(mock_module)
    assert_with_msg(
        result == "poetry run python -m app_module",
        f"Expected 'poetry run python -m app_module', got '{result}'",
    )
