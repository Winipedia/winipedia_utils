"""Utilities for working with Python projects."""

from winipedia_utils.dev.configs.base.base import ConfigFile
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.dev.testing.convention import TESTS_PACKAGE_NAME
from winipedia_utils.utils.modules.module import create_module


def create_root() -> None:
    """Create the project root."""
    src_package_name = PyprojectConfigFile.get_package_name()
    create_module(src_package_name, is_package=True)
    create_module(TESTS_PACKAGE_NAME, is_package=True)
    ConfigFile.init_config_files()
