"""Tests for winipedia_utils.projects.project module."""

from types import ModuleType

from pytest_mock import MockFixture

from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.projects.poetry.config import PyProjectTomlConfig
from winipedia_utils.projects.project import (
    create_project_root,
    make_name_from_package,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_create_project_root(mocker: MockFixture) -> None:
    """Test func for _create_project_root."""
    # Mock get_poetry_package_name
    mock_get_poetry_name = mocker.patch(
        make_obj_importpath(PyProjectTomlConfig.get_package_name),
        return_value="test_package",
    )

    # Mock create_module
    mock_create_module = mocker.patch("winipedia_utils.projects.project.create_module")

    # Call the function
    create_project_root()

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
