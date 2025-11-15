"""A script that can be called after you installed the package.

This script calls create tests, creates the pre-commit config, and
creates the pyproject.toml file and some other things to set up a project.
This package assumes you are using poetry and pre-commit.
This script is intended to be called once at the beginning of a project.
"""

from collections.abc import Callable
from typing import Any

from winipedia_utils.dev.configs.base.base import ConfigFile
from winipedia_utils.dev.configs.conftest import ConftestConfigFile
from winipedia_utils.dev.configs.pre_commit import PreCommitConfigConfigFile
from winipedia_utils.dev.projects.poetry.poetry import POETRY_ARG
from winipedia_utils.utils.logging.logger import get_logger
from winipedia_utils.utils.os.os import run_subprocess

logger = get_logger(__name__)


SETUP_STEPS: list[Callable[..., Any]] = [
    ConfigFile.init_winipedia_utils_config_files,
    lambda: run_subprocess([POETRY_ARG, "update", "--with", "dev"]),
    PreCommitConfigConfigFile.run_hooks,
    lambda: ConftestConfigFile().run_tests(check=False),  # creates tests
    ConftestConfigFile.run_tests,
]


def setup() -> None:
    """Set up the project."""
    for step in SETUP_STEPS:
        logger.info("Running setup step: %s", step.__name__)
        step()
    logger.info("Setup complete!")


if __name__ == "__main__":
    setup()
