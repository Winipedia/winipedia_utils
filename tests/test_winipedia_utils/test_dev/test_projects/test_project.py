"""Tests for winipedia_utils.projects.project module."""

from pytest_mock import MockFixture

from winipedia_utils.dev.projects import project
from winipedia_utils.dev.projects.project import (
    create_project_root,
)
from winipedia_utils.utils.modules.module import create_module


def test_create_project_root(mocker: MockFixture) -> None:
    """Test func for _create_project_root."""
    spy_create_module = mocker.spy(project, create_module.__name__)
    create_project_root()
    spy_create_module.assert_called_once()
