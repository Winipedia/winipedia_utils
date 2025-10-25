"""Config utilities for .gitignore."""

from pathlib import Path
from typing import Any

from winipedia_utils.text.config import ConfigFile


class GitIgnoreConfigFile(ConfigFile):
    """Config file for .gitignore."""

    PATH = Path(".gitignore")

    IGNORE_KEY = "ignore"

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def load(self) -> dict[str, Any]:
        """Load the config file."""
        return self.load_static()

    @classmethod
    def load_static(cls) -> dict[str, Any]:
        """Load the config file."""
        paths = cls.PATH.read_text().splitlines()
        return {cls.IGNORE_KEY: paths}

    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""
        patterns = config.get(self.IGNORE_KEY, [])
        self.path.write_text("\n".join(patterns))

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        from winipedia_utils.testing.config import (  # noqa: PLC0415  # avoid circular import
            ExperimentConfigFile,
        )

        needed = [
            "__pycache__/",
            ".idea/",
            ".mypy_cache/",
            ".pytest_cache/",
            ".ruff_cache/",
            ".vscode/",
            "dist/",
            ".git/",  # for walk_os_skipping_gitignore_patterns func
            ExperimentConfigFile.PATH.name,  # for executing experimental code
        ]
        existing = self.load()[self.IGNORE_KEY]
        needed = [p for p in needed if p not in set(existing)]
        return {self.IGNORE_KEY: existing + needed}
