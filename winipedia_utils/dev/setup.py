"""A script that can be called after you installed the package.

This script calls create tests, creates the pre-commit config, and
creates the pyproject.toml file and some other things to set up a project.
This package assumes you are using poetry and pre-commit.
This script is intended to be called once at the beginning of a project.
"""

from collections.abc import Callable
from typing import Any

from winipedia_utils.dev.configs.conftest import ConftestConfigFile
from winipedia_utils.dev.configs.pre_commit import PreCommitConfigConfigFile
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.dev.projects.create_root import create_root
from winipedia_utils.dev.testing.create_tests import create_tests
from winipedia_utils.utils.logging.logger import get_logger

logger = get_logger(__name__)


SETUP_STEPS: list[Callable[..., Any]] = [
    create_root,
    create_tests,
    create_root,  # second time to make sure __init__.py files are created
    PyprojectConfigFile.update_dependencies,
    PreCommitConfigConfigFile.run_hooks,
    ConftestConfigFile.run_tests,
]


def setup() -> None:
    """Set up the project."""
    for step in SETUP_STEPS:
        logger.info("Running setup step: %s", step.__name__)
        step()
    logger.info("Setup complete!")
