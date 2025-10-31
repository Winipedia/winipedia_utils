"""Tests for winipedia_utils.projects.poetry.poetry module."""

from types import ModuleType

from pytest_mock import MockFixture

from winipedia_utils.projects.poetry.poetry import (
    VersionConstraint,
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


class TestVersionConstraint:
    """Test class for VersionConstraint."""

    def test___init__(self) -> None:
        """Test method for __init__."""
        constraint = ">=3.8, <3.12"
        version_constraint = VersionConstraint(constraint)
        assert_with_msg(
            version_constraint.constraint == constraint,
            f"Expected {constraint}, got {version_constraint.constraint}",
        )

    def test_get_lower_inclusive(self) -> None:
        """Test method for get_lower_inclusive."""
        constraint = ">=3.8, <3.12"
        version_constraint = VersionConstraint(constraint)
        lower = version_constraint.get_lower_inclusive()
        expected = "3.8"
        assert_with_msg(
            str(lower) == expected,
            f"Expected {expected}, got {lower}",
        )

        constraint = ">3.8, <3.12"
        version_constraint = VersionConstraint(constraint)
        lower = version_constraint.get_lower_inclusive()
        expected = "3.8.1"
        assert_with_msg(
            str(lower) == expected,
            f"Expected {expected}, got {lower}",
        )

        constraint = "<3.12"
        version_constraint = VersionConstraint(constraint)
        lower = version_constraint.get_lower_inclusive()
        assert_with_msg(
            lower is None,
            f"Expected None, got {lower}",
        )
        lower = version_constraint.get_lower_inclusive("3.8")
        expected = "3.8"
        assert_with_msg(
            str(lower) == expected,
            f"Expected {expected}, got {lower}",
        )

    def test_get_upper_exclusive(self) -> None:
        """Test method for get_upper_exclusive."""
        constraint = ">=3.8, <3.12"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_exclusive()
        expected = "3.12"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )
        constraint = ">=3.8, <=3.12"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_exclusive()
        expected = "3.12.1"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )

        constraint = ">=3.8"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_exclusive()
        assert_with_msg(
            upper is None,
            f"Expected None, got {upper}",
        )
        upper = version_constraint.get_upper_exclusive("3.12")
        expected = "3.12"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )

    def test_get_upper_inclusive(self) -> None:
        """Test method for get_upper_inclusive."""
        constraint = ">=3.8, <3.12"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_inclusive()
        expected = "3.11"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )
        constraint = ">=3.8, <=3.12"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_inclusive()
        expected = "3.12.0"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )
        constraint = ">=3.8, <3.12.1"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_inclusive()
        expected = "3.12.0"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )

        constraint = ">=3.8"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_inclusive()
        assert_with_msg(
            upper is None,
            f"Expected None, got {upper}",
        )

        constraint = ">=2.8, <3.12.0"
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_inclusive()
        expected = "3.11"
        assert_with_msg(
            str(upper) == expected,
            f"Expected {expected}, got {upper}",
        )

    def test_get_version_range(self) -> None:
        """Test method for get_version_range."""
        constraint = ">=3.8, <3.12"
        version_constraint = VersionConstraint(constraint)
        versions = version_constraint.get_version_range(level="major")
        expected = ["3"]
        actual = [str(v) for v in versions]
        assert_with_msg(
            actual == expected,
            f"Expected {expected}, got {actual}",
        )
        versions = version_constraint.get_version_range(level="minor")
        expected = ["3.8", "3.9", "3.10", "3.11"]
        actual = [str(v) for v in versions]
        assert_with_msg(
            actual == expected,
            f"Expected {expected}, got {actual}",
        )
        constraint = ">=3.8.2, <3.9.6"
        version_constraint = VersionConstraint(constraint)
        versions = version_constraint.get_version_range(level="micro")
        expected = [
            "3.8.2",
            "3.8.3",
            "3.8.4",
            "3.8.5",
            "3.9.2",
            "3.9.3",
            "3.9.4",
            "3.9.5",
        ]
        actual = [str(v) for v in versions]
        assert_with_msg(
            actual == expected,
            f"Expected {expected}, got {actual}",
        )
