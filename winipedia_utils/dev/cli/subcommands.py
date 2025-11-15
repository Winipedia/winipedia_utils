"""Subcommands for the CLI.

They will be automatically imported and added to the CLI
IMPORTANT: All funcs in this file will be added as subcommands.
So best to define the logic elsewhere and just call it here in a wrapper.
"""

from winipedia_utils.dev.projects.create_root import create_root as create_root_cmd
from winipedia_utils.dev.setup import setup as setup_cmd
from winipedia_utils.dev.testing.create_tests import create_tests as create_tests_cmd


def create_root() -> None:
    """Create the project root."""
    create_root_cmd()


def create_tests() -> None:
    """Create all test files for the project."""
    create_tests_cmd()


def setup() -> None:
    """Set up the project."""
    setup_cmd()
