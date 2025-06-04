"""Tests for winipedia_utils.projects.project module."""

from pathlib import Path
from types import ModuleType

from pytest_mock import MockFixture

from winipedia_utils.projects.project import (
    _create_project_root,
    _create_py_typed,
    make_name_from_package,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test__create_project_root(mocker: MockFixture) -> None:
    """Test func for _create_project_root."""
    # Mock get_poetry_package_name
    mock_get_poetry_name = mocker.patch(
        "winipedia_utils.projects.project.get_poetry_package_name",
        return_value="test_package",
    )

    # Mock create_module
    mock_create_module = mocker.patch("winipedia_utils.projects.project.create_module")

    # Mock _create_py_typed
    mock_create_py_typed = mocker.patch(
        "winipedia_utils.projects.project._create_py_typed"
    )

    # Call the function
    _create_project_root()

    # Verify get_poetry_package_name was called
    assert_with_msg(
        mock_get_poetry_name.call_count == 1,
        "Expected get_poetry_package_name to be called once",
    )

    # Verify create_module was called with correct arguments
    assert_with_msg(
        mock_create_module.call_count == 1, "Expected create_module to be called once"
    )
    mock_create_module.assert_called_with("test_package", is_package=True)

    # Verify _create_py_typed was called
    assert_with_msg(
        mock_create_py_typed.call_count == 1,
        "Expected _create_py_typed to be called once",
    )


def test__create_py_typed(mocker: MockFixture) -> None:
    """Test func for _create_py_typed."""
    # Create mock source package
    mock_src_package = ModuleType("winipedia_utils")
    mock_src_package.__name__ = "winipedia_utils"

    # Mock get_src_package
    mock_get_src_package = mocker.patch(
        "winipedia_utils.projects.project.get_src_package",
        return_value=mock_src_package,
    )

    # Create a mock Path object that we can control
    mock_py_typed_path = mocker.MagicMock()
    mock_package_path = mocker.MagicMock(spec=Path)
    mock_package_path.__truediv__.return_value = mock_py_typed_path

    # Mock to_path
    mock_to_path = mocker.patch(
        "winipedia_utils.projects.project.to_path", return_value=mock_package_path
    )

    # Call the function
    _create_py_typed()

    # Verify get_src_package was called
    assert_with_msg(
        mock_get_src_package.call_count == 1,
        "Expected get_src_package to be called once",
    )

    # Verify to_path was called with correct arguments
    assert_with_msg(mock_to_path.call_count == 1, "Expected to_path to be called once")
    mock_to_path.assert_called_with("winipedia_utils", is_package=True)

    # Verify the path division was called to create py.typed path
    assert_with_msg(
        mock_package_path.__truediv__.call_count == 1,
        "Expected path division to be called once for py.typed",
    )
    mock_package_path.__truediv__.assert_called_with("py.typed")

    # Verify touch was called on the py.typed file
    assert_with_msg(
        mock_py_typed_path.touch.call_count == 1,
        "Expected touch to be called once on py.typed file",
    )


def test_make_name_from_package() -> None:
    """Test func for make_project_name."""
    # Create mock source package
    mock_src_package = ModuleType("winipedia_utils")
    mock_src_package.__name__ = "winipedia_utils"

    result = make_name_from_package(mock_src_package)
    expected = "Winipedia-Utils"
    assert_with_msg(
        result == expected,
        f"Expected '{expected}', got '{result}'",
    )

    result = make_name_from_package(mock_src_package, split_on="-", join_on="_")
    expected = "Winipedia_utils"
    assert_with_msg(
        result == expected,
        f"Expected '{expected}', got '{result}'",
    )
    result = make_name_from_package(mock_src_package, capitalize=False)
    expected = "winipedia-utils"
    assert_with_msg(
        result == expected,
        f"Expected '{expected}', got '{result}'",
    )

    result = make_name_from_package(
        mock_src_package, split_on="-", join_on="_", capitalize=False
    )
    expected = "winipedia_utils"
    assert_with_msg(
        result == expected,
        f"Expected '{expected}', got '{result}'",
    )
