"""Has config utilities for pre-commit."""

from pathlib import Path
from typing import Any

import winipedia_utils
from winipedia_utils.git.pre_commit import run_hooks
from winipedia_utils.logging.logger import get_logger
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.os.os import run_subprocess
from winipedia_utils.projects.poetry.poetry import POETRY_RUN_ARGS
from winipedia_utils.projects.project import make_name_from_package
from winipedia_utils.text.config import YamlConfigFile

logger = get_logger(__name__)


class PreCommitConfigFile(YamlConfigFile):
    """Config file for pre-commit."""

    PATH = Path(".pre-commit-config.yaml")

    def __init__(self) -> None:
        """Init the file."""
        super().__init__()
        self.install()

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        hook_name = make_name_from_package(winipedia_utils, capitalize=False)
        return {
            "repos": [
                {
                    "repo": "local",
                    "hooks": [
                        {
                            "id": hook_name,
                            "name": hook_name,
                            "entry": f"python -m {make_obj_importpath(run_hooks)}",
                            "language": "system",
                            "always_run": True,
                            "pass_filenames": False,
                        }
                    ],
                },
            ]
        }

    @classmethod
    def install(cls) -> None:
        """Installs the pre commits in the config."""
        logger.info("Running pre-commit install")
        run_subprocess([*POETRY_RUN_ARGS, "pre-commit", "install"], check=True)
