"""Tests for winipedia_utils.setup module."""

import os
import platform
import sys
from contextlib import chdir
from pathlib import Path

import pytest

import winipedia_utils
from winipedia_utils.dev import setup
from winipedia_utils.dev.setup import SETUP_STEPS, get_setup_steps
from winipedia_utils.utils.modules.module import to_path
from winipedia_utils.utils.os.os import run_subprocess
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_get_setup_steps() -> None:
    """Test func for _get_setup_steps."""
    setup_steps = get_setup_steps()
    assert_with_msg(
        setup_steps == SETUP_STEPS,
        f"Expected {SETUP_STEPS}, got {setup_steps}",
    )


@pytest.mark.skipif(
    platform.system() == "Windows",
    reason="Test fails on Windows due to poetry add path fails",
)
def test_setup(tmp_path: Path) -> None:
    """Test func for _setup."""
    # on Actions windows-latest temp path is on another drive so poetry add path fails
    # so we use a tmp dir in the current dir
    # now test that in an empty folder with a pyproject.toml file
    # with a folder src that the setup works
    src_project_dir = tmp_path / "src_project"
    src_project_dir.mkdir()

    # Initialize git repo in the test project directory
    with chdir(src_project_dir):
        run_subprocess(["git", "init"])
        run_subprocess(["git", "config", "user.email", "test@example.com"])
        run_subprocess(["git", "config", "user.name", "Test User"])

    # Run setup from current poetry env in test project directory
    local_winipedia_utils_path = to_path(
        winipedia_utils.__name__, is_package=True
    ).parent.absolute()
    with chdir(src_project_dir):
        # Create a clean environment dict without VIRTUAL_ENV to force poetry
        # to create a new virtual environment instead of reusing the current one
        clean_env = os.environ.copy()
        clean_env.pop("VIRTUAL_ENV", None)

        # Get the current Python version in major.minor format
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

        run_subprocess(
            ["poetry", "init", "-n", f"--python=>={python_version}"],
            check=False,
            env=clean_env,
        )
        # Explicitly create a new virtual environment using the current Python
        run_subprocess(
            ["poetry", "env", "use", sys.executable], check=False, env=clean_env
        )
        run_subprocess(
            [
                "poetry",
                "add",
                local_winipedia_utils_path.as_posix(),
                "--editable",
            ],
            env=clean_env,
        )
        setup.setup()

    pkg_dir = src_project_dir / "src_project"
    assert_with_msg(
        (pkg_dir / "__init__.py").exists(),
        f"Expected {pkg_dir / '__init__.py'} to be created",
    )
