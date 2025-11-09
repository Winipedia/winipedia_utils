"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_hooks
"""

from winipedia_utils.dev.git.pre_commit.hooks import (
    add_updates_to_git,
    check_package_manager_configs,
    check_security,
    check_static_types,
    create_missing_tests,
    format_code,
    lint_code,
    run_tests,
)
from winipedia_utils.dev.projects.poetry.poetry import (
    POETRY_ARG,
)
from winipedia_utils.dev.testing import create_tests
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_check_package_manager_configs() -> None:
    """Test func for check_package_manager_configs."""
    # Call the function
    result = check_package_manager_configs()

    # Expected result
    expected = [POETRY_ARG, "check", "--strict"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_create_missing_tests() -> None:
    """Test func for create_tests."""
    # Call the function
    result = create_missing_tests()

    expected = ["poetry", "run", "python", "-m", f"{make_obj_importpath(create_tests)}"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_lint_code() -> None:
    """Test func for lint_code."""
    # Call the function
    result = lint_code()

    # Expected result
    expected = ["ruff", "check", "--fix"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_format_code() -> None:
    """Test func for format_code."""
    # Call the function
    result = format_code()

    # Expected result
    expected = ["ruff", "format"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_check_static_types() -> None:
    """Test func for check_static_types."""
    # Call the function
    result = check_static_types()

    # Expected result
    expected = ["mypy", "--exclude-gitignore"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_check_security() -> None:
    """Test func for check_security."""
    # Call the function
    result = check_security()

    # Expected result
    expected = ["bandit", "-c", "pyproject.toml", "-r", "."]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_run_tests() -> None:
    """Test func for run_tests."""
    # Call the function
    result = run_tests()

    # Expected result
    expected = ["pytest"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_add_updates_to_git() -> None:
    """Test func for add_updates_to_git."""
    # Call the function
    result = add_updates_to_git()

    # Expected result
    expected = ["git", "add", "pyproject.toml", "poetry.lock"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )
