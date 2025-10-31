"""Has config utilities for pre-commit."""

from pathlib import Path
from typing import Any

import winipedia_utils
from winipedia_utils.logging.logger import get_logger
from winipedia_utils.modules.package import make_name_from_package
from winipedia_utils.os.os import run_subprocess
from winipedia_utils.text.config import YamlConfigFile

logger = get_logger(__name__)


class PreCommitConfigConfigFile(YamlConfigFile):
    """Config file for pre-commit."""

    @classmethod
    def get_filename(cls) -> str:
        """Get the filename of the config file."""
        filename = super().get_filename()
        return f".{filename.replace('_', '-')}"

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        return Path()

    @classmethod
    def get_configs(cls) -> dict[str, Any]:
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
                            "entry": cls.get_poetry_run_setup_script(),
                            "language": "system",
                            "always_run": True,
                            "pass_filenames": False,
                        }
                    ],
                },
            ]
        }

    def __init__(self) -> None:
        """Init the file."""
        super().__init__()
        self.install()

    @classmethod
    def install(cls) -> None:
        """Installs the pre commits in the config."""
        logger.info("Running pre-commit install")
        run_subprocess(["pre-commit", "install"], check=True)
