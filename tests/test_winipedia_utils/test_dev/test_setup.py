"""Tests for winipedia_utils.setup module."""

from contextlib import chdir
from pathlib import Path

from winipedia_utils.dev.setup import SETUP_STEPS, get_setup_steps
from winipedia_utils.utils.os.os import run_subprocess, which_with_raise
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_get_setup_steps() -> None:
    """Test func for _get_setup_steps."""
    setup_steps = get_setup_steps()
    assert_with_msg(
        setup_steps == SETUP_STEPS,
        f"Expected {SETUP_STEPS}, got {setup_steps}",
    )


def test_setup(tmp_path: Path) -> None:
    """Test func for _setup."""
    # now test that in an empty folder with a pyproject.toml file
    # with a folder src that the setup works
    src_project_dir = tmp_path / "src_project"
    src_project_dir.mkdir()

    pyproject_toml = src_project_dir / "pyproject.toml"
    pyproject_toml.write_text(
        """[project]
name = "src-project"
version = "0.1.0"
description = "A test project"
authors = [
    {name = "Winipedia",email = "win.steveker@gmx.de"}
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "winipedia-utils (>=0.6.7,<0.7.0)"
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
    )

    # Initialize git repo in the test project directory
    with chdir(src_project_dir):
        run_subprocess(["git", "init"])
        run_subprocess(["git", "config", "user.email", "test@example.com"])
        run_subprocess(["git", "config", "user.name", "Test User"])

    # Run setup from current poetry env in test project directory
    poetry_path = which_with_raise("poetry")
    with chdir(src_project_dir):
        run_subprocess(
            [
                str(poetry_path),
                "run",
                "python",
                "-m",
                "winipedia_utils.dev.setup",
            ]
        )

    pkg_dir = src_project_dir / "src_project"
    assert_with_msg(
        (pkg_dir / "__init__.py").exists(),
        f"Expected {pkg_dir / '__init__.py'} to be created",
    )
