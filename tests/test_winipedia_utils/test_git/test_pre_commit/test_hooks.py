"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_hooks
"""

from winipedia_utils.git.pre_commit.hooks import (
    _add_version_patch_to_git,
    _check_configurations,
    _creating_tests,
    _formating,
    _install_packages,
    _linting,
    _lock_dependencies,
    _security_checking,
    _testing,
    _type_checking,
    _update_package_manager,
    _update_packages,
    _version_patch,
)
from winipedia_utils.projects.poetry.poetry import (
    POETRY_PATH,
    POETRY_RUN_ARGS,
    POETRY_RUN_PYTHON_ARGS,
    POETRY_RUN_RUFF_ARGS,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test__version_patch() -> None:
    """Test func for _version_patch."""
    # Call the function
    result = _version_patch()

    # Expected result
    expected = [POETRY_PATH, "version", "patch"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__add_version_patch_to_git() -> None:
    """Test func for _add_version_patch_to_git."""
    # Call the function
    result = _add_version_patch_to_git()

    # Expected result
    expected = [*POETRY_RUN_ARGS, "git", "add", "pyproject.toml"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__update_package_manager() -> None:
    """Test func for _update_package_manager."""
    # Call the function
    result = _update_package_manager()

    # Expected result
    expected = [POETRY_PATH, "self", "update"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__install_packages() -> None:
    """Test func for _install_packages."""
    # Call the function
    result = _install_packages()

    # Expected result
    expected = [POETRY_PATH, "install"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__update_packages() -> None:
    """Test func for _update_packages."""
    # Call the function
    result = _update_packages()

    # Expected result
    expected = [POETRY_PATH, "update"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__lock_dependencies() -> None:
    """Test func for _lock_dependencies."""
    # Call the function
    result = _lock_dependencies()

    # Expected result
    expected = [POETRY_PATH, "lock"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__check_configurations() -> None:
    """Test func for _check_configurations."""
    # Call the function
    result = _check_configurations()

    # Expected result
    expected = [POETRY_PATH, "check", "--strict"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__creating_tests() -> None:
    """Test func for _creating_tests."""
    # Call the function
    result = _creating_tests()

    # Expected result
    expected = [*POETRY_RUN_PYTHON_ARGS, "-m", "winipedia_utils.testing.create_tests"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__linting() -> None:
    """Test func for _linting."""
    # Call the function
    result = _linting()

    # Expected result
    expected = [*POETRY_RUN_RUFF_ARGS, "check", "--fix"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__formating() -> None:
    """Test func for _formating."""
    # Call the function
    result = _formating()

    # Expected result
    expected = [*POETRY_RUN_RUFF_ARGS, "format"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__type_checking() -> None:
    """Test func for _type_checking."""
    # Call the function
    result = _type_checking()

    # Expected result
    expected = [*POETRY_RUN_ARGS, "mypy"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__security_checking() -> None:
    """Test func for _security_checking."""
    # Call the function
    result = _security_checking()

    # Expected result
    expected = [*POETRY_RUN_ARGS, "bandit", "-c", "pyproject.toml", "-r", "."]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test__testing() -> None:
    """Test func for _testing."""
    # Call the function
    result = _testing()

    # Expected result
    expected = [*POETRY_RUN_ARGS, "pytest"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )
