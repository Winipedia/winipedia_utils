"""Tests for winipedia_utils.projects.poetry.poetry module."""

from pytest_mock import MockFixture

from winipedia_utils.projects.poetry.poetry import _install_dev_dependencies
from winipedia_utils.testing.assertions import assert_with_msg


def test__install_dev_dependencies(mocker: MockFixture) -> None:
    """Test func for _install_dev_dependencies."""
    # Mock the dependencies
    mock_dev_dependencies = ["pytest", "ruff", "mypy"]
    mocker.patch(
        "winipedia_utils.projects.poetry.poetry._DEV_DEPENDENCIES",
        mock_dev_dependencies,
    )

    # Mock run_subprocess
    mock_run_subprocess = mocker.patch(
        "winipedia_utils.projects.poetry.poetry.run_subprocess"
    )

    # Mock logger
    mock_logger = mocker.patch("winipedia_utils.projects.poetry.poetry.logger")

    _install_dev_dependencies()

    # Verify basic functionality
    assert_with_msg(
        mock_logger.info.called,
        "Expected logger.info to be called",
    )

    assert_with_msg(
        mock_run_subprocess.called,
        "Expected run_subprocess to be called",
    )
