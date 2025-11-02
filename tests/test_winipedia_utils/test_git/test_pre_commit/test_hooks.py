"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_hooks
"""

from winipedia_utils.git.pre_commit.hooks import (
    add_lock_file_to_git,
    add_popped_stash_to_git,
    add_updates_to_git,
    add_version_patch_to_git,
    check_package_manager_configs,
    check_security,
    check_static_types,
    create_missing_tests,
    fetch_latest_changes,
    format_code,
    install_dependencies_with_dev,
    lint_code,
    lock_dependencies,
    patch_version,
    pop_stashed_changes,
    rebase_on_main,
    run_tests,
    stash_changes,
    update_dependencies_with_dev,
    update_package_manager,
)
from winipedia_utils.projects.poetry.poetry import (
    POETRY_ARG,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_fetch_latest_changes() -> None:
    """Test func for fetch_latest_changes."""
    # Call the function
    result = fetch_latest_changes()

    # Expected result
    expected = ["git", "fetch", "origin"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )
    assert_with_msg(
        result[0] == "git",
        f"Expected first element to be 'git', got {result[0]}",
    )


def test_stash_changes() -> None:
    """Test func for stash_changes."""
    # Call the function
    result = stash_changes()

    # Expected result
    expected = [
        "git",
        "stash",
        "push",
        "-m",
        "WIP: Temporarily stashed changes before rebasing",
    ]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_rebase_on_main() -> None:
    """Test func for rebase_on_main."""
    # Call the function
    result = rebase_on_main()

    # Expected result
    expected = ["git", "rebase", "origin/main"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_pop_stashed_changes() -> None:
    """Test func for pop_stashed_changes."""
    # Call the function
    result = pop_stashed_changes()

    # Expected result
    expected = ["git", "stash", "pop"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_add_popped_stash_to_git() -> None:
    """Test func for add_changes_to_git."""
    # Call the function
    result = add_popped_stash_to_git()

    # Expected result
    expected = ["git", "add", "."]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_patch_version() -> None:
    """Test func for patch_version."""
    # Call the function
    result = patch_version()

    # Expected result
    expected = [POETRY_ARG, "version", "patch"]

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
    expected = ["git", "add", "pyproject.toml"]

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
    expected = [POETRY_ARG, "self", "update"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_install_dependencies_with_dev() -> None:
    """Test func for install_packages."""
    # Call the function
    result = install_dependencies_with_dev()

    # Expected result
    expected = [POETRY_ARG, "install", "--with", "dev"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_update_dependencies_with_dev() -> None:
    """Test func for update_packages."""
    # Call the function
    result = update_dependencies_with_dev()

    # Expected result
    expected = [POETRY_ARG, "update", "--with", "dev"]

    # Verify the result
    assert_with_msg(
        set(expected).issubset(set(result)),
        f"Expected {expected}, got {result}",
    )


def test_lock_dependencies() -> None:
    """Test func for lock_dependencies."""
    # Call the function
    result = lock_dependencies()

    # Expected result
    expected = [POETRY_ARG, "lock"]

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

    expected = ["poetry", "run", "python", "-m", "winipedia_utils.testing.create_tests"]

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
    expected = ["git", "add", "pyproject.toml"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_add_lock_file_to_git() -> None:
    """Test func for add_lock_file_to_git."""
    # Call the function
    result = add_lock_file_to_git()

    # Expected result
    expected = ["git", "add", "poetry.lock"]

    # Verify the result
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )
