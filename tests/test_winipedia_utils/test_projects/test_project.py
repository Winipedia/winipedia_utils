"""Tests for winipedia_utils.projects.project module."""

from pytest_mock import MockFixture

from winipedia_utils.modules.module import create_module
from winipedia_utils.projects import project
from winipedia_utils.projects.project import (
    create_project_root,
)


def test_create_project_root(mocker: MockFixture) -> None:
    """Test func for _create_project_root."""
    spy_create_module = mocker.spy(project, create_module.__name__)
    create_project_root()
    spy_create_module.assert_called_once()
