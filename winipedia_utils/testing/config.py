"""Config utilities for testing."""

from abc import abstractmethod
from pathlib import Path
from typing import Any

from winipedia_utils.testing.convention import TESTS_PACKAGE_NAME
from winipedia_utils.text.config import ConfigFile


class PythonConfigFile(ConfigFile):
    """Base class for python config files."""

    CONTENT_KEY = "content"

    def load(self) -> dict[str, str]:
        """Load the config file."""
        return {self.CONTENT_KEY: self.path.read_text()}

    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""
        self.path.write_text(config[self.CONTENT_KEY])

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        return {self.CONTENT_KEY: self.get_content()}

    @abstractmethod
    def get_content(self) -> str:
        """Get the content."""
        return self.load()[self.CONTENT_KEY]


class ConftestConfigFile(PythonConfigFile):
    """Config file for conftest.py."""

    PATH = Path(f"{TESTS_PACKAGE_NAME}/conftest.py")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_content(self) -> str:
        """Get the config content."""
        return '''"""Pytest configuration for tests.

This module configures pytest plugins for the test suite, setting up the necessary
fixtures and hooks for the different
test scopes (function, class, module, package, session).
It also import custom plugins from tests/base/scopes.
This file should not be modified manually.
"""

pytest_plugins = ["winipedia_utils.testing.tests.conftest"]
'''


class ZeroTestConfigFile(PythonConfigFile):
    """Config file for test_0.py."""

    PATH = Path(f"{TESTS_PACKAGE_NAME}/test_0.py")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_content(self) -> str:
        """Get the config."""
        return '''"""Contains an empty test."""


def test_0() -> None:
    """Empty test.

    Exists so that when no tests are written yet the base fixtures are executed.
    """
'''


class ExperimentConfigFile(PythonConfigFile):
    """Config file for experiment.py.

    Is at root level and in .gitignore for experimentation.
    """

    PATH = Path("experiment.py")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_content(self) -> str:
        """Get the config."""
        return '''"""This file is for experimentation and is ignored by git."""
'''
