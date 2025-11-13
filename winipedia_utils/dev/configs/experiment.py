"""Config utilities for experiment.py."""

import subprocess
from pathlib import Path

from winipedia_utils.dev.configs.base.base import PythonConfigFile

print(subprocess.run(["ls", "-l"], check=False))  # noqa: S607, T201


class ExperimentConfigFile(PythonConfigFile):
    """Config file for experiment.py.

    Is at root level and in .gitignore for experimentation.
    """

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        return Path()

    @classmethod
    def get_content_str(cls) -> str:
        """Get the config."""
        return '''"""This file is for experimentation and is ignored by git."""
'''
