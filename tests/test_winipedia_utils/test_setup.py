"""Tests for winipedia_utils.setup module."""

import sys
from contextlib import chdir
from pathlib import Path
from typing import Any

from pytest_mock import MockFixture

from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.setup import SETUP_STEPS, get_setup_steps, setup
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_setup_steps() -> None:
    """Test func for _get_setup_steps."""
    setup_steps = get_setup_steps()
    assert_with_msg(
        setup_steps == SETUP_STEPS,
        f"Expected {SETUP_STEPS}, got {setup_steps}",
    )


def test_setup(mocker: MockFixture, tmp_path: Path) -> None:
    """Test func for _setup."""
    # patch _get_setup_steps to return a list of mock functions
    # which we assert are called once
    mock_setup_steps: list[Any] = []
    for i, step in enumerate(SETUP_STEPS):
        mock_step = mocker.MagicMock()
        mock_step.__name__ = f"mock_step_{step.__name__}_{i}"
        mock_setup_steps.append(mock_step)

    mocker.patch(
        make_obj_importpath(get_setup_steps),
        return_value=mock_setup_steps,
    )

    # assert all mock setup steps are called once
    setup()
    for mock_setup_step in mock_setup_steps:
        assert_with_msg(
            mock_setup_step.call_count == 1,
            f"Expected {mock_setup_step} to be called exactly once",
        )

    # remove all mocks
    mocker.stopall()

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
license = {text = "MIT"}
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

    pkg_dir = src_project_dir / "src_project"
    pkg_dir.mkdir()

    # mock subprocess.run to avoid actually calling it
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0

    # Add src_project_dir to sys.path so the package can be imported

    original_sys_path = sys.path.copy()
    try:
        sys.path.insert(0, str(src_project_dir))
        with chdir(src_project_dir):
            setup()
    finally:
        sys.path = original_sys_path

    assert_with_msg(
        (pkg_dir / "__init__.py").exists(),
        f"Expected {pkg_dir / '__init__.py'} to be created",
    )
