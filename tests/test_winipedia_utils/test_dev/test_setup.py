"""Tests for winipedia_utils.setup module."""

import os
import platform
import shutil
from contextlib import chdir
from pathlib import Path

import pytest

import winipedia_utils
from winipedia_utils.dev import setup
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.utils.modules.module import to_path
from winipedia_utils.utils.os.os import run_subprocess
from winipedia_utils.utils.testing.assertions import assert_with_msg


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

    # copy the winipedia_utils package to tmp_path/winipedia_utils with shutil
    winipedia_utils_temp_path = tmp_path / PyprojectConfigFile.get_project_name()
    shutil.copytree(
        to_path(winipedia_utils.__name__, is_package=True).parent,
        winipedia_utils_temp_path,
    )
    winipedia_utils_temp_path = winipedia_utils_temp_path.resolve()
    with chdir(winipedia_utils_temp_path):
        # build the package
        run_subprocess(["poetry", "build"])

    dist_files = list((winipedia_utils_temp_path / "dist").glob("*.whl"))
    wheel_path = dist_files[-1].as_posix()

    src_project_dir = tmp_path / "src-project"
    src_project_dir.mkdir()

    # Get the current Python version in major.minor format
    python_version = str(PyprojectConfigFile.get_first_supported_python_version())

    # Initialize git repo in the test project directory
    with chdir(src_project_dir):
        run_subprocess(["git", "init"])
        run_subprocess(["git", "config", "user.email", "test@example.com"])
        run_subprocess(["git", "config", "user.name", "Test User"])

    with chdir(src_project_dir):
        # Create a clean environment dict without VIRTUAL_ENV to force poetry
        # to create a new virtual environment instead of reusing the current one
        clean_env = os.environ.copy()
        clean_env.pop("VIRTUAL_ENV", None)

        run_subprocess(
            ["poetry", "init", "--no-interaction", f"--python=>={python_version}"],
            env=clean_env,
        )
        # Explicitly create a new virtual environment using the current Python
        run_subprocess(["poetry", "env", "use", python_version], env=clean_env)

        run_subprocess(
            [
                "poetry",
                "add",
                wheel_path,
            ],
            env=clean_env,
        )
        # Run setup via poetry run to ensure it uses the new virtual environment
        # with the editable install of the current state of winipedia_utils
        setup.setup()

    pkg_dir = src_project_dir / "src_project"
    assert_with_msg(
        (pkg_dir / "__init__.py").exists(),
        f"Expected {pkg_dir / '__init__.py'} to be created",
    )
