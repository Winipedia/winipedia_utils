"""module contains functions that return the input for subprocess.run().

Each function is named after the hook it represents. The docstring of each function
describes the hook it represents. The function returns a list of strings that
represent the command to run. The first string is the command, and the following
strings are the arguments to the command. These funcs will be called by
run_hooks.py, which will pass the returned list to subprocess.run().
"""

from pathlib import Path

from winipedia_utils.projects.poetry.poetry import (
    POETRY_ARG,
    get_run_python_module_args,
)


def patch_version() -> list[str | Path]:
    """Patch the version in pyproject.toml.

    This function returns the input for subprocess.run() to patch the version
    in pyproject.toml.
    """
    return [POETRY_ARG, "version", "patch"]


def add_version_patch_to_git() -> list[str | Path]:
    """Add the version patch to git.

    This function returns the input for subprocess.run() to add the version
    patch to git, so that the hook does not fail bc the file was changed.
    """
    return ["git", "add", "pyproject.toml"]


def update_package_manager() -> list[str | Path]:
    """Update the package manager.

    This function returns the input for subprocess.run() to update the package
    manager.
    """
    return [POETRY_ARG, "self", "update"]


def install_dependencies_with_dev() -> list[str | Path]:
    """Install all dependencies.

    This function returns the input for subprocess.run() to install all dependencies.
    """
    return [POETRY_ARG, "install", "--with", "dev"]


def update_dependencies_with_dev() -> list[str | Path]:
    """Update all dependencies.

    This function returns the input for subprocess.run() to update all dependencies.
    """
    return [POETRY_ARG, "update", "--with", "dev"]


def add_updates_to_git() -> list[str | Path]:
    """Add the updated dependencies to git.

    This function returns the input for subprocess.run() to add the updated
    dependencies to git, so that the hook does not fail bc the file was changed.
    """
    return ["git", "add", "pyproject.toml"]


def lock_dependencies() -> list[str | Path]:
    """Lock the dependencies.

    This function returns the input for subprocess.run() to lock the dependencies.
    """
    return [POETRY_ARG, "lock"]


def add_lock_file_to_git() -> list[str | Path]:
    """Add the lock file to git.

    This function returns the input for subprocess.run() to add the lock file
    to git, so that the hook does not fail bc the file was changed.
    """
    return ["git", "add", "poetry.lock"]


def check_package_manager_configs() -> list[str | Path]:
    """Check that poetry.lock and pyproject.toml is up to date.

    This function returns the input for subprocess.run() to check that poetry.lock
    is up to date.
    """
    return [POETRY_ARG, "check", "--strict"]


def create_missing_tests() -> list[str | Path]:
    """Create all tests for the project.

    This function returns the input for subprocess.run() to create all tests.
    """
    from winipedia_utils.testing import (  # noqa: PLC0415  # avoid circular import
        create_tests,
    )

    return [*get_run_python_module_args(create_tests)]


def lint_code() -> list[str | Path]:
    """Check the code.

    This function returns the input for subprocess.run() to lint the code.
    It autofixes all errors that can be autofixed with --fix.
    """
    return ["ruff", "check", "--fix"]


def format_code() -> list[str | Path]:
    """Format the code.

    This function calls ruff format to format the code.
    """
    return ["ruff", "format"]


def check_static_types() -> list[str | Path]:
    """Check the types.

    This function returns the input for subprocess.run() to check the static types.
    """
    return ["mypy"]


def check_security() -> list[str | Path]:
    """Check the security of the code.

    This function returns the input for subprocess.run() to check the security of
    the code.
    """
    return ["bandit", "-c", "pyproject.toml", "-r", "."]


def run_tests() -> list[str | Path]:
    """Run the tests.

    This function returns the input for subprocess.run() to run all tests.
    """
    return ["pytest"]
