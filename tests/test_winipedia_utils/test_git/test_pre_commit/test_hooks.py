"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_hooks
"""

from winipedia_utils.git.pre_commit.hooks import (
    add_version_patch_to_git,
    check_package_manager_configs,
    check_security,
    check_static_types,
    create_tests,
    format_code,
    install_packages,
    lint_code,
    lock_dependencies,
    patch_version,
    run_tests,
    update_package_manager,
    update_packages,
)
from winipedia_utils.projects.poetry.poetry import (
    POETRY_PATH,
    POETRY_RUN_ARGS,
    POETRY_RUN_PYTHON_ARGS,
    POETRY_RUN_RUFF_ARGS,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_patch_version() -> None:
    """Test func for patch_version."""
    # Call the function
    result = patch_version()

    # Expected result
    expected = [POETRY_PATH, "version", "patch"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_add_version_patch_to_git() -> None:
    """Test func for add_version_patch_to_git."""
    # Call the function
    result = add_version_patch_to_git()

    # Expected result
    expected = [*POETRY_RUN_ARGS, "git", "add", "pyproject.toml"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_update_package_manager() -> None:
    """Test func for update_package_manager."""
    # Call the function
    result = update_package_manager()

    # Expected result
    expected = [POETRY_PATH, "self", "update"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_install_packages() -> None:
    """Test func for install_packages."""
    # Call the function
    result = install_packages()

    # Expected result
    expected = [POETRY_PATH, "install"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_update_packages() -> None:
    """Test func for update_packages."""
    # Call the function
    result = update_packages()

    # Expected result
    expected = [POETRY_PATH, "update"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_lock_dependencies() -> None:
    """Test func for lock_dependencies."""
    # Call the function
    result = lock_dependencies()

    # Expected result
    expected = [POETRY_PATH, "lock"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_check_package_manager_configs() -> None:
    """Test func for check_package_manager_configs."""
    # Call the function
    result = check_package_manager_configs()

    # Expected result
    expected = [POETRY_PATH, "check", "--strict"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_create_tests() -> None:
    """Test func for create_tests."""
    # Call the function
    result = create_tests()

    # Expected result
    expected = [*POETRY_RUN_PYTHON_ARGS, "-m", "winipedia_utils.testing.create_tests"]

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
    expected = [*POETRY_RUN_RUFF_ARGS, "check", "--fix"]

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
    expected = [*POETRY_RUN_RUFF_ARGS, "format"]

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
    expected = [*POETRY_RUN_ARGS, "mypy"]

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
    expected = [*POETRY_RUN_ARGS, "bandit", "-c", "pyproject.toml", "-r", "."]

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
    expected = [*POETRY_RUN_ARGS, "pytest"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )
